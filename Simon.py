# link to video: https://youtu.be/_8N2OkqrNfE

import RPi.GPIO as GPIO
import random
import wiringpi
from time import sleep

gpioPinRed = 21
gpioPinYellow = 20
gpioPinGreen = 16
gpioPinBlue = 12
gpioButtonRed = 5
gpioButtonYellow = 6
gpioButtonGreen = 13
gpioButtonBlue = 19
gpioSpeaker = 17

led = [gpioPinRed, gpioPinYellow, gpioPinGreen, gpioPinBlue]
buttons = [gpioButtonRed, gpioButtonYellow, gpioButtonGreen, gpioButtonBlue]
sounds = [440, 523, 659, 784]

moves = []
playing = True

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(gpioSpeaker)

for i in range(0, len(led)):
    GPIO.setup(buttons[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(led[i], GPIO.OUT, initial=GPIO.LOW)


while playing:
    currentMove = random.randint(0, 3)
    moves.append(currentMove)

    for move in range(0, len(moves)):
        wiringpi.softToneWrite(gpioSpeaker, sounds[moves[move]])
        GPIO.output(led[moves[move]], GPIO.HIGH)
        sleep(1)
        wiringpi.softToneWrite(gpioSpeaker, -sounds[moves[move]])
        GPIO.output(led[moves[move]], GPIO.LOW)
        sleep(1)

    for move in range(0, len(moves)):
        pushed = False
        while not pushed:
            for currentButton in range(0, len(buttons)):
                if GPIO.input(buttons[currentButton]) == GPIO.HIGH:
                    pushed = True
                    wiringpi.softToneWrite(gpioSpeaker, sounds[currentButton])
                    GPIO.output(led[currentButton], GPIO.HIGH)
                    sleep(1)
                    wiringpi.softToneWrite(gpioSpeaker, -sounds[currentButton])
                    GPIO.output(led[currentButton], GPIO.LOW)
                    if moves[move] != currentButton:
                        playing = False
                        for i in range(0, len(led)):
                            GPIO.output(led[i], GPIO.HIGH)
                        wiringpi.softToneWrite(gpioSpeaker, 880)
                        sleep(1)
                        wiringpi.softToneWrite(gpioSpeaker, -880)
                        for i in range(0, len(led)):
                            GPIO.output(led[i], GPIO.LOW)
        if not playing:
            break
    sleep(1)
