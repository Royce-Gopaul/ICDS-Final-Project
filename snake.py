from tkinter import *
import random 

class SnakeGame:
    def __init__(self):
        
        self.WIDTH = 500
        self.HEIGHT = 500
        self.SPEED = 200
        self.SPACE_SIZE = 20
        self.BODY_SIZE = 2
        self.SNAKE_COLOR = "#00FF00"
        self.FOOD_COLOR = "#FFFFFF"
        self.BACKGROUND_COLOR = "#000000"
        self.score = 0
        self.direction = 'down'
        
        self.window = Tk()
        self.window.title("Snake Game")
        self.canvas = Canvas(self.window, bg=self.BACKGROUND_COLOR, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()

        self.label = Label(self.window, text="Points:{}".format(self.score), font=('consolas', 20))
        self.label.pack()

        self.food = self.create_food()
        self.snake = self.create_snake()

        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))

        self.next_turn()

    def create_snake(self):
        snake = []
        x_start = self.WIDTH / 2
        y_start = self.HEIGHT / 2
        for i in range(self.BODY_SIZE):
            x = x_start
            y = y_start - i * self.SPACE_SIZE
            snake.append(self.canvas.create_rectangle(x, y, x + self.SPACE_SIZE, y + self.SPACE_SIZE, fill=self.SNAKE_COLOR))
        return snake

    def create_food(self):
        x = random.randint(0, (self.WIDTH / self.SPACE_SIZE) - 1) * self.SPACE_SIZE
        y = random.randint(0, (self.HEIGHT / self.SPACE_SIZE) - 1) * self.SPACE_SIZE
        return self.canvas.create_oval(x, y, x + self.SPACE_SIZE, y + self.SPACE_SIZE, fill=self.FOOD_COLOR)

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def next_turn(self):
        head_coords = self.canvas.coords(self.snake[0])  # Get coordinates of the snake's head
        x, y = head_coords[0], head_coords[1]  # Extract x and y coordinates of the snake's head

        if self.direction == "up":
            y -= self.SPACE_SIZE
        elif self.direction == "down":
            y += self.SPACE_SIZE
        elif self.direction == "left":
            x -= self.SPACE_SIZE
        elif self.direction == "right":
            x += self.SPACE_SIZE

        new_head = self.canvas.create_rectangle(x, y, x + self.SPACE_SIZE, y + self.SPACE_SIZE, fill=self.SNAKE_COLOR)
        self.snake.insert(0, new_head)

        # Check if the snake's head collides with the food
        food_coords = self.canvas.coords(self.food)
        if head_coords[0] == food_coords[0] and head_coords[1] == food_coords[1]:
            self.score += 1
            self.label.config(text="Points:{}".format(self.score))
            self.canvas.delete(self.food)
            self.food = self.create_food()  # Create new food at a random position
        else:
            # Remove the tail of the snake if it did not eat the food
            self.canvas.delete(self.snake[-1])
            self.snake.pop()

        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(self.SPEED, self.next_turn)

    def check_collisions(self):
        head_coords = self.canvas.coords(self.snake[0])  # Get coordinates of the snake's head
        x, y = head_coords[0], head_coords[1]  # Extract x and y coordinates of the snake's head

        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return True

        for body_part in self.snake[1:]:
            if x == self.canvas.coords(body_part)[0] and y == self.canvas.coords(body_part)[1]:
                return True

        return False

    def game_over(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(self.WIDTH / 2, self.HEIGHT / 2, font=('consolas', 70), text="GAME OVER", fill="red")

    def play(self):
        self.window.mainloop()

def main():
    game = SnakeGame()
    game.play()

if __name__ == "__main__":
    main()
