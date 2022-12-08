from dino_runner.components.player_hearts.heart import Heart

class PlayerHeartManager:
    def __init__(self):
        self.heart_count = 5

    def reduce_heart_count(self):
        self.heart_count -= 1

    def draw(self, screen):
        x_position = 10
        y_position = 20

        for counter in range(self.heart_count):
            heart = Heart(x_position, y_position)
            heart.draw(screen)
            x_position += 30
    
    def reset_heart_count(self):
        self.heart_count = 5