from GeneticOptimizer import GeneticOptimizer

def main():
    def func(x, y): return 1/(1+(x-3)**2+(y-4)**2) + 1/(2+(x-6)**2+(y-7)**2) # Sol. at (3, 4)
    # def func(x, y): return  -(x**2 + y - 11)**2 - (x + y**2 - 7)**2 # Sol. at (3, 2) (-2.805, -3.131) (-3.779, -3.283) (3.584, -1.848)
    # def func(x, y): return -(x + 2*y - 7)**2 - (2*x + y - 5)**2 # Sol. at (1,3)
    # def func(x,y): return -x**2 - y**2 # Sol. at (0, 0)
    # def func(x): return -x**2 # Sol. at (0)
    opt = GeneticOptimizer(func, -10, 10, iter=500, size=100, elitism=0.20, precision=32, tournament_size=30, mutation=0.1)
    (bestDesign, designValues, designFitness, fitnessHistory) = opt.optimize()
    bar = "="*100
    print(f"{bar}\nDesign String:\n{bestDesign}\n\nDesign Values:\n{designValues}\n\nDesign Fitness:\n{designFitness}\n\nHistory of Fitness:\n{fitnessHistory}\n{bar}\n")

if __name__ == "__main__":
    main()