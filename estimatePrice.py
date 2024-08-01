import argparse

def is_float(s):
    if s == "":
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False


def main():
    value = None
    parser = argparse.ArgumentParser(description="Example input of programm.")
    
    parser.add_argument('kilo', type=float, help='Amount of kilometers to calculate price for')
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
    print(f"Price for {args.kilo}km will be {"%.2f" % (value[0] + value[1] * args.kilo)} Euro")

if __name__ == "__main__":
    main()