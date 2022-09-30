class Population:
    def __init__(self, lowerBound, upperBound, **kwargs):
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        if lowerBound >= upperBound:
            raise Exception("Lower bound must be less than upper bound.")

        self.iter = kwargs.get("iter", 50)
        if self.iter < 1:
            raise Exception("Must have more than 0 iterations.")

        self.size = kwargs.get("size", 25)
        if self.size < 1:
            raise Exception("Must have a population larger than 0.")
        
        self.elitism = kwargs.get("elitism", 0.0)
        if self.elitism < 0 or self.elitism > 1:
            raise Exception("Elitism must be a value from 0 to 1.")
        
        self.precision = kwargs.get("precision", 8)


class Individual:
    def __init__(self, data, **kwargs):
        self.data = data