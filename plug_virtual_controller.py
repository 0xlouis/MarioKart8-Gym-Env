import time

import sys
sys.path.append("../../src/")

from platform_specific import Controller

controller = Controller()

print("press ctr+c to quit.")

while True:
    controller.instant_a()
    time.sleep(1/4)