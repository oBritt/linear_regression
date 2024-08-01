import sys

def is_float(s):
    if s == "":
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False

class Module:

    def __init__(self, path):
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
        print(self.km)
        print(self.prices)
        

    def estimate_price(self, milage):
        return self.theta0 + self.theta1 * milage

    def calculate(self):
        acceptable = 0.0000000000000000000000000001
        counter = 0
        max_iterations = 4000
        prev_theta0 = 1
        prev_theta1 = 1
        return
        while (abs(self.theta0 - prev_theta0) > acceptable or abs(self.theta1 - prev_theta1) > acceptable):
            sum1 = 0
            sum2 = 0
            for i in range(self.M):
                error = self.estimate_price(self.km[i]) - self.prices[i]
                sum1 += error
                sum2 += error * self.km[i]

            self.theta0 -= self.learning_rate * sum1 / self.M
            self.theta1 -= self.learning_rate * sum2 / self.M

            counter += 1
            print(f"Iteration {counter}: theta0 = {self.theta0}, theta1 = {self.theta1}")


        with open("data.txt", "w") as f:
            t = [str(self.theta0), str(self.theta1)]
            s = ",".join(t)
            f.write(s)

    

def main():
    if (len(sys.argv) != 2):
        print("Usage [executable] [data_base]")
    try:
        m = Module(sys.argv[1])
    except Exception as e:
        print("Error with data")
    m.calculate()

if __name__ == "__main__":
    main()