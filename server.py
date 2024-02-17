import sys
import os

sys.path.append(os.environ.copy()['ENV_PATH'])

from platform_specific import Controller, Monitor
import paho.mqtt.client as mqtt
import numpy as np
import subprocess
import threading
import common
import struct
import random
import enum
import time
import gdb


class SanityCheckException(Exception):
    '''
    This Exception should be raised if there is an issue with the datas provided by the game.
    '''
    pass


class AddressItem:
    '''
    Interface used to know the size and the data type of an particular address.
    '''
    def __init__(self, address, byte_size, rep_fmt):
        self.address    = address
        self.byte_size  = byte_size
        self.rep_fmt    = rep_fmt


class TimerWatchpoint(gdb.Breakpoint):
    '''
    GDB breakpoint triggered on the game timer write.
    Serve as base timer to be sync with the game.
    '''

    class Mode(enum.IntEnum):
        SAMPLER     = 0 # Sample without pausing the game
        STEPPER     = 1 # Pause the game untile continue
        SPEED_INIT  = 2 # Used to get the current race instance pointer

    def __init__(self, addr_timer, addr_items):
        super().__init__("(*{})".format(hex(addr_timer)), gdb.BP_WATCHPOINT, gdb.WP_WRITE, internal=False)
        #
        self.process            = gdb.inferiors()[0]
        self.addr_timer         = addr_timer
        self.addr_items         = addr_items
        self._lock_results      = threading.Lock()
        self._results           = {}
        self.mode               = TimerWatchpoint.Mode.SAMPLER
        self.step_size          = 6 # 1 tick equal ~16.7ms (60fps)
        self._ref_time          = 0
        self._sync              = threading.Event()
        self._speed_bp          = SpeedBreakpoint()

    def set_mode(self, mode):
        if mode == TimerWatchpoint.Mode.SAMPLER:
            self.mode = TimerWatchpoint.Mode.SAMPLER
        elif mode == TimerWatchpoint.Mode.STEPPER:
            self.mode = TimerWatchpoint.Mode.STEPPER
            self._ref_time = 0
        elif mode == TimerWatchpoint.Mode.SPEED_INIT:
            self._speed_bp.free()
            self.mode = TimerWatchpoint.Mode.SPEED_INIT

    def speed_init_done(self):
        return self._speed_bp.has_results()

    def get_speed_results(self):
        return self._speed_bp.get_player_one_addr_speed()

    def stop(self):
        try:
            with self._lock_results:
                for item in self.addr_items:
                    data  = self.process.read_memory(item.address, item.byte_size)
                    value = struct.unpack(item.rep_fmt, bytes(data))[0]
                    self._results[item.address] = value
            if self.mode == TimerWatchpoint.Mode.STEPPER:
                if (self._results[self.addr_timer] - self._ref_time) >= self.step_size:
                    self._ref_time = self._results[self.addr_timer]
                    # return True # Slower, use Event() instead
                    self._sync.clear()
                    self._sync.wait()
            if self.mode == TimerWatchpoint.Mode.SPEED_INIT:
                if not self._speed_bp.busy:
                    self._speed_bp.go()
        except:
            pass
        return False

    def get_results(self):
        with self._lock_results:
            return self._results.copy()


class SpeedBreakpoint(gdb.Breakpoint):
    '''
    GDB breakpoint used to grab race instance pointer.
    The instance contain players list and all their stats.
    '''

    def __init__(self):
        super().__init__("*0x00386278", gdb.BP_BREAKPOINT, internal=False)
        self.enabled    = False
        self._lock      = threading.Lock()
        self.players    = [] #lis of ptr to all players stats
        self.busy       = False

    def free(self):
        with self._lock:
            self.players.clear()
        self.busy = False

    def go(self):
        if not self.busy:
            with self._lock:
                self.players.clear()
            self.enabled = True
            self.busy = True
    
    def has_results(self):
        with self._lock:
            return len(self.players) == 12

    def get_player_one_addr_speed(self):
        with self._lock:
            return min(self.players) + 804

    def stop(self):
        data = gdb.parse_and_eval("$r4")
        addr = int(data)
        with self._lock:
            if addr not in self.players:
                self.players.append(addr)
            if len(self.players) == 12:
                self.enabled = False
        return False


class GameDebugger(threading.Thread):
    '''
    ARM Debugger used in conjonction with the Yuzu GDB stub to get access of raw states of the game without the need of reading the screen.
    In principle the debugger is an necessity only in training mode.
    '''

    class SceneID(enum.IntEnum):
        '''
        The SceneID encode the main state of the game.
        '''
        TITLE_SCREEN = 0x8C7CE150
        MAIN_MENU = 0x8C819B54
        LOADING = 0x00000000
        RACE = 0x8E51B158
        RACE_AFTER_PAUSE = 0x8EA36604
        SOLO_MENU = 0x8C90E870
        PRIZE_CC = 0x8C9135EC
        PLAYER_SELECTION = 0x8CA467A8
        PLAYER_ALT_SELECTION = 0x8C9CC7F0
        CAR_SELECTION = 0x8CABCB54
        PRIZE_TRACK_SELECTION = 0x8CB53EA8
        GO_VALIDATION = 0x8CC9AA68
        RACE_RULE_SELECTION = 0x8CAC9508
        RACE_TRACK_SELECTION = 0x8CB7FE00
        CINEMATIC_INTRO_RACE = 0x8E77EE74
        PAUSE_MENU = 0x8E7FB12C
        QUIT_VALIDATION = 0x875B4364
        RACE_RESULT = 0x8E74212C
        RACE_END_MENU = 0x8E991F14

    def __init__(self):
        super().__init__()
        # Connect to the GDB stub
        gdb.execute("target remote 127.0.0.1:6543")
        # Delete all breakpoints
        gdb.execute("d")
        # Register all memory address
        self.addr_dict = {
            'scene_id'              : AddressItem(0x846cb88c, 4, 'i'),
            'pause_menu_idx'        : AddressItem(0x84c38764, 4, 'i'),
            'quit_menu_idx'         : AddressItem(0x84c38124, 4, 'i'),
            'main_menu_idx'         : AddressItem(0x84c382c4, 4, 'i'),
            'solo_menu_idx'         : AddressItem(0x84c382e4, 4, 'i'),
            'race_end_menu_idx'     : AddressItem(0x84c38794, 4, 'i'),
            'player_menu_idx'       : AddressItem(0x84c38374, 4, 'i'),
            'player_alt_menu_idx'   : AddressItem(0x8c9e6974, 4, 'i'),
            'car_body_idx'          : AddressItem(0x8cabd37c, 4, 'i'),
            'car_wheel_idx'         : AddressItem(0x8cabde2c, 4, 'i'),
            'car_wing_idx'          : AddressItem(0x8cabe7ac, 4, 'i'),
            'car_menu_idx'          : AddressItem(0x84c383a4, 4, 'i'),
            'rule_menu_idx'         : AddressItem(0x87665654, 4, 'i'),
            'track_cup_sel_idx'     : AddressItem(0x84c38404, 1, 'B'),
            'race_rule_cc'          : AddressItem(0x84db2790, 1, 'B'),
            'race_rule_team'        : AddressItem(0x84db276c, 1, 'B'),
            'race_rule_item'        : AddressItem(0x84db277c, 1, 'B'),
            'race_rule_ai'          : AddressItem(0x84db2798, 1, 'B'),
            'race_rule_car_ai'      : AddressItem(0x84db27ac, 1, 'B'),
            'race_rule_track'       : AddressItem(0x84db27c0, 1, 'B'),
            'race_rule_num'         : AddressItem(0x84db27c8, 1, 'B'),
            'timer'                 : AddressItem(0x96afe398, 4, 'i'),
            'speed'                 : AddressItem(0x96bfade8, 4, 'f'),
            'coins'                 : AddressItem(0x96bf4ac4, 4, 'i'),
            'status'                : AddressItem(0x96bf4ab0, 4, 'i'),
            'rank'                  : AddressItem(0x96bf4ab4, 4, 'i'),
            'lap_continuous'        : AddressItem(0x80cc172c, 4, 'f'),
            'lap_discrete'          : AddressItem(0x8e697f8d, 1, 'B'),
            'pos_x'                 : AddressItem(0x96af34d4, 4, 'f'),
            'pos_y'                 : AddressItem(0x96af34d8, 4, 'f'),
            'pos_z'                 : AddressItem(0x96af34dc, 4, 'f'),
            'towing'                : AddressItem(0x954def14, 1, 'B'),#0 if in towing else 154 (do not use for the reward)
            'track'                 : AddressItem(0x84cc187c, 4, 'i'),#start @ 1401
        }
        # Will contain the main breakpoint to be sync with the game 
        self.watch = None
        # If true the debugger will stop
        self.terminate = False

    def run(self):
        self.watch = TimerWatchpoint(self.addr_dict['timer'].address, list(self.addr_dict.values()))
        # Keep the game running
        while not self.terminate:
            try:
                gdb.execute("continue")
                print("INTERRUPTED")
            except gdb.error as e:
                print(e)
                time.sleep(1.0)

    def _map_player_one_speed(self):
        bak_mode = self.watch.mode
        self.watch.set_mode(TimerWatchpoint.Mode.SPEED_INIT)
        while True:
            if self.watch.speed_init_done():
                break
            time.sleep(0.1)
        addr = self.watch.get_speed_results()
        self.addr_dict['speed'].address = addr
        self.watch.set_mode(bak_mode)

    def set_mode(self, mode):
        self.watch.set_mode(mode)
        if mode == TimerWatchpoint.Mode.SAMPLER:
            self.watch._sync.set()

    def step_finished(self):
        return not self.watch._sync.is_set()

    def validate_step(self):
        self.watch._sync.set()

    # def delete_breakpoint(self):
    #     gdb.execute("interrupt")

    def init_race(self):
        self._map_player_one_speed()

    def print(self):
        if self.watch is None:
            return
        print("*"*64)
        results = self.watch.get_results()
        for k,v in self.addr_dict.items():
            if v.address in results:
                if k == 'scene_id':
                    value = "{}, 0x{}".format(hex(results[v.address]), results[v.address].to_bytes(4, byteorder='big', signed=True).hex().upper())
                else:
                    value = results[v.address]
                print("{:20s} : {}".format(k, value))


class MK8_Helper:
    '''
    Mario Kart 8 Helper.
    Provide serval interfaces to easly interact with the game.
    '''

    def __init__(self, debugger, monitor, controller):
        '''
        Instanciate an MK8_Helper.
        Parameters:
            debugger (GameDebugger): The game debugger to get access to the internal game states.
            monitor (Monitor): Monitor to get game screenshot.
            controller (Controller): The controller to interact with the game.
        Returns:
            An "MK8_Helper" object.
        '''
        self.debugger   = debugger
        self.monitor    = monitor
        self.controller = controller

    def read_debugger_value(self, key):
        '''
        Get memory value from the debugger.
        Parameters:
            key (str): On of the registered key in the debugger.
        Returns:
            The lowlevel value wich the type depend on the registered item.
        '''
        addr = self.debugger.addr_dict[key].address
        while True:
            results = self.debugger.watch.get_results()
            if addr in results:
                return results[addr]
            time.sleep(0.1)

    def get_current_scene(self):
        '''
        Get current main state (aka scene) of the game.
        Returns:
            An GameDebugger.SceneID (aka int)
        '''
        value = self.read_debugger_value('scene_id')
        dword = value.to_bytes(4, byteorder='big', signed=True)
        return int.from_bytes(dword, 'big')

    def setup_race(self, game_setup):
        '''
        This function will execute an state machine that will take the controler to setup the game race according to the parameter.
        Parameters:
            game_setup (dict): An dict representing the wanted game state in format:
                - MAIN_MODE                = common.GameSetup.MainMenu.<value>
                - GAME_MODE                = common.GameSetup.GameMode.<value>
                - PLAYER                   = common.GameSetup.Player.<value>
                - PLAYER_VARIANT           = common.GameSetup.Player.<value>.<value>
                - CAR_BODY                 = common.GameSetup.Car.Body.<value>
                - CAR_WHEEL                = common.GameSetup.Car.Wheel.<value>
                - CAR_WING                 = common.GameSetup.Car.Wing.<value>
                - RACE_RULE_MODE           = common.GameSetup.RaceRule.Mode.<value>
                - RACE_RULE_TEAMS          = common.GameSetup.RaceRule.Teams.<value>
                - RACE_RULE_ITEMS          = common.GameSetup.RaceRule.Items.<value>
                - RACE_RULE_COM            = common.GameSetup.RaceRule.COM.<value>
                - RACE_RULE_COM_VEHICLES   = common.GameSetup.RaceRule.COMVehicles.<value>
                - RACE_RULE_COURSES        = common.GameSetup.RaceRule.Courses.<value>
                - RACE_RULE_RACE_COUNT     = common.GameSetup.RaceRule.RaceCount.<value>
                - COURSE_CUP               = common.GameSetup.Course.Cup.<value>
                - COURSE                   = common.GameSetup.Course.Cup.Special.<value>
                - MAX_STEP                 = <int value> which represent max step to done before closing the game instance. 
        Returns:
            The lowlevel value wich the type depend on the registered item.
        '''
        state = "INIT"
        while True:
            # if isinstance(state, int):
            #     print(hex(state))
            # else:
            #     print(state)

            if state == "INIT":
                state = self.get_current_scene()
            
            elif state == GameDebugger.SceneID.TITLE_SCREEN:
                self.controller.instant_b()
                state = self.get_current_scene()

            elif state == GameDebugger.SceneID.MAIN_MENU:
                item_idx = self.read_debugger_value('main_menu_idx')
                if item_idx == game_setup['MAIN_MODE']:
                    self.controller.instant_b()
                else:
                    self.controller.instant_pad_down()
                state = self.get_current_scene()
            
            elif state == GameDebugger.SceneID.SOLO_MENU:
                item_idx = self.read_debugger_value('solo_menu_idx')
                if item_idx == game_setup['GAME_MODE']:
                    self.controller.instant_b()
                else:
                    self.controller.instant_pad_down()
                state = self.get_current_scene()
            
            elif state == GameDebugger.SceneID.PLAYER_SELECTION:
                item_idx = self.read_debugger_value('player_menu_idx')
                if item_idx//7 != game_setup['PLAYER']//7:
                    self.controller.instant_pad_down()
                elif item_idx != game_setup['PLAYER']:
                    self.controller.instant_pad_right()
                else:
                    self.controller.instant_b()
                state = self.get_current_scene()
            
            elif state == GameDebugger.SceneID.PLAYER_ALT_SELECTION:
                item_idx = self.read_debugger_value('player_alt_menu_idx')
                if item_idx//3 != game_setup['PLAYER_VARIANT']//3:
                    self.controller.instant_pad_down()
                elif item_idx != game_setup['PLAYER_VARIANT']:
                    self.controller.instant_pad_right()
                else:
                    self.controller.instant_b()
                state = self.get_current_scene()

            elif state == GameDebugger.SceneID.CAR_SELECTION:
                item_idx = self.read_debugger_value('car_menu_idx')
                if item_idx == 0:
                    sub_item_idx = self.read_debugger_value('car_body_idx')
                    if sub_item_idx != game_setup['CAR_BODY']:
                        self.controller.instant_pad_down()
                    else:
                        self.controller.instant_b()
                elif item_idx == 1:
                    sub_item_idx = self.read_debugger_value('car_wheel_idx')
                    if sub_item_idx != game_setup['CAR_WHEEL']:
                        self.controller.instant_pad_down()
                    else:
                        self.controller.instant_b()
                elif item_idx == 2:
                    sub_item_idx = self.read_debugger_value('car_wing_idx')
                    if sub_item_idx != game_setup['CAR_WING']:
                        self.controller.instant_pad_down()
                    else:
                        self.controller.instant_b()
                state = self.get_current_scene()
            
            elif state == GameDebugger.SceneID.RACE_RULE_SELECTION:
                item_idx = self.read_debugger_value('rule_menu_idx')
                if item_idx == 0:
                    sub_item_idx = self.read_debugger_value('race_rule_cc')
                    if sub_item_idx != game_setup['RACE_RULE_MODE']:
                        self.controller.instant_pad_right()
                    else:
                        self.controller.instant_pad_down()
                elif item_idx == 1:
                    sub_item_idx = self.read_debugger_value('race_rule_team')
                    if sub_item_idx != game_setup['RACE_RULE_TEAMS']:
                        self.controller.instant_pad_right()
                    else:
                        self.controller.instant_pad_down()
                elif item_idx == 2:
                    sub_item_idx = self.read_debugger_value('race_rule_item')
                    if sub_item_idx != game_setup['RACE_RULE_ITEMS']:
                        self.controller.instant_pad_right()
                    else:
                        self.controller.instant_pad_down()
                elif item_idx == 3:
                    sub_item_idx = self.read_debugger_value('race_rule_ai')
                    if sub_item_idx != game_setup['RACE_RULE_COM']:
                        self.controller.instant_pad_right()
                    else:
                        self.controller.instant_pad_down()
                elif item_idx == 4:
                    sub_item_idx = self.read_debugger_value('race_rule_car_ai')
                    if sub_item_idx != game_setup['RACE_RULE_COM_VEHICLES']:
                        self.controller.instant_pad_right()
                    else:
                        self.controller.instant_pad_down()
                elif item_idx == 5:
                    sub_item_idx = self.read_debugger_value('race_rule_track')
                    if sub_item_idx != game_setup['RACE_RULE_COURSES']:
                        self.controller.instant_pad_right()
                    else:
                        self.controller.instant_pad_down()
                elif item_idx == 6:
                    sub_item_idx = self.read_debugger_value('race_rule_num')
                    if sub_item_idx != game_setup['RACE_RULE_RACE_COUNT']:
                        self.controller.instant_pad_right()
                    else:
                        self.controller.instant_b()
                state = self.get_current_scene()
            
            elif state == GameDebugger.SceneID.RACE_TRACK_SELECTION:
                item_idx = self.read_debugger_value('track_cup_sel_idx')
                if item_idx < 12:
                    if item_idx//6 != game_setup['COURSE_CUP']//6:
                        self.controller.instant_pad_down()
                    elif item_idx != game_setup['COURSE_CUP']:
                        self.controller.instant_pad_right()
                    else:
                        self.controller.instant_b()
                else:
                    if item_idx != game_setup['COURSE']:
                        self.controller.instant_pad_right()
                    else:
                        self.controller.instant_b()
                state = self.get_current_scene()

            elif state == GameDebugger.SceneID.GO_VALIDATION:
                if self.get_current_scene() == GameDebugger.SceneID.GO_VALIDATION:
                    self.controller.instant_b()
                else:
                    state = "WAIT_RACE"
            
            elif (state == GameDebugger.SceneID.RACE) or (state == GameDebugger.SceneID.RACE_AFTER_PAUSE):
                self.controller.instant_start()
                state = self.get_current_scene()

            elif state == GameDebugger.SceneID.PAUSE_MENU:
                self.controller.instant_pad_down()
                time.sleep(0.1)
                self.controller.instant_b()
                state = GameDebugger.SceneID.QUIT_VALIDATION
                # item_idx = self.read_debugger_value('pause_menu_idx')
                # if item_idx != 1:
                #     self.controller.instant_pad_down()
                # else:
                #     self.controller.instant_b()
                # state = self.get_current_scene()

            elif state == GameDebugger.SceneID.QUIT_VALIDATION:
                self.controller.instant_pad_right()
                time.sleep(0.1)
                self.controller.instant_b()
                state = "INIT"
                # item_idx = self.read_debugger_value('quit_menu_idx')
                # if item_idx != 1:
                #     self.controller.instant_pad_right()
                # else:
                #     self.controller.instant_b()
                # state = "INIT"

            elif state == GameDebugger.SceneID.RACE_RESULT:
                self.controller.instant_b()
                time.sleep(1.0)
                state = self.get_current_scene()
            
            elif state == GameDebugger.SceneID.RACE_END_MENU:
                time.sleep(1.0)
                item_idx = self.read_debugger_value('race_end_menu_idx')
                if item_idx == 2:
                    self.controller.instant_b()
                else:
                    self.controller.instant_pad_down()
                state = self.get_current_scene()
                # self.controller.instant_b()
                # state = "INIT"
            
            elif state == GameDebugger.SceneID.CINEMATIC_INTRO_RACE:
                self.controller.instant_b()
                state = "WAIT_RACE"

            # elif state == GameDebugger.SceneID.LOADING:
            #     # Solve GDB bug (?) that make the breakpoint disable (??)
            #     self.debugger.delete_breakpoint()
            #     time.sleep(1)
            #     state = "INIT"

            elif state == "WAIT_RACE":
                current_scene = self.get_current_scene()
                if current_scene == GameDebugger.SceneID.CINEMATIC_INTRO_RACE:
                    self.controller.instant_b()
                if (self.read_debugger_value('status') == 16) and ((current_scene == GameDebugger.SceneID.RACE) or (current_scene == GameDebugger.SceneID.RACE_AFTER_PAUSE)):
                    state = "READY"
                if current_scene == GameDebugger.SceneID.RACE_END_MENU:
                    state = "INIT"

            elif state == "READY":
                return

            else:
                state = "INIT"

            time.sleep(0.1)
    
    def is_race_finish(self):
        '''
        Get the race status.
        Returns:
            True if the race is finished, False otherwise.
        '''
        value = self.read_debugger_value('status')
        if (value == 16) or (value == 24):
            return False
        return True


class GameEmulator(threading.Thread):
    '''
    Represent the game emulator.
    '''
    def __init__(self, game_path):
        super().__init__()
        #
        self.game_path = game_path
        self._proc_yuzu = None
        self._proc_gdb = None

    def _yuzu_task(self):
        env = os.environ.copy()
        env['LD_LIBRARY_PATH'] = "../emulator/yuzu/usr/lib"
        cmd = [
            "../emulator/yuzu/AppRun", 
            "-g", 
            self.game_path
        ]
        self._proc_yuzu = subprocess.Popen(cmd, env=env)

    def _gdb_task(self):
        cmd = ["../rsrc/aarch64-zephyr-elf/bin/aarch64-zephyr-elf-gdb-py"]
        self._proc_gdb = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        self._proc_gdb.communicate(input="target remote 127.0.0.1:6543\ncontinue\n".encode("utf8"))

    def launch(self):
        self.task_yuzu = threading.Thread(target=self._yuzu_task)
        self.task_yuzu.start()
        time.sleep(3.0)
        self.task_gdb = threading.Thread(target=self._gdb_task)
        self.task_gdb.start()
        time.sleep(15.0)
        os.system("wmctrl -r \"yuzu Mainline\" -e 0,32,32,256,256")
        os.system("wmctrl -a \"yuzu Mainline\"")
    
    def close(self):
        try:
            self._proc_yuzu.kill()
            self._proc_yuzu.wait()
        except:
            pass
        try:
            self._proc_gdb.kill()
            self._proc_gdb.wait()
        except:
            pass


class Server(threading.Thread):
    '''
    The server is in charge of the MQTT IO.
    '''
    def __init__(self, server_callback, instance_id=None, mqtt_host="127.0.0.1", mqtt_port=1883):
        super().__init__()
        #
        self.instance_id = instance_id
        if self.instance_id is None:
            self.instance_id = random.randint(0, (2**32)-1).to_bytes(4, 'big').hex().upper()
        #
        self.mqtt = mqtt.Client()
        self.mqtt.on_connect = self._on_connect
        self.mqtt.on_message = self._on_message
        self.mqtt.will_set("Mario_Kart_8/"+self.instance_id+"/status", payload=struct.pack('B', False), qos=1, retain=True)
        self.mqtt.connect(mqtt_host, mqtt_port, 60)
        #
        self.server_callback = server_callback

    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe("Mario_Kart_8/"+self.instance_id+"/order/reset")
        client.subscribe("Mario_Kart_8/"+self.instance_id+"/order/setup/+")
        client.subscribe("Mario_Kart_8/"+self.instance_id+"/order/action")
        client.publish("Mario_Kart_8/"+self.instance_id+"/status", payload=struct.pack('B', True), qos=1, retain=True)

    def _on_message(self, client, userdata, msg):
        if msg.topic == "Mario_Kart_8/"+self.instance_id+"/order/reset":
            order = (common.Server.Order.RESET,)
            self.server_callback(client, order)
        elif msg.topic.startswith("Mario_Kart_8/"+self.instance_id+"/order/setup/"):
            key   = msg.topic.split('/')[-1]
            order = (common.Server.Order.GAME_SETUP, (key, struct.unpack('i', msg.payload)[0]))
            self.server_callback(client, order)
        elif msg.topic == "Mario_Kart_8/"+self.instance_id+"/order/action":
            go_forward      = struct.unpack('b', msg.payload[0:1])[0]
            go_backward     = struct.unpack('b', msg.payload[1:2])[0]
            go_x_direction  = struct.unpack('f', msg.payload[2:6])[0]
            set_y_direction = struct.unpack('f', msg.payload[6:10])[0]
            look_backward   = struct.unpack('b', msg.payload[10:11])[0]
            throw_horn      = struct.unpack('b', msg.payload[11:12])[0]
            bump_drift      = struct.unpack('b', msg.payload[12:13])[0]
            order = (common.Server.Order.ACTION, (go_forward, go_backward, go_x_direction, set_y_direction, look_backward, throw_horn, bump_drift))
            self.server_callback(client, order)

    def listen(self):
        self.mqtt.loop_forever()

    def run(self):
        self.listen()


class Manager:
    '''
    The manager aggregates all the above elements to produce a game instance that can be managed by MQTT.
    '''
    class Mode(enum.IntEnum):
        TRAINING    = 0
        INFERENCE   = 1

    def __init__(self, instance_id="00000000", mqtt_host="192.168.27.66", mqtt_port=1883):
        self.server     = Server(server_callback=self._receive_order, instance_id=instance_id, mqtt_host=mqtt_host, mqtt_port=mqtt_port)
        self.game       = GameEmulator(game_path="../../../game/Mario_Kart_8_Deluxe.xci")
        self.game.launch()
        self.monitor    = Monitor()
        self.controller = Controller()
        self._init_debugger()
        #
        self.game_setup = {}
        self.game_setup['MAIN_MODE']                = common.GameSetup.MainMenu.SINGLE_PLAYER
        self.game_setup['GAME_MODE']                = common.GameSetup.GameMode.VS_RACE
        self.game_setup['PLAYER']                   = common.GameSetup.Player.MASKASS
        self.game_setup['PLAYER_VARIANT']           = common.GameSetup.Player.MaskassVariant.DEFAULT
        self.game_setup['CAR_BODY']                 = common.GameSetup.Car.Body.BIDDYBUGGY
        self.game_setup['CAR_WHEEL']                = common.GameSetup.Car.Wheel.ROLLER
        self.game_setup['CAR_WING']                 = common.GameSetup.Car.Wing.CLOUD_GLIDER
        self.game_setup['RACE_RULE_MODE']           = common.GameSetup.RaceRule.Mode.CC_150
        self.game_setup['RACE_RULE_TEAMS']          = common.GameSetup.RaceRule.Teams.NO_TEAMS
        self.game_setup['RACE_RULE_ITEMS']          = common.GameSetup.RaceRule.Items.FRANTIC_ITEMS
        self.game_setup['RACE_RULE_COM']            = common.GameSetup.RaceRule.COM.HARD
        self.game_setup['RACE_RULE_COM_VEHICLES']   = common.GameSetup.RaceRule.COMVehicles.ALL
        self.game_setup['RACE_RULE_COURSES']        = common.GameSetup.RaceRule.Courses.CHOOSE
        self.game_setup['RACE_RULE_RACE_COUNT']     = common.GameSetup.RaceRule.RaceCount.FOUR
        self.game_setup['COURSE_CUP']               = common.GameSetup.Course.Cup.SPECIAL
        self.game_setup['COURSE']                   = common.GameSetup.Course.Cup.Special.RAINBOW_ROAD
        self.game_setup['MAX_STEP']                 = 1600
        #
        self.action_received = threading.Event()
        #
        self.mode = Manager.Mode.TRAINING
        #
        self.reset = True
        self.server.start()
        while self.debugger.watch is None:
            print("Waiting debugger...")
            time.sleep(1.0)
        print("Waiting debugger... OK")

    def _init_debugger(self):
        self.debugger = GameDebugger()
        self.mk8_helper = MK8_Helper(self.debugger, self.monitor, self.controller)
        self.debugger.start()

    def _publish_step_results(self):
        if self.mode == Manager.Mode.INFERENCE:
            frame   = self.monitor.get_screen_shot()
            results = self.debugger.watch.get_results()
            root    = "Mario_Kart_8/"+self.server.instance_id+"/step"
            self.server.mqtt.publish(root+"/frame"                  , payload=frame.tobytes()                                    , qos=1, retain=True)
            self.server.mqtt.publish(root+"/terminal"               , payload=struct.pack('B', self.terminal)                    , qos=1, retain=True)
            self.server.mqtt.publish(root+"/terminated_by_timeout"  , payload=struct.pack('B', self.terminated_by_timeout)       , qos=1, retain=True)
            self.server.mqtt.publish(root+"/is_race_finish"         , payload=struct.pack('B', False)                            , qos=1, retain=True)
            self.server.mqtt.publish(root, payload=struct.pack('I'  , self.step_no), qos=1, retain=True)
        elif self.mode == Manager.Mode.TRAINING:
            frame   = self.monitor.get_screen_shot()
            results = self.debugger.watch.get_results()
            root    = "Mario_Kart_8/"+self.server.instance_id+"/step"
            self.server.mqtt.publish(root+"/frame"                  , payload=frame.tobytes()                                    , qos=1, retain=True)
            self.server.mqtt.publish(root+"/terminal"               , payload=struct.pack('B', self.terminal)                    , qos=1, retain=True)
            self.server.mqtt.publish(root+"/terminated_by_timeout"  , payload=struct.pack('B', self.terminated_by_timeout)       , qos=1, retain=True)
            self.server.mqtt.publish(root+"/is_race_finish"         , payload=struct.pack('B', self.mk8_helper.is_race_finish()) , qos=1, retain=True)
            for key in ('timer', 'speed', 'coins', 'status', 'rank', 'lap_continuous', 'lap_discrete', 'pos_x', 'pos_y', 'pos_z', 'towing', 'track'):
                value = results[self.debugger.addr_dict[key].address]
                self.server.mqtt.publish(root+"/"+key, payload=struct.pack(self.debugger.addr_dict[key].rep_fmt, value), qos=1, retain=True)
            self.server.mqtt.publish(root, payload=struct.pack('I', self.step_no), qos=1, retain=True)

    def _receive_order(self, client, order):
        if order[0] == common.Server.Order.RESET:
            self.reset = True
            self.action_received.set()
        elif order[0] == common.Server.Order.GAME_SETUP:
            try:
                self.game_setup[order[1][0]] = order[1][1]
            except KeyError:
                print("Unknow gamesetup key '{}'".format(order[1]))
        elif order[0] == common.Server.Order.ACTION:
            if order[1][0] != 0:
                self.controller.go_forward()
            if order[1][1] != 0:
                self.controller.go_backward()
            self.controller.go_x_direction(order[1][2])
            self.controller.set_y_direction(order[1][3])
            if order[1][4] != 0:
                self.controller.look_backward()
            if order[1][5] != 0:
                self.controller.throw_horn()
            if order[1][6] != 0:
                self.controller.bump_drift()
            self.controller.apply()
            self.action_received.set()
        else:
            print("Unknow order {}".format(order))

    def _wait_action(self):
        print("wait...")
        self.server.mqtt.publish("Mario_Kart_8/"+self.server.instance_id+"/status/waiting_for_action", payload=struct.pack('B', True), qos=1, retain=True)
        self.action_received.wait()
        self.action_received.clear()
        self.server.mqtt.publish("Mario_Kart_8/"+self.server.instance_id+"/status/waiting_for_action", payload=struct.pack('B', False), qos=1, retain=True)
        print("wait... OK")

    def _standarize_img(self, img):
        img = img.astype(np.float32)
        return (img - np.mean(img)) / np.std(img)

    def _img_invariant_transformation(self, img):
        # TODO mask players with an patch
        morph = (img.astype(np.float32) + np.flip(img, axis=1).astype(np.float32))/2.0
        return self._standarize_img(morph)

    def _match_track(self, img, fail_ths=0.9):
        mag = self._img_invariant_transformation(img)
        ref_files   = os.listdir("../datas/img")
        scores      = np.zeros(len(ref_files))
        for idx, ref_file in enumerate(ref_files):
            ref_data    = np.load(os.path.join("../datas/img", ref_file))
            ref_mag     = self._img_invariant_transformation(ref_data)
            scores[idx] = np.sum(ref_mag * mag) / (128*128*3)        
        idx = np.argmax(scores)
        if scores[idx] < fail_ths:
            raise Exception("Match failed")
        code = ref_files[idx]
        code = code.split('.')[0]
        code = int(code.split('_')[0])
        track = common.INTERNAL_TRACK_TO_ENUM[code]
        return track

    def _sanity_check(self):
        frame = self.monitor.get_screen_shot()
        try:
            # Sometime the emulator produce an bugged rendering. This function perform check on the RGB image to prevent that.
            track = self._match_track(frame)
        except:
            # dir = os.listdir("./anomaly")
            # np.save("./anomaly/record_{}".format(len(dir)), frame)
            raise SanityCheckException("Cannot recognize track from image.")
        if self.game_setup['RACE_RULE_COURSES'] == common.GameSetup.RaceRule.Courses.CHOOSE:
            if self.game_setup['COURSE_CUP'] != common.INTERNAL_TRACK_TO_CUP[track]:
                raise SanityCheckException("Current cup does not match the choosen cup.")
            if self.game_setup['COURSE'] != common.INTERNAL_TRACK_TO_TRACK[track]:
                raise SanityCheckException("Current track does not match the choosen track.")

    def init_game(self):
        self.server.mqtt.publish("Mario_Kart_8/"+self.server.instance_id+"/status/initializing_game", payload=struct.pack('B', True), qos=1, retain=True)
        self.debugger.set_mode(TimerWatchpoint.Mode.SAMPLER)
        self.mk8_helper.setup_race(self.game_setup)
        # self._sanity_check()
        self.server.mqtt.publish("Mario_Kart_8/"+self.server.instance_id+"/status/initializing_game", payload=struct.pack('B', False), qos=1, retain=True)

    def in_game(self):
        self.terminal = False
        self.step_no = 0
        self.action_received.clear()
        self.terminated_by_timeout = False
        self.reset = False

        if self.mode == Manager.Mode.INFERENCE:
            _last_time = 0

            self.debugger.set_mode(TimerWatchpoint.Mode.SAMPLER)
            self.server.mqtt.publish("Mario_Kart_8/"+self.server.instance_id+"/status/playing_game", payload=struct.pack('B', True), qos=1, retain=True)
            while True:
                self._publish_step_results()
                self._wait_action()
                self.step_no += 1
                # Timeout
                if self.step_no >= self.game_setup['MAX_STEP']:
                    self.terminated_by_timeout = True
                    break
                if self.reset:
                    break
                dt = 0.1-(time.time()-_last_time)
                time.sleep(max(0, dt))
                _last_time = time.time()
            self.terminal = True
            self._publish_step_results()
            self.debugger.set_mode(TimerWatchpoint.Mode.SAMPLER)
            self.server.mqtt.publish("Mario_Kart_8/"+self.server.instance_id+"/status/playing_game", payload=struct.pack('B', False), qos=1, retain=True)


        elif self.mode == Manager.Mode.TRAINING:
            self.server.mqtt.publish("Mario_Kart_8/"+self.server.instance_id+"/status/playing_game", payload=struct.pack('B', True), qos=1, retain=True)
            self.debugger.set_mode(TimerWatchpoint.Mode.STEPPER)
            while not self.mk8_helper.is_race_finish():
                if self.debugger.step_finished():
                    self._publish_step_results()
                    self._wait_action()
                    self.debugger.validate_step()
                    self.step_no += 1
                    # Timeout
                    if self.step_no >= self.game_setup['MAX_STEP']:
                        self.terminated_by_timeout = True
                        break
                    if self.reset:
                        break
                time.sleep(1/30)
            self.terminal = True
            self._publish_step_results()
            self.debugger.set_mode(TimerWatchpoint.Mode.SAMPLER)
            self.server.mqtt.publish("Mario_Kart_8/"+self.server.instance_id+"/status/playing_game", payload=struct.pack('B', False), qos=1, retain=True)

    def set_mode(self, mode):
        self.mode = mode

    def loop(self):
        while True:
            print("Waiting reset order...")
            while self.reset == False:
                time.sleep(1/10)
            print("Waiting reset order... OK")
            print("Creating game instance...")
            try:
                self.init_game()
            except SanityCheckException as e:
                self.debugger.terminate = True
                self.game.close()
                self.game.launch()
                self._init_debugger()
                print("Creating game instance... FAIL ({})".format(e))
                continue
            print("Creating game instance... OK")
            print("Playing...")
            self.in_game()
            print("Playing... OK")


if __name__ == "__main__":
    manager = Manager(instance_id=os.environ['INSTANCE_ID'], mqtt_host=os.environ['MQTT_HOST'], mqtt_port=int(os.environ['MQTT_PORT']))
    manager.set_mode(int(os.environ['SERVER_MODE']))
    manager.loop()
