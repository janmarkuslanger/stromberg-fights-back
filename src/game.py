#!/usr/bin/env python
from element import Element


class Game:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def is_element_not_in_range(self, element: Element) -> bool:
        topside_not_in_range = (
            element.pos.top < 0
            or element.pos.bottom < 0
            or element.pos.left < 0
            or element.pos.right < 0
        )

        bottomside_not_in_range = (
            element.pos.top > self.height
        )

        return (topside_not_in_range or bottomside_not_in_range)