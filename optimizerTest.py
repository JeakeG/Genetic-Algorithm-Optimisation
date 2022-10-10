from GeneticOptimizer import GeneticOptimizer

def func(x, y):
    return -(x + 2*y - 7)**2 - (2*x + y - 5)**2

def main():
    # func = "f(x, y) = -(x**2 + y - 11)**2 - (x + y**2 - 7)**2 + 1000"
    # func = "f(x, y) = -(x + 2*y - y)**2 - (2*x + y - 5)**2 + 1000"
    # func = "f(x,y) = -x*y + 25"
    # func = "f(x) = -x**2 + 25"
    opt = GeneticOptimizer(func, -10, 10, iter=1000, size=100, elitism=0.20, precision=32)
    res = opt.optimize()
    print(res)

if __name__ == "__main__":
    main()