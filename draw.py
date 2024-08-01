import pygame
from train_module import Module
import argparse

def is_float(s):
    if s == "":
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False
    
class Graph:
    def __init__(self, value, km, prices):
        self.value = value
        self.km = km
        self.prices = prices
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption('Histogramm')
        self.font_cwords = pygame.font.SysFont('Arial', 50)
        self.font_words = pygame.font.SysFont('Arial', 30)
        self.font_numbers = pygame.font.SysFont('Arial', 12)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def get_width_text(self, text:str, angle:int, font)->int:
        text_surface = font.render(text, True, (0, 0, 0))
        rotated_surface = pygame.transform.rotate(text_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        return rotated_rect.width
    
    def draw_text(self, text: str, position: tuple[int, int], angle: int, font) -> None:
        text_surface = font.render(text, True, (0, 0, 0))
        rotated_surface = pygame.transform.rotate(text_surface, angle)
        rotated_rect = rotated_surface.get_rect(center=position)
        self.screen.blit(rotated_surface, rotated_rect.topleft)

    def draw_y(self, x, y, height, max_value):
        pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x, y - height - 40), 3)
        pygame.draw.polygon(self.screen, (0, 0, 0), [[x, y - height - 70], [x - 11, y - height - 15], [x, y - height - 40], [x + 11, y - height - 15]])
        for i in range(10):
            w = self.get_width_text(str("%.0f" % (max_value * (i + 1) / 10)), 0, self.font_cwords)
            self.draw_text(str("%.0f" % (max_value * (i + 1) / 10)), ( x - 5 - w / 2  , y - height / 10 * (i + 1)), 0, self.font_words)
            pygame.draw.line(self.screen, (0, 0, 0), (x + 8,  y - height / 10 * (i + 1)), (x - 8,  y - height / 10 * (i + 1)), 3)

    def draw_x(self, x, y, width, max_value):
        pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x + width + 40, y), 3)
        pygame.draw.polygon(self.screen, (0, 0, 0), [[x + width + 70, y], [x + width + 15, y - 11], [x + width + 40, y], [x + width + 15, y + 11]])
        for i in range(10):
            self.draw_text(str("%.0f" % (max_value * (i + 1) / 10)), ( x + width / 10 * (i + 1) , y + 30), 0, self.font_words)
            pygame.draw.line(self.screen, (0, 0, 0), ( x + width / 10 * (i + 1) , y - 8), ( x + width / 10 * (i + 1) , y + 8), 3)

    def put_dots(self, x, y, width, height, max_x, max_y):
        for i in range(len(self.km)):
            real_x = x + width * self.km[i] / max_x
            real_y = y - height * self.prices[i] / max_y
            pygame.draw.circle(self.screen, (255, 0, 0), (real_x, real_y), 5)

    def draw_line(self, x, y, width, height, max_x, max_y):
        y1 = self.value[0]
        x1 = 0
        x2 = max_x
        y2 = self.value[0] + self.value[1] * max_x
        real_x1 = x + x1 * width / max_x
        real_y1 = y - y1 * height / max_y
        real_x2 = x + x2 * width / max_x
        real_y2 = y - y2 * height / max_y
        pygame.draw.line(self.screen, (0, 0, 255), (real_x1, real_y1), (real_x2, real_y2), 3)

    def display(self):
        
        width = 1600
        height = 800
        max_x = max(self.km) * 1.1
        max_y = max(self.prices) * 1.1
        self.draw_line(180, self.screen.get_height() - 150, width, height, max_x, max_y)
        self.draw_x(180, self.screen.get_height() - 150, width, max_x)
        self.draw_y(180, self.screen.get_height() - 150, height, max_y)
        self.draw_text("Kilometers", (150 + width / 2, self.screen.get_height() - 50), 0, self.font_cwords)
        self.draw_text("Price in Euro", (50, self.screen.get_height() - 150 - height / 2), 90, self.font_cwords)
        self.put_dots(180, self.screen.get_height() - 150, width, height, max_x, max_y)


    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill("white")
            self.handle_event()
            self.handle_keys()
            self.display()
            pygame.display.flip() 
            clock.tick(60)
        pygame.quit()



def main():
    value = None
    parser = argparse.ArgumentParser(description="Example input of programm.")
    parser.add_argument('file', type=str, help='The file to process')
    parser.add_argument('data', type=str, help='The output of training')
    args = parser.parse_args()

    try:
        with open(args.data, "r") as f:
            for line in f:
                value = line.split(',')
                if (len(value) != 2):
                    raise Exception
                if not is_float(value[0]) or not is_float(value[1]):
                    raise Exception
                value[0] = float(value[0])
                value[1] = float(value[1])
                break
    except Exception as e:
        print("Model is not trained or the file was modified")
        return
    g = None
    try:
        a = Module(args.file, 0)
        g = Graph(value, a.km, a.prices)
    except Exception as e:
        print("Smth is wrong with data")
        return
    g.run()

if __name__ == "__main__":
    main()