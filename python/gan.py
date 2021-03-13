#!/usr/bin/env python3

import pickle
import os
import neat


class NeatGAN():

    def __init__(self, gen_settings, player_settings):

        self.gen_population = neat.Population(gen_settings[0])
        self.gen_num_generations = gen_settings[1]
        self.gen_population.add_reporter(neat.StdOutReporter(True))
        self.gen_stats = neat.StatisticsReporter()
        self.gen_population.add_reporter(self.gen_stats)

        self.player_population = neat.Population(player_settings[0])
        self.player_num_generations = player_settings[1]
        self.player_population.add_reporter(neat.StdOutReporter(True))
        self.player_stats = neat.StatisticsReporter()
        self.player_population.add_reporter(self.player_stats)

    def eval_player(genomes, config):
        pass

    def train_player():

        best_generator = self.generator_population.run(
            self.eval_generator, self.self.generator_num_generations)

    def eval_generator(genomes, config):
        pass

    def train_generator():

        best_player = self.player_population.run(
            self.eval_player, self.self.player_num_generations)


if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)

    generator_config_file = os.path.join(
        local_dir, "config/generator_config.txt")
    generator_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                          generator_config_file)

    player_config_file = os.path.join(
        local_dir, "config/player_config.txt")
    player_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                       neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                       player_config_file)

    a = NeatGAN((generator_config, 20), (player_config, 20))
