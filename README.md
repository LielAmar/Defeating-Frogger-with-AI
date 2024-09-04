# AI Learns to Play Frogger

Hello!

This project is a simple implementation of a frogger-like game, with two AI agents that learn to play it using Deep Q-learning and NEAT.
It was developed by Liel Amar, Tomer Meidan and Omer Ferster from The Hebrew University of Jerusalem, as part of the course "Introduction to Artificial Intelligence" (2024).

## Installation
To install the required packages, use your favorite package manager to initialize a new environment.
Then, run the following command to install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration
There are several configuration flags that can be inputted to the program, to change the behavior of the game and the learning algorithms.
The flags are as follows:
- `--agent`: The agent to use. Can be either `dqn`, `neat`, `random` or `onlyup`. Default is `random`.
- `--fps`: The frames per second of the game. Default is 5.
- `--grid_like`: Whether to use a grid-like environment or a continuous one. Default is `False`.
- `--with_train`: Whether to include the train obstacle or not. Default is `False`.
- `--with_water`: Whether to include the water segment or not. Default is `False`.
- `--games`: The number of games to play. Default is 3.
- `--lives`: The number of lives the agent has. Default is 3 (only for NEAT).
- `--neat_config`: The configuration file for NEAT. Default is `neat-config.txt`.
- `--generations`: The number of generations to run NEAT for. Default is 200.
- `--plot`: Whether to plot the results or not. Default is `False`.
- `--test`: Whether to test a model or not. Default is `*` - meaning all available models will be tested. Can also be a specific model name to be tested.

## Our Agents

### NEAT
We trained an agent using the NEAT algorithm, which achieved a win rate of 93%.

The configuration we had used for this agent is as follows:

- `neat-config.txt`
    ```text
    [NEAT]
    fitness_criterion     = max
    fitness_threshold     = 22.5
    pop_size              = 200
    reset_on_extinction   = False
    
    [DefaultGenome]
    # node activation options
    activation_default      = tanh
    activation_mutate_rate  = 0.4
    activation_options      = tanh relu
    
    # node aggregation options
    aggregation_default     = sum
    aggregation_mutate_rate = 0.4
    aggregation_options     = sum
    
    # node bias options
    bias_init_mean          = 0.0
    bias_init_stdev         = 1.0
    bias_max_value          = 30.0
    bias_min_value          = -30.0
    bias_mutate_power       = 0.5
    bias_mutate_rate        = 0.3
    bias_replace_rate       = 0.1
    
    # genome compatibility options
    compatibility_disjoint_coefficient = 1.5
    compatibility_weight_coefficient   = 0.5
    
    # connection options
    conn_add_prob           = 0.7
    conn_enable_prob        = 0.2
    conn_initial_connection = unconnected
    conn_weight_init_mean   = 0.0
    conn_weight_init_stdev  = 1.0
    conn_weight_max_value   = 30
    conn_weight_min_value   = -30
    conn_weight_mutate_power= 0.5
    conn_weight_mutate_rate = 0.4
    conn_weight_replace_rate= 0.1
    conn_delete_prob        = 0.2
    enabled_default         = True
    enabled_mutate_rate     = 0.1
    
    # weight initialization options
    weight_init_mean        = 0.0
    weight_init_stdev       = 1.0
    weight_max_value        = 30.0
    weight_min_value        = -30.0
    weight_mutate_power     = 0.5
    weight_mutate_rate      = 0.4
    weight_replace_rate     = 0.1
    
    # node response options
    response_init_mean      = 1.0
    response_init_stdev     = 0.0
    response_max_value      = 30.0
    response_min_value      = -30.0
    response_mutate_power   = 0.5
    response_mutate_rate    = 0.2
    response_replace_rate   = 0.1
    
    # genome node options
    num_hidden              = 3
    num_inputs              = 10
    num_outputs             = 4
    num_initial_nodes       = 0
    initial_connection      = unconnected
    feed_forward            = True
    
    # genome structural mutation options
    structural_mutation_surerate = 0.3
    node_add_prob          = 0.6
    node_disable_prob      = 0.0
    node_delete_prob       = 0.4
    
    # species options
    max_stagnation         = 10
    species_fitness_func   = max
    elitism                = 2
    
    [DefaultReproduction]
    elitism                = 2
    survival_threshold     = 0.1
    
    [DefaultSpeciesSet]
    compatibility_threshold = 3.9
    
    [DefaultStagnation]
    species_fitness_func = max
    max_stagnation = 20
    species_elitism = 2
    ```

- `flags`: `--agent=neat --fps=240 --grid_like=True --with_train=False --with_water=False --lives=5 --neat_config=neat-config.txt --generations=200 --plot=True`

### DQN
