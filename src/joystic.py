import threading
import evdev
import time


class JoysticPS2:
    '''
    Read the state of an Playstation 2 controller (yeah...) to produce an RL agent like action vector.
    Used for debugging purposes.
    Work with evdev (https://github.com/gvalkov/python-evdev).
    '''
    class Inputs:
        def __init__(self):
            self.cross      = 0
            self.circle     = 0
            self.triangle   = 0
            self.square     = 0
            #
            self.right  = 0
            self.up     = 0
            self.left   = 0
            self.down   = 0
            #
            self.l1 = 0
            self.l2 = 0
            self.l3 = 0
            self.r1 = 0
            self.r2 = 0
            self.r3 = 0
            #
            self.start  = 0
            self.select = 0
            #
            self.joy_r_x = 0
            self.joy_r_y = 0
            self.joy_l_x = 0
            self.joy_l_y = 0

    def __init__(self, device):
        self._device = evdev.InputDevice(device)
        self._thread = threading.Thread(target=self._monitoring_thread)
        self._active = True
        self.inputs  = JoysticPS2.Inputs()
        self._thread.start()

    def _monitoring_thread(self):
        while self._active:
            event = self._device.read_one()
            if event is None:
                time.sleep(1/60)
                continue

            if event.type == evdev.ecodes.EV_KEY:
                ev = evdev.categorize(event)
                # print(ev.scancode, ev.keystate)

                if ev.scancode == 290:
                    self.inputs.cross = ev.keystate
                elif ev.scancode == 289:
                    self.inputs.circle = ev.keystate
                elif ev.scancode == 288:
                    self.inputs.triangle = ev.keystate
                elif ev.scancode == 291:
                    self.inputs.square = ev.keystate
                elif ev.scancode == 294:
                    self.inputs.l1 = ev.keystate
                elif ev.scancode == 292:
                    self.inputs.l2 = ev.keystate
                elif ev.scancode == 298:
                    self.inputs.l3 = ev.keystate
                elif ev.scancode == 295:
                    self.inputs.r1 = ev.keystate
                elif ev.scancode == 293:
                    self.inputs.r2 = ev.keystate
                elif ev.scancode == 299:
                    self.inputs.r3 = ev.keystate
                elif ev.scancode == 296:
                    self.inputs.select = ev.keystate
                elif ev.scancode == 297:
                    self.inputs.start = ev.keystate


            elif event.type == evdev.ecodes.EV_ABS:
                ev = evdev.categorize(event)
                # print(ev.event.code, ev.event.value)

                if ev.event.code == 16:
                    if ev.event.value > 0:
                        self.inputs.right = 1
                        self.inputs.left  = 0
                    elif ev.event.value < 0:
                        self.inputs.right = 0
                        self.inputs.left  = 1
                    else:
                        self.inputs.right = 0
                        self.inputs.left  = 0
                elif ev.event.code == 17:
                    if ev.event.value > 0:
                        self.inputs.down    = 1
                        self.inputs.up      = 0
                    elif ev.event.value < 0:
                        self.inputs.down    = 0
                        self.inputs.up      = 1
                    else:
                        self.inputs.down    = 0
                        self.inputs.up      = 0
                elif ev.event.code == 0:
                    self.inputs.joy_l_x = ev.event.value
                elif ev.event.code == 1:
                    self.inputs.joy_l_y = ev.event.value
                elif ev.event.code == 5:
                    self.inputs.joy_r_x = ev.event.value
                elif ev.event.code == 2:
                    self.inputs.joy_r_y = ev.event.value

    def to_gym(self):
        go_forward  = 1.0 if self.inputs.circle > 0 else -1.0
        go_backward = 1.0 if self.inputs.cross > 0 else -1.0
        look_backward = 1.0 if self.inputs.triangle > 0 else -1.0
        throw_horn = 1.0 if (self.inputs.l1 > 0) or (self.inputs.l2 > 0) else -1.0
        bump_drift = 1.0 if (self.inputs.r1 > 0) or (self.inputs.r2 > 0) else -1.0
        go_x_direction = ((self.inputs.joy_l_x - 128.0) / 256.0) * 2.0
        go_y_direction = ((self.inputs.joy_l_y - 128.0) / 256.0) * 2.0
        return [go_forward, go_backward, look_backward, throw_horn, bump_drift, go_x_direction, go_y_direction]

    def __del__(self):
        self._active = False


if __name__=="__main__":
    joystic = JoysticPS2("/dev/input/by-id/usb-0810_USB_Gamepad-event-joystick")

    while True:
        # print(joystic.inputs.__dict__)
        print(joystic.to_gym())
        time.sleep(1/10)
