#!/usr/bin/env python
class Element:
    def __init__(self, speed: int, top: int, left: int) -> None:
        self.speed = speed
        self.top = top
        self.left = left
        self.pos = None

    def move_up(self) -> None:
        self.pos = self.pos.move(0, -1*self.speed)

    def move_down(self) -> None:
        self.pos = self.pos.move(0, 1*self.speed)

    def move_left(self) -> None:
        self.pos = self.pos.move((-1*self.speed), 0)

    def move_right(self) -> None:
        self.pos = self.pos.move(1*self.speed, 0)