import inspect
import random

"""
    Class: GeneticOptimizer
    init params:
        func
            -string
            -function that is to be optimized formatted with python syntax
        lowerBound
            -float
            -lower bound of optimization
        upperBound
            -float
            -upper bound of optimization
        iter
            -int > 0
            -the number of generations that will be produced
        size
            -int > 0
            -the size of the population for each generation
        elitism
            -float [0, 1]
            -the best performing percentage of the previous population that will carry over to the new population
        precision
            -int > 0
            -the number of digits in the binary representation of the design's variables
        mutation
            -float [0, 1]
            -the chance of a mutation occuring in offspring
        tournament_size
            -int < size
            -the number of designs present for each tournament selection
"""
class GeneticOptimizer:
    def __init__(self, func, lowerBound, upperBound, **kwargs):
        self.func = func
        self.arglen = len(str(inspect.signature(self.func)).split(","))

        self.lowerBound = lowerBound
        self.upperBound = upperBound
        if lowerBound >= upperBound:
            raise Exception("Lower bound must be less than upper bound.")

        self.iter = kwargs.get("iter", 50)
        if self.iter < 0:
            raise Exception("Must at least 1 iteration.")

        self.size = kwargs.get("size", 25)
        if self.size % 2 != 0:
            self.size += 1
        if self.size < 6:
            raise Exception("Must have a population size of at least 6.")
        
        self.elitism = kwargs.get("elitism", 0.0)
        if self.elitism < 0 or self.elitism > 1:
            raise Exception("Elitism must be a value from 0 to 1.")
        
        self.precision = kwargs.get("precision", 8)
        if self.precision < 1:
            raise Exception("Precision must be greater than 0")
        
        self.mutation = kwargs.get("mutation", 0.05)
        if self.mutation < 0 or self.mutation > 1:
            raise Exception("Mutation must be a value from 0 to 1.")
        
        self.tournament_size = kwargs.get("tournament_size", 3)
        if self.tournament_size > self.size:
            raise Exception("Tournament size must be smaller than population size")
        
        # history of population's fitness
        self.fitness_history = []
        # list of designs in current generation
        self.current_gen = []
        # save current best design
        self.best = None


    def registerFunc(self):
        try:
            string = self.func
            split_string = string.split("=")
            func_name = string.split("(")[0]
            exec(f"global {func_name}\ndef {split_string[0].strip()}:   return {split_string[1].strip()}")
            args = split_string[0].split("(")[1].split(")")[0].split(",")
            arg_nums = len(args)

            self.func_name = func_name
            self.arglen = arg_nums

            return True
        except Exception as e:
            return False


    def spawnFirstGeneration(self):
        for i in range(self.size):
            s = ""
            for j in range(self.precision * self.arglen):
                s += str(random.randint(0, 1))
            self.current_gen.append(s)
    

    def getFitness(self, design):
        args = self.getValuesFromString(design)
        return self.func(*args)
        # return eval(self.func_name + str(args))
    

    def getValuesFromString(self, designString):
        values = [designString[i:i+self.precision] for i in range(0, len(designString), self.precision)]
        L = self.lowerBound
        U = self.upperBound
        J = 2**self.precision - 1
        converted_values = []
        for x in values:
            converted_values.append(L + ((U-L)/J)*int(x, 2))
        return tuple(converted_values)
    

    def generateChildren(self, parent1, parent2):
        child1 = ""
        child2 = ""
        for i in range(self.arglen):
            crossover_point = random.randint(0, self.precision - 1)
            start_idx = i*self.precision
            end_idx = (i+1)*self.precision
            child1 += parent1[start_idx:start_idx + crossover_point] + parent2[start_idx + crossover_point:end_idx]
            child2 += parent2[start_idx:start_idx + crossover_point] + parent1[start_idx + crossover_point:end_idx]
        children = [child1, child2]
        for i in range(2):
            if random.random() < 1:
                mutation_point = random.randint(0, self.precision * self.arglen - 1)
                l = list(children[i])
                l[mutation_point] = "0" if l[mutation_point] == "1" else "1"
                children[i] = "".join(l)
        return children
    

    def generateNewGeneration(self):
        num_child = round(self.size * (1 - self.elitism))
        num_carryover = round(self.size * self.elitism)
        if not num_child % 2 == 0:
            num_child += 1
            num_carryover -= 1
        
        # calculate fitness for generation and save result
        gen_fitness = [self.getFitness(x) for x in self.current_gen]
        self.fitness_history.append(sum(gen_fitness) / self.size)

        # carry over best designs from prev generation based on elitism
        sorted_generation = [x for _,x in sorted(zip(gen_fitness, self.current_gen), key= lambda x: x[0], reverse=True)]
        new_gen = sorted_generation[:num_carryover]

        for i in range(0, num_child, 2):
            new_gen.extend(self.generateChildren(*self.selectParents()))
        
        self.current_gen = new_gen
        
        
    def selectParents(self):
        k = self.tournament_size
        parent_num = 2
        parents = []
        for i in range(parent_num):
            best = None
            gen = self.current_gen.copy()
            # remove already chosen parents from selection pool
            [gen.remove(p) for p in parents]

            # choose best design from random choice of k designs
            for j in range(k):
                ind = random.randint(0, len(gen)-1)
                if best == None or self.getFitness(best) < self.getFitness(gen[ind]):
                    best = gen[ind]
                gen.remove(gen[ind])
            
            parents.append(best)
        return parents


    def optimize(self):
        self.spawnFirstGeneration()
        self.generateNewGeneration()
        for i in range(self.iter):
            self.generateNewGeneration()
        
        best = [x for _,x in sorted(zip([self.getFitness(x) for x in self.current_gen], self.current_gen), key= lambda x: x[0], reverse=True)][0]
        return (best, self.getValuesFromString(best))