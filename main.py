import argparse
import os

from src.agents.neat.neat_runner import NEATRunner
from src.agents.onlyup.onlyup_runner import OnlyUpRunner
from src.agents.random.random_runner import RandomRunner
from src.constants import ONLY_UP_AGENT_GAMES_TO_PLAY, RANDOM_AGENT_GAMES_TO_PLAY

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the game')

    parser.add_argument('--agent', choices=['neat', 'dqn', 'onlyup', 'random'], default='neat',
                        help='The type of agent to play the game')
    parser.add_argument('--grid_like', action='store_true', help='Run the game in grid mode')
    parser.add_argument('--with_train', action='store_true', help='Run the game with train')

    parser.add_argument('--number_of_generations', type=int, default=200,
                        help='Number of generations to run the NEAT algorithm')

    parser.add_argument('--plot', action='store_true', help='Whether to plot')

    # add an argument that is a string
    parser.add_argument('--test', type=str, default=None,
                        help='Run the game in test mode (either "*" to test all available models or the name of a specific model)')

    args = parser.parse_args()

    print(f'Running game with agent {args.agent}!')

    if args.agent == 'neat':
        runner = NEATRunner(
            grid_like=args.grid_like,
            config_file="neat-config.txt",
            with_train=args.with_train,
            lives_per_player=1 if args.test is not None else 5,
            number_of_generations=args.number_of_generations,
            plot=args.plot
        )

        models_files = []

        if args.test == '*':
            for file in os.listdir('models'):
                if file.endswith('.pkl'):
                    models_files.append(file)
        elif args.test is not None:
            models_files.append(args.test)

        if args.test is not None:
            wins_tracker = dict()

            for model_file in models_files:
                wins_tracker[model_file] = runner.test_run(model_file)

                print(f'{model_file}: won {wins_tracker[model_file]}% of the games')

            print(f'Total Wins: {sum(wins_tracker.values())}')
            print(f'Win Rate: {sum(wins_tracker.values()) / (len(wins_tracker) * 100)}%')

            best_player = max(wins_tracker, key=wins_tracker.get)

            print(f'Best Player Wins: {wins_tracker[best_player]}')
            print(f'Best Player Win Rate: {wins_tracker[best_player] / 100}%')
        else:
            runner.run()

    # elif args.agent == 'dqn':
    #     DQNRunner().run()
    elif args.agent == 'onlyup':
        OnlyUpRunner(
            grid_like=args.grid_like,
            games_to_play=ONLY_UP_AGENT_GAMES_TO_PLAY
        ).run()
    elif args.agent == 'random':
        RandomRunner(
            grid_like=args.grid_like,
            games_to_play=RANDOM_AGENT_GAMES_TO_PLAY
        ).run()
    else:
        print("Invalid Agent argument\nPlease choose from: [neat, dqn, up, random]")
