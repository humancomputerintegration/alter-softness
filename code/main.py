import sys
import math
import time
import struct
import serial


import numpy as np
import matplotlib.pyplot as plt

import utils
from pid_controller import PIDController
from arduino_controller import ArduinoController

PORT = "/dev/cu.usbmodem14101"
DEVICE = 0


def main():
    controller = ArduinoController(PORT)
    PID = PIDController(P=1.3, I=0.004, D=7)
    fsr_target = int(sys.argv[1])

    i = 0
    while i < 100:
        run_pid(controller, PID, fsr_target)
        print(i)
        i = i + 1
    if i >= 50:
        controller.run_motor(DEVICE, 1, 0)


def run_pid(controller, PID, fsr_target):
    PID.set_target(fsr_target)
    # while True:
    fsr = controller.read_fsr(DEVICE)
    print("FSR:" + str(fsr))

    pid_output = PID.step(fsr)
    speed = utils.calculate_speed(pid_output)
    print("PID:" + str(pid_output))

    error_margin = 5
    if pid_output < error_margin and pid_output > -(error_margin):
        speed = 0
        controller.run_motor(DEVICE, 1, speed)
    elif pid_output < -error_margin:
        controller.run_motor(DEVICE, 1, speed)
    else:
        controller.run_motor(DEVICE, 0, speed)

    time.sleep(0.01)


if __name__ == "__main__":
    main()
