import RPi.GPIO as GPIO
import time


class Servo:

    def __init__(self, pin):
        self.pin = pin

    def __del__(self):
        GPIO.cleanup()

    def _setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.p = GPIO.PWM(self.pin, 50)

    def _convert_angle(self, angle):
        return (angle * 1 / 18) + 2.5

    def set_angle(self, angle):
        angle *= -1
        angle += 90
        self._setup()
        self.p.start(self._convert_angle(angle))
        time.sleep(1)
        self.p.stop()


if __name__ == "__main__":
    servo = Servo(16)
    while True:
        servo.set_angle(float(input("Angle: ")))
