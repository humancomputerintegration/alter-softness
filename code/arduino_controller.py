from pyfirmata import ArduinoMega, util
import pyfirmata
import time
import math


class ArduinoController:
    def __init__(self, port):
        print("connecting")
        self.board = ArduinoMega(port)
        self.it = util.Iterator(self.board)
        self.it.start()
        self.board.add_cmd_handler(
            pyfirmata.pyfirmata.STRING_DATA, self._message_handler
        )

        # Get Motor Pin
        self.stand_by = self.board.get_pin("d:10:p")
        self.ain_1 = self.board.get_pin("d:9:p")
        self.ain_2 = self.board.get_pin("d:8:p")
        self.pwm_a = self.board.get_pin("d:3:p")

        self.bin_1 = self.board.get_pin("d:12:p")
        self.bin_2 = self.board.get_pin("d:11:p")
        self.pwm_b = self.board.get_pin("d:5:p")

        # Get FSR Pin
        self.fsr_0 = self.board.get_pin("a:0:i")
        self.fsr_1 = self.board.get_pin("a:1:i")

        print("connected")
        self.state = 0

    def disconnect(self):
        self.board.exit()

    def _message_handler(self, *args, **kwargs):
        msg = int(util.two_byte_iter_to_str(args))
        self.state = int(msg)

    def run_motor(self, index, dir, speed):
        self.stand_by.write(1)

        if dir == 1:
            dir_pin_1 = 1
            dir_pin_2 = 0
        else:
            dir_pin_1 = 0
            dir_pin_2 = 1

        if index == 1:
            a = 1
            self.ain_1.write(dir_pin_1)
            self.ain_2.write(dir_pin_2)
            self.pwm_a.write(speed)
        else:
            self.bin_1.write(dir_pin_1)
            self.bin_2.write(dir_pin_2)
            self.pwm_b.write(speed)

    def read_fsr(self, index):
        if index == 0:
            readings = self.fsr_0.read()
        else:
            readings = self.fsr_1.read()

        if readings != None and readings != 0:
            fsr_voltage = 5000 * readings
            fsr_resistance = 5000 - fsr_voltage
            fsr_resistance = ((fsr_resistance * 47000) / fsr_voltage) / 1000
            fsr_force = 16154.22 / (2 * math.pow(fsr_resistance, 1.408))
            fsr_force = int(fsr_force)
        else:
            fsr_force = 0

        return fsr_force

    def stop_motor(self):
        self.stand_by(0)
