import paho.mqtt.client as mqtt
import subprocess
import threading
import psutil
import signal
import time
import os


class ServerInstance:
    '''
    Launch an instance of the game via the targeted MQTT.
    The game configuration and data will be published as "Mario_Kart_8/{instance_id}".
    A watchog will be set up to protect the system from an unwanted crash of the game emulator.
    This is useful for training an instance without having to worry about its state.
    The instance should be run with "launch()" (which is blocking until the end of the instance).
    '''

    def __init__(self, instance_id="00000000", mqtt_host="192.168.27.66", mqtt_port=1883, training=True, watchdog_timeout=120):
        '''
        Instanciate one server instance.
        Parameters:
            instance_id (str): The id of the instance that will be used to create the MQTT topic.
            mqtt_host (str): IPv4 address of the MQTT server.
            mqtt_port (int): TCP/IP Port of the MQTT server.
            training (bool): Indicate if the server should be run in training mode or not.
            watchdog_timeout (float): The watchdog will trigger if no activity was observed on the MQTT after the watchdog_timeout in seconds.
        Returns:
            An "ServerInstance" in waiting state.
        '''
        self.instance_id        = instance_id
        self.mqtt_host          = mqtt_host
        self.mqtt_port          = mqtt_port
        self.training           = training
        self.watchdog_timeout   = watchdog_timeout

        # Setup an MQTT client and setup callback
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_connect
        self.mqtt_client.on_message = self._on_message
        self.mqtt_client.connect(mqtt_host, mqtt_port, 60)
        self.mqtt_client.loop_start()

        # Use monotonic instead of time to get robustness against system time change
        self.last_activity = time.monotonic()

        # Start watchdog
        self._watchdog = threading.Thread(target=self._task_watchdog)
        self._watchdog.start()


    def _on_connect(self, client, userdata, flags, rc):
        # The watchdog observe this topic
        client.subscribe("Mario_Kart_8/"+self.instance_id+"/step")
        client.subscribe("Mario_Kart_8/"+self.instance_id+"/step/+")
        client.subscribe("Mario_Kart_8/"+self.instance_id+"/status")
        client.subscribe("Mario_Kart_8/"+self.instance_id+"/status/+")


    def _on_message(self, client, userdata, msg):
        self.last_activity = time.monotonic()
    

    def _task_watchdog(self):
        # The watchdog retrieves the PID of the server instance and all the PIDs of the server's children.
        # If the watchdog is triggered, all PIDs will be SIGKILLed.
        childs_trace = set()

        while True:

            pid = psutil.Process()
            childs_trace = childs_trace | set(pid.children(recursive=True))

            if (time.monotonic() - self.last_activity) > self.watchdog_timeout:
                try:
                    for child_proc in childs_trace:
                        print("Killing {}".format(child_proc.pid))
                        try:
                            os.kill(child_proc.pid, signal.SIGKILL)
                            continue
                        except:
                            pass
                except:
                    pass
            
            time.sleep(5.0)


    def launch(self):
        '''
        Launch the server instance and block execution until the server is terminated.
        '''
        env = os.environ.copy()
        env['INSTANCE_ID']  = self.instance_id
        env['MQTT_HOST']    = self.mqtt_host
        env['MQTT_PORT']    = str(self.mqtt_port)
        env['SERVER_MODE']  = '0' if self.training else '1'
        env['ENV_PATH']     = env['PWD']
        cmd = [
            "../rsrc/aarch64-zephyr-elf/bin/aarch64-zephyr-elf-gdb-py",
            "--batch",
            "-x",
            "server.py"
            ]
        self.last_activity = time.time()
        self._proc_server = subprocess.Popen(cmd, env=env)
        self._proc_server.wait()


if __name__ == "__main__":
    # Usage example
    instance = ServerInstance(instance_id="00000000", mqtt_host="127.0.0.1", mqtt_port=1883)
    # instance = ServerInstance(instance_id="01234567", mqtt_host="192.168.27.66", mqtt_port=1883, training=False)

    while True:
        print("Staring server instance...")
        instance.launch()
        print("Server instance was closed.")
        time.sleep(1.0)
