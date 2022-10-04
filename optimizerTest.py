from GeneticOptimizer import GeneticOptimizer


def main():
    func = "f(x, y) = -(x**2 + y - 11)**2 - (x + y**2 - 7)**2 + 1000"
    func = "f(x, y) = -(x + 2*y - y)**2 - (2*x + y - 5)**2 + 1000"
    func = "f(x,y) = -x*y + 25"
    func = "f(x) = -x**2 + 25"
    opt = GeneticOptimizer(func, -5, 5, iter=100)
    opt.optimize()

if __name__ == "__main__":
    main()