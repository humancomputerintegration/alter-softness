"""HARIOMHARIBOLJAIMATAJIPITAJIKIJAIJAI"""
# Developed by Mark Tomczak (fixermark@gmail.com)
# Python class to calculate PID values


class PIDController:
    def __init__(self, P, I, D):
        self.KP = P
        self.KI = I
        self.KD = D
        self.target = 140

        self.lastError = 0
        self.integrator = 0

    def set_target(self, newTarget):
        self.target = newTarget
        self.integrator = 0

    def step(self, currentValue):
        error = currentValue - self.target

        output = (
            self.KP * error
            + self.KI * self.integrator
            + self.KD * (error - self.lastError)
        )

        self.lastError = error
        self.integrator += error

        return output
