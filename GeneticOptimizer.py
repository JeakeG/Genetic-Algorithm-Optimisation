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
"""
class GeneticOptimizer:
    def __init__(self, func, lowerBound, upperBound, **kwargs):
        self.func = func
        if not self.registerFunc():
            raise Exception("Provided function was formatted incorrectly.")

        self.lowerBound = lowerBound
        self.upperBound = upperBound
        if lowerBound >= upperBound:
            raise Exception("Lower bound must be less than upper bound.")

        self.iter = kwargs.get("iter", 50)
        if self.iter < 5:
            raise Exception("Must at least 5 iterations.")

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
        
        self.sum_fitness = []
        
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
        
    def firstGen(self):
        self.current_generation = []
        for i in range(self.size):
            rand_data = []
            for j in range(self.arglen):
                rand_data.append(random.uniform(self.lowerBound, self.upperBound))
            self.current_generation.append(Design(rand_data, self))
            
    def getFitness(self, design):
        return eval(self.func_name + str(design.data))
        
    def crossover(self):
        # calculates fitness for current generation
        fitness_list = []
        for i in range(self.size):
            fitness_list.append(self.getFitness(self.current_generation[i]))
        
        self.sum_fitness.append(sum(fitness_list)/self.size)

        # amount of previous generation to carry over
        carryover = int(self.size * self.elitism)
        num_child = self.size - carryover

        if num_child % 2 != 0:
            num_child += 1
            carryover -= 1
        
        # weighted random list of parents of next generation based on fitness
        # print(fitness_list)
        parent_pool = random.choices(self.current_generation, weights=fitness_list, k=num_child)
        next_generation = []
    
        # sorts generation by fitness level
        sorted_generation = [x for _,x in sorted(zip(fitness_list, self.current_generation), key= lambda x: x[0], reverse=True)]
        for i in range(carryover):
            next_generation[i] = sorted_generation[i]

        # perform crossover
        for i in range(0, num_child, 2):
            parent2 = parent_pool[i+1]
            parent1 = parent_pool[i]

            string1 = parent1.getBinaryString()
            string2 = parent2.getBinaryString()

            strlen = len(string1)
            crossover_point = random.randint(0, strlen)

            new_string1 = string1[:crossover_point] + string2[crossover_point:]
            new_string2 = string2[:crossover_point] + string1[crossover_point:]

            next_generation.append(Design(self.valueFromBinaryString(new_string1), self))
            next_generation.append(Design(self.valueFromBinaryString(new_string2), self))
        
        self.current_generation = next_generation
            
    def valueFromBinaryString(self, string):
        values = [string[i:i+self.precision] for i in range(0, len(string), self.precision)]
        L = self.lowerBound
        U = self.upperBound
        J = 2**self.precision - 1
        converted_values = []
        for x in values:
            converted_values.append(L + ((U-L)/J)*int(x, 2))
        return converted_values

    def optimize(self):
        self.firstGen()
        for i in range(self.iter):
            self.crossover()
        print(self.sum_fitness)
        for design in self.current_generation:
            print(design.data)

"""
    Class: Design
    init params:
        data
            -tuple
            -contains the data values for each variable of a potential design
        population
            -Population
            -object of population that design belongs to
"""
class Design:
    def __init__(self, data, population):
        self.data = tuple(data)
        self.lowerBound = population.lowerBound
        self.upperBound = population.upperBound
        self.precision = population.precision
    
    def getBinaryString(self):
        res = ""
        L = self.lowerBound
        U = self.upperBound
        J = 2**self.precision - 1
        for value in self.data:
            X = round(((value - L) * J)/(U - L))
            res += format(X, f'0{self.precision}b')
        return res