# AI Learns to Play Frogger

Hello!

This project is a simple implementation of a frogger-like game, with two AI agents that learn to play it using Deep Q-learning and NEAT.
It was developed by Tomer Meidan, Omer Ferster and I, from The Hebrew University of Jerusalem, as part of the course "Introduction to Artificial Intelligence" (2024).

## Installation
To install the required packages, use your favorite package manager with python 3.12 to initialize a new environment.
Then, run the following command to install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration
There are several configuration flags that can be inputted to the program, to change the behavior of the game and the learning algorithms.
The flags are as follows:
- `--agent`: The agent to use. Can be either `dqn`, `neat`, `random`, `onlyup` or `human`. Default is `random`.
- `--fps`: The frames per second of the game. Default is 5.
- `--grid_like`: Whether to use a grid-like environment or a continuous one. Default is `False`.
- `--train`: Whether to include the train obstacle or not. Default is `False`.
- `--neat_config`: The configuration file for NEAT. Default is `neat-config.txt`.
- `--generations`: The number of generations to run NEAT for. Default is 200.
- `--plot`: Whether to plot the results or not. Default is `False`.
- `--test`: Whether to test a model or not. Default is None. `*` tests all available models will be tested. Can also be a specific model name to be tested.
- `--multi_test`: Whether to test multiple models or not. Default is `False`.

* Note that when the game runs, you can click on "space" to change the speed of the game from 5 fps to the original fps given under the `fps` flag.

## Difficulties

The game has three difficulties:

1. **Easy**: The basic difficulty, with cars moving horizontally.
2. **Medium**: The intermediate difficulty, with cars moving horizontally and a train moving horizontally.
3. **Hard**: The hardest difficulty, with cars moving horizontally, a train moving horizontally and logs moving vertically.

To change the difficulty, you can change the `--train` flag to `True` and `--water` to `True`.

## Gameplay
<video width="320" height="240" controls>
  <source src="videos/gameplay.mp4" type="video/mp4">
</video>

## Our Agents

During our time working on the project, we tweaked and tuned our agents to achieve the best results possible. Here are the results of our base agents and best agents:

### Random Agent

#### Information
The random agent is the first base-line agent we decided to implement. It simply chooses a random action from the available actions at each time step. The win rate of this agent is 0% even with only the cars obstacle.

#### Testing
To run this model, use the following command:

```bash
python main.py --agent=random --grid_like --fps=500 --lives=1 --games=100
```

### Only Up Agent

#### Information
The only up agent is the second base-line agent we decided to implement. It simply chooses the "up" action at each time step. The win rate of this agent is ~40% with only the cars obstacle, ~40% with cars and a train and 0% win rate with cars, train and water section.
The reason this agent has a higher win rate than the random agent is because sometimes, going just up is enough to avoid all cars. However, most times the agent will encounter obstacles, and the only-up agent, has no idea how to deal with them.

#### Testing
To run this model, use the following command:

```bash
python main.py --agent=onlyup --grid_like --fps=500 --lives=1 --games=100
```

### NEAT

#### Information
The best agents we managed to train using the NEAT algorithm achieved the following:
1. In easy mode, the best agent achieved a win rate of 99%.
2. In medium mode, the best agent achieved a win rate of 72%.
3. In hard mode, the best agent achieved a win rate of 8%.

In this section, we'll go over the exact configuration and code that lead to us getting these results.

#### Testing
You can test these models yourself. They are included in this project under: `models/neat/`:
1. `models/neat/easy - 99%.pkl`
2. `models/neat/medium - 72%.pkl`
3. `models/neat/hard - 8%.pkl`

To run any model, use the following command (replace with desired model name):

```bash
python main.py --agent=neat --grid_like --fps=500 --lives=1 --games=100 --test="easy - 99%.pkl" [--train] [--water]
```

#### Training

Let's go over the main parts of the training of this model:

1. Run command:
    ```bash
    python main.py --agent=neat --grid_like --fps=500 --lives=3 --generations=300 --plot [--train] [--water]
    ```

2. Configuration file: `neat-config.txt`

3. State representation: `src/agents/neat/neat_player.py`

4. Fitness function: `src/agents/neat/neat_game.py`

#### Plots

The following are the plots of the training of the NEAT algorithm, for each difficulty - easy, medium and hard respectively:

<img src="./graphs/easy%20-%20neat%20training.png" width="300">
<br>
<img src="./graphs/medium%20-%20neat%20training.png" width="300">
<br>
<img src="./graphs/hard%20-%20neat%20training.png" width="300">

As you can see, in the easy task, NEAT was able to converge to a good solution pretty quickly, and the more complexity we introduce, the more the algorithm struggles.

### DQN

#### Information

The best agents we managed to train using the DDQN algorithm achieved the following:
1. In easy mode, the best agent achieved a win rate of 100%.
2. In medium mode, the best agent achieved a win rate of 100%.
3. In hard mode, the best agent achieved a win rate of 99%.

In this section, we'll go over the exact configuration and code that lead to us getting these results.

* It is important to note that the exact variation of the DQN algorithm we used is the Double DQN algorithm.

#### Testing
You can test these models yourself. They are included in this project under: `models/dqn/`:
1. `models/dqn/easy - 100%.pkl`
2. `models/dqn/medium - 100%.pkl`
3. `models/dqn/hard - 99%.pkl`

To run any model, use the following command (replace with desired model name):

```bash
python main.py --agent=dqn --grid_like --fps=500 --lives=1 --games=100 --test="easy - 100%.pth" [--train] [--water]
```

#### Training

Let's go over the main parts of the training of this model:
1. Run command:
    ```bash
    python main.py --agent=dqn --grid_like --fps=500 --lives=1 --games=2000 --plot [--train] [--water]
    ```

2. Model: `src/agents/dqn/dqn_model.py`:

3. Agent: `src/agents/dqn/dqn_agent.py`:

4. State representation: `src/agents/dqn/dqn_player.py`

5. Reward function: `src/agents/dqn/dqn_game.py`

#### Plots
The following are the plots of the training of the NEAT algorithm, for each difficulty - easy, medium and hard respectively:

<img src="./graphs/easy%20-%20ddqn%20training.png" width="300">
<br>
<img src="./graphs/medium%20-%20ddqn%20training.png" width="300">
<br>
<img src="./graphs/hard%20-%20ddqn%20training.png" width="300">

It is noticeable that the DQN algorithm was able to converge to a good solution pretty quickly in the easy task, requiring just 1000 episodes.
However, it took way longer in the medium and hard tasks, requiring 4000 and 6000 episodes respectively.

It did, however, reached very good results overall compared to NEAT.

## Comparison

### Easy Difficulty
<img src="./graphs/easy%20-%20models%20comparison.png" width="300">
<br>

### Medium Difficulty
<img src="./graphs/medium%20-%20models%20comparison.png" width="300">
<br>

### Hard Difficulty
<img src="./graphs/hard%20-%20models%20comparison.png" width="300">

We can see that the DQN algorithm was able to achieve better results than the NEAT algorithm in all difficulties.
The two base-line agents, random and only-up, struggled to achieve good results and shuttered completely in the hard difficulty.

## Gallery

This section shows some images from the game:

<img src="./images/car%20section%20state.png" width="250">
<img src="./images/train%20section%20state.png" width="250">
<img src="./images/water%20section%20state.png" width="250">
