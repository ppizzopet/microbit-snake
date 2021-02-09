import random
import microbit
 
score = 0
foodOnScreen = False
gameLoop = True
 
class Food(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
    def draw(self):
        microbit.display.set_pixel(self.x, self.y, 4)
 
    def getCollision(self):
        global foodOnScreen, snake, score
 
        if snake.x == self.x and snake.y == self.y:
 
            snake.bodySize += 1
 
            if snake.bodySize == 1:
                snake.body.append(SnakeBody(snake.x, snake.y, snake.bodySize, snake.snakeDist, snake.previousDist))
            else:
                snake.body.append(SnakeBody(snake.body[-1].x, snake.body[-1].y, snake.bodySize,
                                            snake.body[-1].bodyDist, snake.body[snake.bodySize - 2].previousDist))
 
            foodOnScreen = False
            score += 1
 
 
class SnakeBody(object):
    def __init__(self, x, y, bodySize, dist, previousDist):
        self.x = x
        self.y = y
        self.bodyDist = dist
        self.previousDist = previousDist
        self.posInBody = bodySize
 
        if self.bodyDist == "up":
            self.y += 1
        if self.bodyDist == "down":
            self.y -= 1
        if self.bodyDist == "right":
            self.x -= 1
        if self.bodyDist == "left":
            self.x += 1
 
    def draw(self):
        microbit.display.set_pixel(self.x, self.y, 7)
 
    def updateDir(self):
        if self.posInBody <= 1:
            self.bodyDist = snake.previousDist
        else:
            self.bodyDist = snake.body[(self.posInBody - 2)].previousDist
 
    def moveBody(self):
 
        if self.bodyDist == "up":
            self.y -= 1
        elif self.bodyDist == "down":
            self.y += 1
        elif self.bodyDist == "right":
            self.x += 1
        elif self.bodyDist == "left":
            self.x -= 1
 
        self.previousDist = self.bodyDist
 
 
class Snake(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.snakeDist = "up"
        self.body = []
        self.bodySize = 0
        self.previousDist = None
 
        self.countdownToMove = 0
        self.delayToMove = 20
 
    def moveSnake(self):
        self.countdownToMove += 1
 
        if self.countdownToMove == self.delayToMove:
 
            if self.snakeDist == "up":
                self.y -= 1
            elif self.snakeDist == "down":
                self.y += 1
            elif self.snakeDist == "right":
                self.x += 1
            elif self.snakeDist == "left":
                self.x -= 1
 
            for body in self.body:
                body.moveBody()
                if self.x == body.x and self.y == body.y:
                    gameOver()
 
            self.countdownToMove = 0
            self.previousDist = self.snakeDist
 
    def drawSnake(self):
        try:
            microbit.display.set_pixel(self.x, self.y, 9)
            for body in self.body:
                body.draw()
        except:
            gameOver()
 
 
snake = Snake(2, 2)
 
 
def gameOver():
    global score
    microbit.display.scroll("Game Over! Your score was "+str(score))
 
 
 
def run():
    global snake, foodOnScreen
 
    food = Food(0, 0)
 
    while gameLoop:
        microbit.sleep(75)
 
        if not foodOnScreen:
            food.x, food.y  = random.randint(1, 4), random.randint(1, 4)
            foodOnScreen = True
 
        microbit.display.clear()
 
        # SNAKE MOVEMENT
        if microbit.button_a.is_pressed():
            if snake.snakeDist == "up":
                microbit.display.show(microbit.Image.ARROW_S)
                snake.snakeDist = "down"
                microbit.sleep(750)
            elif snake.snakeDist == "down":
                microbit.display.show(microbit.Image.ARROW_E)
                snake.snakeDist = "right"
                microbit.sleep(750)
            elif snake.snakeDist == "right":
                microbit.display.show(microbit.Image.ARROW_W)
                snake.snakeDist = "left"
                microbit.sleep(750)
            elif snake.snakeDist == "left":
                microbit.display.show(microbit.Image.ARROW_N)
                snake.snakeDist = "up"
                microbit.sleep(750)
        for body in snake.body:
            body.updateDir()
 
        food.draw()
        snake.moveSnake()
        snake.drawSnake()
        food.getCollision()
 
        # CHECKS IF SNAKE TOUCH THE BORDER
        if snake.x > 4 or snake.x < 0 or snake.y > 4 or snake.y < 0:
            gameOver()
 
run()
