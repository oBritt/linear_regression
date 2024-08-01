import argparse
import pygame

def is_float(s):
    if s == "":
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False

class Module:

    def __init__(self, path, bonus):
        self.prices = []
        self.km = []
        self.theta0 = 0
        self.theta1 = 0
        self.learning_rate = 0.01
        reversed = 0
        with open(path, "r") as f:
            for ind, line in enumerate(f):
                line = line.strip()
                if (line == ""):
                    continue
                t = line.split(',')
                if len(t) != 2:
                    raise ValueError
                if (ind == 0):
                    if t[0] != "km" and t[1] != "km":
                        raise ValueError
                    if t[0] != "price" and t[1] != "price":
                        raise ValueError
                    if (t[0] != "km"):
                        reversed = 1
                else:
                    if not is_float(t[0]) or not is_float(t[1]):
                        raise ValueError
                    if (reversed):
                        self.km.append(float(t[1]))
                        self.prices.append(float(t[0]))
                    else:
                        self.km.append(float(t[0]))
                        self.prices.append(float(t[1]))
        self.M = len(self.km)
        self.bonus = bonus  
        if self.bonus:
            pygame.init()
            self.running = True
            self.screen = pygame.display.set_mode((1920, 1080))
            pygame.display.set_caption('Histogramm')
            self.font_cwords = pygame.font.SysFont('Arial', 50)
            self.font_words = pygame.font.SysFont('Arial', 30)
            self.font_numbers = pygame.font.SysFont('Arial', 12)
            self.t0 = [0]
            self.t1 = [0]
            self.finished = 0
            self.km_n = self.normalisation(self.km)
            self.prices_n = self.normalisation(self.prices)
            self.acceptable_error = 0.001
            self.max_iterations = 10000
            self.current = 0

    def split_range(self, start, end, n):
        if n <= 0:
            raise ValueError("Number of parts must be greater than zero")
        
        step = (end - start) / n
        ranges = [[start + step * i, start + step * (i + 1)] for i in range(n)]
        return ranges

    def map_number(self, value, from_min, from_max, to_min, to_max):
        if from_min == from_max:
            raise ValueError("The source range cannot have the same min and max values.")
        scale = (to_max - to_min) / (from_max - from_min)
        return to_min + (value - from_min) * scale

    def get_values_y(self, values):
        min_v = min(min(values), 0) * 1.2
        max_v = max(values) * 1.2
        return self.split_range(min_v, max_v, 10)

    def normalisation(self, s):
        return [(_ / max(s)) for _ in s]

    def estimate_price(self, milage):
        return self.theta0 + self.theta1 * milage

    def calculate(self):
        km = self.normalisation(self.km)
        prices = self.normalisation(self.prices)
        acceptable_error = 0.001
        max_iterations = 10000
        for iteration in range(max_iterations):
            sum1 = 0.0
            sum2 = 0.0
            for i in range(self.M):
                error = self.estimate_price(km[i]) - prices[i]
                sum1 += error
                sum2 += error * km[i]
        
            # Update parameters
            self.theta0 -= (self.learning_rate * sum1) / self.M
            self.theta1 -= (self.learning_rate * sum2) / self.M  
            if abs(sum1) < acceptable_error and abs(sum2) < acceptable_error:
                break

        self.theta0 *= max(self.prices)
        self.theta1 = self.theta1 / max(self.km) * max(self.prices) 
        with open("data.txt", "w") as f:
            t = [str(self.theta0), str(self.theta1)]
            s = ",".join(t)
            f.write(s)

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

    def display_x(self, x, y, width, max_val):
        pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x + width + 30, y))
        for i in range(10):
            self.draw_text(str(max_val / 10 * (i + 1)), (x + width / 10 * (i + 1), y + 10), 0, self.font_numbers)
            pygame.draw.line(self.screen, (0, 0, 0), (x + width / 10 * (i + 1), - 5), (x + width / 10 * (i + 1), + 5), 3)


    def display_y(self, x, y, height, values):
        pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x, y - height - 30))
        values_y = self.get_values_y(values)
        for i in range(10):
            w = self.get_width_text(str("%.4f" % values_y[i][1]), 0, self.font_numbers)
            self.draw_text(str("%.4f" % values_y[i][1]), (x - w / 2 - 8, y - height / 10 * (i + 1)), 0, self.font_numbers)
            pygame.draw.line(self.screen, (0, 0, 0), (x + 5, y - height / 10 * (i + 1)), (x - 5, y - height / 10 * (i + 1)), 3)
    
    def calc1(self):
        km = self.km_n
        prices = self.prices_n
        sum1 = 0.0
        sum2 = 0.0
        for i in range(self.M):
            error = self.estimate_price(km[i]) - prices[i]
            sum1 += error
            sum2 += error * km[i]

        self.theta0 -= (self.learning_rate * sum1) / self.M
        self.theta1 -= (self.learning_rate * sum2) / self.M
        if not self.current % 10:
            self.t0.append(self.theta0 * max(self.prices))
            self.t1.append(self.theta1 / max(self.km) * max(self.prices))
        if self.current == self.max_iterations or (abs(sum1) < self.acceptable_error and abs(sum2) < self.acceptable_error):
            self.finished = 1
        self.current += 1

    def output_dots(self, x, y, width, height, values):
        values_y = self.get_values_y(values)
        max_y = values_y[9][1]
        min_y = values_y[0][0]
        for ind, dot in enumerate(values):
            pygame.draw.circle(self.screen, (0, 0, 255), (x + width / (self.max_iterations / 10) * (ind + 1), y - self.map_number(dot, min_y, max_y, 0, height)), 2)

    def display(self):
        width = 750
        height = 750
        if (not self.finished):
            self.calc1()
            self.draw_text("Computing", (self.screen.get_width() / 2, 50), 0, self.font_cwords)
        else:
            self.draw_text("Finished", (self.screen.get_width() / 2, 50), 0, self.font_cwords)

        self.draw_text("theta0", (100 + width / 2, 200), 0, self.font_cwords)
        self.display_x(100, self.screen.get_height() - 100, width, self.max_iterations)
        self.display_y(100, self.screen.get_height() - 100, height, self.t0)

        self.draw_text("theta1", (100 + width / 2 + width + 200, 200), 0, self.font_cwords)
        self.display_x(100 + width + 200, self.screen.get_height() - 100, width, self.max_iterations)
        self.display_y(100 + width + 200, self.screen.get_height() - 100, height, self.t1)

        self.output_dots(100, self.screen.get_height() - 100, width, height, self.t0)
        self.output_dots(100 + width + 200, self.screen.get_height() - 100, width, height, self.t1)

    # Mean Absolute Percentage Error (MAPE)
    def output_mape(self):
        total = 0
        for i in range(self.M):
            total += abs((self.prices[i] - self.estimate_price(self.km[i])) / self.prices[i])
        total = total / float(self.M) * 100
        print(f"MEPA is: {"%.4f" % total}%")

    # Coefficient of Determination (R-squared)
    def output_r2(self):
        total0 = 0
        total1 = 0
        mean = sum(self.prices) / self.M
        for i in range(self.M):
            total0 += (self.prices[i] - self.estimate_price(self.km[i])) ** 2
            total1 += (self.prices[i] - mean) ** 2
        if (total1 != 0):
            r = 1 - total0 / total1
        else:
            r = 1
        r *= 100
        print(f"R2 is: {"%.4f" % r}%")


    # Percentage of Predictions within a Tolerance Range
    def output_within_percent(self, p):
        p = p / 100
        counter = 0
        for i in range(self.M):
            t = abs((self.prices[i] - self.estimate_price(self.km[i])) / self.prices[i])
            if (t <= p):
                counter += 1
        print(f"{"%.2f" % (counter / self.M * 100)}% of values are within a Tolarance Range of {p * 100}%")

    def calculate_accuracy(self):
        self.output_mape()
        self.output_r2()
        self.output_within_percent(5)

    def bonus_func(self):
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill("white")
            self.handle_event()
            self.handle_keys()
            self.display()
            pygame.display.flip() 
            clock.tick(60)
        pygame.quit()
        with open("data.txt", "w") as f:
            t = [str(self.t0[len(self.t0) - 1]), str(self.t1[len(self.t1) - 1])]
            s = ",".join(t)
            f.write(s)
        self.theta0 = self.t0[len(self.t0) - 1]
        self.theta1 = self.t1[len(self.t1) - 1]
        self.calculate_accuracy()

    def make_job(self):
        if (self.bonus):
            self.bonus_func()
        else:
            self.calculate()


def main():
    parser = argparse.ArgumentParser(description="Example input of programm.")
    
    parser.add_argument('file', type=str, help='The file to process')
    parser.add_argument('-b', '--bonus', action='store_true', help='Enable bonus feature')
    args = parser.parse_args()

    try:
        m = Module(args.file, args.bonus)
    except Exception as e:
        print("Error with data")
        return
    m.make_job()

if __name__ == "__main__":
    main()