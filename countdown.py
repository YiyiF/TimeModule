#! /usr/bin/env python3

# countdown.py - A simple countdown script.

import time, subprocess

timeLeft = 60
while timeLeft > 0:
    print(timeLeft, end=' ')
    time.sleep(1)
    timeLeft -= 1

subprocess.Popen(['open', 'Alarm 02.wav'])
