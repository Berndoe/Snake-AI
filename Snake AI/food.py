from turtle import Turtle
import random


class Food(Turtle):
    """This class creates the food object"""

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.color("red")
        self.speed("fastest")
        self.randomx = random.randint(-260, 260)
        self.randomy = random.randint(-260, 230)
        self.goto(self.randomx, self.randomy)

    # places food at a new random position when the snake eats it
    def refresh(self):
        self.randomx = random.randint(-260, 260)
        self.randomy = random.randint(-260, 230)
        self.goto(self.randomx, self.randomy)

    def get_xcor(self):
        return self.randomx

    def get_ycor(self):
        return self.randomy
