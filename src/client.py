import paho.mqtt.client as mqtt
import numpy as np
import threading
import struct
import time


class Client(threading.Thread):
    '''
    Client to be used to communicate with the server via MQTT.
    '''

    def __init__(self, host, port, target_id):
        '''
        Instanciate one client instance.
        Call "start()" to connect the client.
        Parameters:
            host (str): IPv4 address of the MQTT server.
            port (int): TCP/IP Port of the MQTT server.
            target_id (str): The id of the instance used to create the MQTT topic.
        Returns:
            An "Client" waiting to start.
        '''
        super().__init__()
        #
        self.isReady = threading.Event()
        self.isReady.clear()
        self.target_id = target_id
        self.mqtt = mqtt.Client()
        self.mqtt.on_connect = self._on_connect
        self.mqtt.on_message = self._on_message
        self.mqtt.connect(host, port, 60)
        #
        self.step_no = None
        self.step_frame = None
        self.step_timer = None
        self.step_speed = None
        self.step_coins = None
        self.step_status = None
        self.step_rank = None
        self.step_lap_continuous = None
        self.step_lap_discrete = None
        self.step_pos_x = None
        self.step_pos_y = None
        self.step_pos_z = None
        self.step_towing = None
        self.step_track = None
        self.step_terminal = None
        self.step_terminated_by_timeout = None
        self.step_is_race_finish = None
        self.status = None
        self.status_waiting_for_action = None
        self.status_initializing_game = None
        self.status_playing_game = None
        #
        self._last_step = None
        self._event_new_step = threading.Event()
        self._event_new_step.clear()

    def _on_connect(self, client, userdata, flags, rc):
        client.subscribe("Mario_Kart_8/"+self.target_id+"/step")
        client.subscribe("Mario_Kart_8/"+self.target_id+"/step/+")
        client.subscribe("Mario_Kart_8/"+self.target_id+"/status")
        client.subscribe("Mario_Kart_8/"+self.target_id+"/status/+")

    def _on_message(self, client, userdata, msg):
        if msg.topic == "Mario_Kart_8/"+self.target_id+"/step":
            self.step_no = struct.unpack('I', msg.payload)[0]
            if self._last_step != self.step_no:
                self._last_step = self.step_no
                self._event_new_step.set()

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/timer":
            self.step_timer = struct.unpack('i', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/speed":
            self.step_speed = struct.unpack('f', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/coins":
            self.step_coins = struct.unpack('i', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/status":
            self.step_status = struct.unpack('i', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/rank":
            self.step_rank = struct.unpack('i', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/lap_continuous":
            self.step_lap_continuous = struct.unpack('f', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/lap_discrete":
            self.step_lap_discrete = struct.unpack('B', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/pos_x":
            self.step_pos_x = struct.unpack('f', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/pos_y":
            self.step_pos_y = struct.unpack('f', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/pos_z":
            self.step_pos_z = struct.unpack('f', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/towing":
            self.step_towing = struct.unpack('B', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/track":
            self.step_track = struct.unpack('i', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/frame":
            image           = np.frombuffer(msg.payload, dtype=np.uint8)
            image           = np.reshape(image, (128, 128, 3))
            self.step_frame = image

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/terminal":
            self.step_terminal = struct.unpack('B', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/terminated_by_timeout":
            self.step_terminated_by_timeout = struct.unpack('B', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/step/is_race_finish":
            self.step_is_race_finish = struct.unpack('B', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/status":
            self.status = struct.unpack('B', msg.payload)[0]
            if self.status == True:
                self.isReady.set()

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/status/waiting_for_action":
            self.status_waiting_for_action = struct.unpack('B', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/status/initializing_game":
            self.status_initializing_game = struct.unpack('B', msg.payload)[0]

        elif msg.topic == "Mario_Kart_8/"+self.target_id+"/status/playing_game":
            self.status_playing_game = struct.unpack('B', msg.payload)[0]

    def _encode_action(self, go_forward, go_backward, go_x_direction, set_y_direction, look_backward, throw_horn, bump_drift):
        payload = bytes()
        payload += struct.pack('b', go_forward)
        payload += struct.pack('b', go_backward)
        payload += struct.pack('f', go_x_direction)
        payload += struct.pack('f', set_y_direction)
        payload += struct.pack('b', look_backward)
        payload += struct.pack('b', throw_horn)
        payload += struct.pack('b', bump_drift)
        return payload

    def reset_game(self):
        '''
        Send an reset order to the game.
        This will block the execution until the reset was done.
        '''
        if self.status != True:
            raise RuntimeError("Server seem to be dead.")
        #
        self.mqtt.publish("Mario_Kart_8/"+self.target_id+"/order/reset", payload=None, qos=1, retain=False)
        #
        while not self.status_initializing_game:
            time.sleep(0.1)
        self._event_new_step.clear()
        self._event_new_step.wait()

    def action_game(self, go_forward, go_backward, go_x_direction, set_y_direction, look_backward, throw_horn, bump_drift):
        '''
        Send an reset action to the game.
        This will block the execution until the action was done.
        Parameters:
            go_forward (bool): Activates or deactivates the controller button used to move forward.
            go_backward (bool): Activates or deactivates the controller button used to move backward.
            go_x_direction (float): Move the controller joystick on X axis. Range [-1.0; 1.0].
            set_y_direction (float): Move the controller joystick on Y axis. Range [-1.0; 1.0].
            look_backward (bool): Activates or deactivates the controller button used to look backward.
            throw_horn (bool): Activates or deactivates the controller button used to horn/throw.
            bump_drift (bool): Activates or deactivates the controller button used to bump/drift.
        '''
        if self.status != True:
            raise RuntimeError("Server seem to be dead.")
        #
        while not self.status_waiting_for_action:
            time.sleep(1/100)
        #
        datas = self._encode_action(go_forward, go_backward, go_x_direction, set_y_direction, look_backward, throw_horn, bump_drift)
        self._event_new_step.clear()
        self.mqtt.publish("Mario_Kart_8/"+self.target_id+"/order/action", payload=datas, qos=1, retain=False)
        self._event_new_step.wait()

    def setup_game(self, game_setup):
        '''
        Send the game setup.
        This will take effect when a new game will be created.
        Parameters:
            go_forward (bool): Activates or deactivates the controller button used to move forward.
            go_backward (bool): Activates or deactivates the controller button used to move backward.
            go_x_direction (float): Move the controller joystick on X axis. Range [-1.0; 1.0].
            set_y_direction (float): Move the controller joystick on Y axis. Range [-1.0; 1.0].
            look_backward (bool): Activates or deactivates the controller button used to look backward.
            throw_horn (bool): Activates or deactivates the controller button used to horn/throw.
            bump_drift (bool): Activates or deactivates the controller button used to bump/drift.
        '''
        if self.status != True:
            raise RuntimeError("Server seem to be dead.")
        #
        for k,v in game_setup.items():
            self.mqtt.publish("Mario_Kart_8/"+self.target_id+"/order/setup/{}".format(k), payload=struct.pack('i', v), qos=1, retain=True)

    def _connection_loop(self):
        self.mqtt.loop_forever()

    def run(self):
        self._connection_loop()


# if __name__ == "__main__":
#     client = Client("192.168.27.66", 1883, "00000000")
#     client.start()
#     time.sleep(3.0)
#     client.mqtt.publish("Mario_Kart_8/"+client.target_id+"/order/reset", payload=None, qos=1, retain=False)