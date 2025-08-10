#!/usr/bin/python3

import os, platform
if platform.system() == "Linux" or platform.system() == "Darwin":
    os.environ["KIVY_VIDEO"] = "ffpyplayer"

from pysimbotlib.core import PySimbotApp, Robot
from kivy.logger import Logger
from kivy.config import Config

# Show only info or higher level logs
Config.set('kivy', 'log_level', 'info')

REFRESH_INTERVAL = 1/1000

class MyRobot(Robot):
    SAFETY_DIST = 20
    CLSOED_DIST = 15
    
    STEP = 10 
    SMALL_STEP = 5
    
    HUGE_TURN = 90
    BIG_TURN = 45
    TURN = 15

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sensor_history = []
        self.history_limit = 6
        self.repeat_threshold = 3

    def is_pattern(self, front, right, left):
        pattern = (front, right, left)
        self.sensor_history.append(pattern)

        if len(self.sensor_history) > self.history_limit:
            self.sensor_history.pop(0)

        repeat_count = sum(1 for p in self.sensor_history if p == pattern)
        return repeat_count >= self.repeat_threshold

    def update(self):
        front, right, IR2, IR3, IR4, IR5, IR6, left = self.distance()
        print(f"FF >> {front}")
        print(f"FR >> {right}")
        print(f"FL >> {left}")

        if self.is_pattern(front, right, left):
            print("stuck")
            if right < left:
                self.turn(self.HUGE_TURN * -1)
                print('left\n')
            else:
                self.turn(self.HUGE_TURN)
                print('right\n')
            self.sensor_history.clear()
            return

        if (front >= self.SAFETY_DIST and right >= self.SAFETY_DIST and left >= self.SAFETY_DIST):
            self.move(self.STEP)
            food_angle = self.smell()
            self.turn(food_angle / 2)
            print('move to food\n')

        elif (front >= self.SAFETY_DIST and (right < self.SAFETY_DIST or left < self.SAFETY_DIST)):
            print('obstacle')
            if right < left:
                self.turn(self.TURN * -1)
                print('left\n')
            else:
                self.turn(self.TURN)
                print('right\n')
            self.move(self.SMALL_STEP)

        else:
            print('crash')
            self.move(self.SMALL_STEP * -1)
            if right < left:
                self.turn(self.BIG_TURN * -1)
                print('left\n')
            else:
                self.turn(self.BIG_TURN)
                print('right\n')


if __name__ == '__main__':
    app = PySimbotApp(robot_cls=MyRobot,
                      interval=REFRESH_INTERVAL)
    app.run()
