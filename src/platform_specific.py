import numpy as np
import PIL.Image
import platform
import time
import PIL


if platform.system() == "Linux":
    from collections import namedtuple
    import Xlib
    import Xlib.display
    import uinput


    class Controller:
        '''
        Create an virtual XBOX 360 controller.
        Work with uinput (https://github.com/tuomasjjrasanen/python-uinput).
        '''

        # The hold button time in seconds in case of rapid (instant) action to behave more human like.
        INSTANT_ACTION_DURATION = 0.05

        def __init__(self):
            '''
            Create the controller and make it appear in "/dev".
            Returns:
                An "Controller" instance.
            '''
            self.events = (
                uinput.BTN_A,
                uinput.BTN_B,
                uinput.BTN_X,
                uinput.BTN_Y,
                uinput.BTN_TL,
                uinput.BTN_TR,
                uinput.BTN_START,
                uinput.ABS_X + (-32768, 32767, 0, 0),
                uinput.ABS_Y + (-32768, 32767, 0, 0),
            )
            self.device = uinput.Device(
                self.events,
                vendor=0x045e,
                product=0x028e,
                version=0x110,
                name="Microsoft X-Box 360 pad",
            )
            time.sleep(1)
            self.reset()
            self.apply()
        
        def _range_to_joyaxe(self, value):
            value = int(value * 2**(16-1))
            value = min(max(value, -32768), 32767)
            return value

        def reset(self):
            '''
            reset() behaves as if the human player were not touching the controller.
            You have to call apply() if you want to apply immediately.
            Or you can set controller state before applying.
            '''
            self.device.emit(uinput.BTN_A, 0, syn=False)
            self.device.emit(uinput.BTN_B, 0, syn=False)
            self.device.emit(uinput.BTN_X, 0, syn=False)
            self.device.emit(uinput.BTN_Y, 0, syn=False)
            self.device.emit(uinput.BTN_TL, 0, syn=False)
            self.device.emit(uinput.BTN_TR, 0, syn=False)
            self.device.emit(uinput.BTN_START, 0, syn=False)
            self.device.emit(uinput.ABS_X, self._range_to_joyaxe(0.0), syn=False)
            self.device.emit(uinput.ABS_Y, self._range_to_joyaxe(0.0), syn=False)

        def apply(self):
            '''
            Sync the current controller image with the system.
            '''
            self.device.syn()
            self.reset()
        
        def instant_pad_up(self):
            self.device.emit(uinput.ABS_Y, self._range_to_joyaxe(-1), syn=True)
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.device.emit(uinput.ABS_Y, self._range_to_joyaxe(0), syn=True)

        def instant_pad_down(self):
            self.device.emit(uinput.ABS_Y, self._range_to_joyaxe(1), syn=True)
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.device.emit(uinput.ABS_Y, self._range_to_joyaxe(0), syn=True)

        def instant_pad_left(self):
            self.device.emit(uinput.ABS_X, self._range_to_joyaxe(-1), syn=True)
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.device.emit(uinput.ABS_X, self._range_to_joyaxe(0), syn=True)

        def instant_pad_right(self):
            self.device.emit(uinput.ABS_X, self._range_to_joyaxe(1), syn=True)
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.device.emit(uinput.ABS_X, self._range_to_joyaxe(0), syn=True)

        def instant_a(self):
            self.device.emit(uinput.BTN_A, 1, syn=True)
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.device.emit(uinput.BTN_A, 0, syn=True)

        def instant_b(self):
            self.device.emit(uinput.BTN_B, 1, syn=True)
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.device.emit(uinput.BTN_B, 0, syn=True)

        def instant_start(self):
            self.device.emit(uinput.BTN_START, 1, syn=True)
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.device.emit(uinput.BTN_START, 0, syn=True)

        def go_forward(self):
            self.device.emit(uinput.BTN_B, 1, syn=False)
        
        def go_backward(self):
            self.device.emit(uinput.BTN_A, 1, syn=False)

        def go_x_direction(self, strengh):
            self.device.emit(uinput.ABS_X, self._range_to_joyaxe(strengh), syn=False)

        def set_y_direction(self, strengh):
            self.device.emit(uinput.ABS_Y, self._range_to_joyaxe(strengh), syn=False)

        def look_backward(self):
            self.device.emit(uinput.BTN_Y, 1, syn=False)

        def throw_horn(self):
            self.device.emit(uinput.BTN_TL, 1, syn=False)

        def bump_drift(self):
            self.device.emit(uinput.BTN_TR, 1, syn=False)


    class Monitor:
        '''
        Take screenshots of yuzu game instance from the current X server attached on the display.
        Work with xlib (https://github.com/python-xlib/python-xlib)
        '''

        MyGeom = namedtuple('MyGeom', 'x y height width')

        def __init__(self):
            '''
            Create the monitor.
            Returns:
                An "Monitor" instance.
            '''
            self.disp = Xlib.display.Display()
            self.root = self.disp.screen().root
            self.win_hnd = None 

        def _find_win_id(self):
            '''
            Find yuzu game window.
            '''
            try:
                winid_list = self.root.get_full_property(self.disp.intern_atom('_NET_CLIENT_LIST'), Xlib.X.AnyPropertyType).value
                for winid in winid_list:
                    win = self.disp.create_resource_object('window', winid)
                    transient_for = win.get_wm_transient_for()
                    wmname = win.get_wm_name()
                    if transient_for == None:
                        if isinstance(wmname, str) and "yuzu" in wmname and "Mainline" in wmname:
                            self.win_hnd = self.disp.create_resource_object('window', winid)
            except Xlib.error.XError:
                pass

        def _check_instance(self):
            '''
            Check if yuzu game window was found.
            '''
            if self.win_hnd is None:
                self._find_win_id()

        def _get_absolute_geometry(self):
            win = self.win_hnd
            geom = win.get_geometry()
            (x, y) = (geom.x, geom.y)
            while True:
                parent = win.query_tree().parent
                pgeom = parent.get_geometry()
                x += pgeom.x
                y += pgeom.y
                if parent.id == self.root.id:
                    break
                win = parent
            return Monitor.MyGeom(x, y, geom.height, geom.width)

        def _get_window_pos(self):
            geom = self._get_absolute_geometry()
            x1 = geom.x
            y1 = geom.y
            return x1, y1, geom.width, geom.height

        def get_screen_shot(self):
            '''
            Get the current game screenshot.
            Returns:
                The RGB screenshot in the shape [128, 128, 3]
            '''
            self._check_instance()

            x, y, w, h = self._get_window_pos()

            x_raw = self.root.get_image(x, y, w, h, Xlib.X.ZPixmap, 0xffffffff)
            image = PIL.Image.frombuffer('RGB', (w, h), x_raw.data, 'raw', 'BGRX', 0, 1)
            image = image.resize((128, 128))
            image = np.asarray(image, dtype=np.uint8)

            return image


elif platform.system() == "Windows":
    import vgamepad as vg
    import win32gui
    import win32con
    import win32ui

    class Controller:
        '''
        Create an virtual XBOX 360 controller.
        Work with VX360Gamepad (https://github.com/yannbouteiller/vgamepad).
        '''

        INSTANT_ACTION_DURATION = 0.05

        def __init__(self):
            self.gamepad = vg.VX360Gamepad()
            time.sleep(1)
        
        def apply(self):
            self.gamepad.update()
            self.gamepad.reset()
        
        def instant_pad_up(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            self.apply()
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.gamepad.update()

        def instant_pad_down(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            self.apply()
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.gamepad.update()

        def instant_pad_left(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            self.apply()
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.gamepad.update()

        def instant_pad_right(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            self.apply()
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.gamepad.update()

        def instant_a(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            self.apply()
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.gamepad.update()

        def instant_b(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            self.apply()
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.gamepad.update()

        def instant_start(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
            self.apply()
            time.sleep(Controller.INSTANT_ACTION_DURATION)
            self.gamepad.update()

        def go_forward(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        
        def go_backward(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

        def go_x_direction(self, strengh):
            value = int(strengh * 2**(16-1))
            value = min(max(value, -32768), 32767)
            self.gamepad.left_joystick(x_value=value, y_value=self.gamepad.report.sThumbLY)

        def set_y_direction(self, strengh):
            value = int(strengh * 2**(16-1))
            value = min(max(value, -32768), 32767)
            self.gamepad.left_joystick(x_value=self.gamepad.report.sThumbLX, y_value=value)

        def look_backward(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

        def throw_horn(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)

        def bump_drift(self):
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)



    class Monitor:
        '''
        Take screenshots of yuzu game instance.
        Work with Windows APIs (https://github.com/mhammond/pywin32).
        WARNING : The API seem broken on Windows 11, somes workaround should be made.
        '''

        def __init__(self):
            self.instance_hwnd = None

        def _find_hwnd_instance(self):
            def _win32EnumCallback(hwnd, args):
                title = win32gui.GetWindowText(hwnd)
                if "yuzu" in title and "Mainline" in title:
                    self.instance_hwnd = hwnd

            while self.instance_hwnd is None:
                print("Waiting for mario kart 8 1.7.1 yuzu instance...")
                win32gui.EnumWindows(_win32EnumCallback, None)
                time.sleep(1.0)
            print("Waiting for mario kart 8 1.7.1 yuzu instance... OK")

        def _check_instance(self):
            if self.instance_hwnd is None or not win32gui.IsWindow(self.instance_hwnd):
                self._find_hwnd_instance()

        def get_screen_shot(self):
            '''
            Get the current game screenshot.
            Returns:
                The RGB screenshot in the shape [128, 128, 3]
            '''
            self._check_instance()

            win_pos = win32gui.GetWindowRect(self.instance_hwnd)
            win_x   = win_pos[0]
            win_y   = win_pos[1]

            frm_x, frm_y, frm_w, frm_h = win32gui.GetClientRect(self.instance_hwnd)
            frm_x, frm_y = win32gui.ClientToScreen(self.instance_hwnd, (frm_x, frm_y))
            frm_w, frm_h = win32gui.ClientToScreen(self.instance_hwnd, (frm_w - frm_x, frm_h - frm_y))

            wDC         = win32gui.GetWindowDC(self.instance_hwnd)
            dcObj       = win32ui.CreateDCFromHandle(wDC)
            cDC         = dcObj.CreateCompatibleDC()
            dataBitMap  = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dcObj, frm_w, frm_h)
            cDC.SelectObject(dataBitMap)
            cDC.BitBlt((0, 0), (frm_w, frm_h), dcObj, (frm_x - win_x, frm_y - win_y), win32con.SRCCOPY)

            bmpstr  = dataBitMap.GetBitmapBits(True)
            image   = PIL.Image.frombuffer('RGB', (frm_w, frm_h), bmpstr, 'raw', 'BGRX', 0, 1)
            # image   = image.crop((0, 50, 100, 100))
            image   = image.resize((128, 128))
            image   = np.asarray(image, dtype=np.uint8)

            # free resources
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(self.instance_hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())

            return image