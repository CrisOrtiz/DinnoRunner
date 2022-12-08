import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.player_hearts.player_heart_manager import PlayerHeartManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.score import Score
from dino_runner.utils.constants import BG, DINO_START, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.utils.text_utils import draw_message_component
class Game:
    def __init__(self):
        
        self.INITIAL_GAME_SPEED = 20
        
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Creamelo una ventana con estas dimensiones
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = self.INITIAL_GAME_SPEED
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.player_heart_manager = PlayerHeartManager()
        self.power_up_manager = PowerUpManager()
        self.score = Score()
        self.death_count = 0

        self.executing = False

    def execute(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()

        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.score.current_score = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.score.update(self)
        self.power_up_manager.update(self.score.current_score, self.game_speed, self.player)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.player.check_power_up(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.player_heart_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width: # Si la imagen ha pasado completamente la ventana
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        pass

    def show_menu(self):
        # Poner color al fondo *
        self.screen.fill((255, 255, 255))

        # Mostrar mensaje de inicio
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        if self.death_count == 0:
            draw_message_component("Press any key to start", self.screen)
        else:
            # Tarea - Refactorizar el codigo de forma que reusemos la misma cosa(funcion, metodo, clase) para mostrar los mensajes.
            # Mostrar puntos obtenidos
            # Mostrar mensaje de reinicio
            # mostrar muertes totales
            draw_message_component("Press any key to restart", self.screen)
            draw_message_component(
                f"Your Score: {self.score.current_score}",
                self.screen,
                pos_y_center=half_screen_height + 50
            )
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen,
                pos_y_center=half_screen_height + 100
            )

        # Mostrar imagen como icono
        self.screen.blit(DINO_START, (half_screen_width - 20, half_screen_height - 140))
        # Actualizar pantalla
        pygame.display.flip()
        # Manejar eventos
        self.handle_menu_events()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def reset_game_speed(self):
        self.game_speed = self.INITIAL_GAME_SPEED