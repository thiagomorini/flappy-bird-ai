import neat

class AI:
  
    def __init__(self):
        self.generation = 0
        self.networks = []
        self.genome_list = []

    def init_genomes(self, genomes, config):
        for _, genome in genomes:
            self.network = neat.nn.FeedForwardNetwork.create(genome, config)
            self.networks.append(self.network)
            genome.fitness = 0
            self.genome_list.append(genome)      

    def inc_generation(self):
        self.generation += 1

    def update_fitness(self, index, value):
        self.genome_list[index].fitness += value

    def activate(self, index, activate):
        return self.networks[index].activate(activate)

    def drop(self, index):
        self.genome_list.pop(index)
        self.networks.pop(index)        

    def start(self, config_path, fitness_function, with_reporter):
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )

        population = neat.Population(config)

        if with_reporter:
            population.add_reporter(neat.StdOutReporter(True))
            population.add_reporter(neat.StatisticsReporter())

        population.run(fitness_function, 50) # max 50 generations
