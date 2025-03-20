import pygame
from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


BOARD_BACKGROUND_COLOR = (0, 0, 0)


BORDER_COLOR = (93, 216, 228)


APPLE_COLOR = (255, 0, 0)


SNAKE_COLOR = (0, 255, 0)


SPEED = 5


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


pygame.display.set_caption('Змейка')


clock = pygame.time.Clock()


class GameObject:
    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        self.body_color = body_color
        self.position = position
    
    def draw (self):
        """Отрисовывает объект на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self): 
        start_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  
        super().__init__(start_position, SNAKE_COLOR)

        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None

        self.last = None

    def move(self):
        """Обновляет позицию змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None 

        new_head = (
            self.positions[0][0] + self.direction[0] * GRID_SIZE,
            self.positions[0][1] + self.direction[1] * GRID_SIZE
        )
        
        self.positions.insert(0, new_head)
        self.last = self.positions.pop()
        self.position = self.positions[0]
    
    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    def __init__(self):
        super().__init__(self.random_position(), APPLE_COLOR)

    def random_position(self):
        """Генирирует случайную позицию для яблока."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE    
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x,y)
    
    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
#;

def main():
    """Основная функция игры."""
    pygame.init()
    
    snake = Snake()
    apple = Apple()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False           
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.next_direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.next_direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.next_direction = RIGHT
        snake.move()

        if snake.positions[0] == apple.position:
            snake.positions.append(snake.last)
            apple.position = apple.random_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.flip()   
    
        clock.tick(SPEED)

    pygame.quit()


if __name__ == "__main__":
    main()