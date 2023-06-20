from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    """This class creates a scoreboard which is displayed on the screen"""

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.score = 0

        with open("highscore.txt") as file:
            self.highscore = int(file.read())

        self.color("white")
        self.goto(0, 260)
        self.write(arg=f"Score: {self.score} Highscore: {self.highscore}", align=ALIGNMENT, font=FONT)
        self.hideturtle()

    def update_score(self):
        self.clear()
        self.score += 1
        self.write(arg=f"Score: {self.score} Highscore: {self.highscore}", align=ALIGNMENT, font=FONT)

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score

        self.save_highscore()
        self.score = 0
        self.update_score()

    # displays game over when the snake hits the edge of the screen
    def game_over(self):
        self.reset()
        self.goto(0, 0)
        self.write(arg=f"GAME OVER", align=ALIGNMENT, font=FONT)

    def save_highscore(self):
        with open("highscore.txt", "w") as file:
            file.write(f"{self.highscore}")
