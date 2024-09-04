import argparse

from src.agents.human.human_runner import HumanRunner
from src.agents.neat.neat_runner import NEATRunner
from src.agents.onlyup.onlyup_runner import OnlyUpRunner
from src.agents.random.random_runner import RandomRunner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the game')

    parser.add_argument(
        '--agent',
        choices=['neat', 'dqn', 'onlyup', 'random', 'human'],
        default='random',
        help='The type of agent to play the game'
    )

    # Settings
    parser.add_argument('--fps', type=int, default=5, help='Frames per second')
    parser.add_argument('--grid_like', action='store_true', help='Run the game in grid mode')
    parser.add_argument('--train', action='store_true', help='Run the game with train')
    parser.add_argument('--water', action='store_true', help='Run the game with water section')
    parser.add_argument('--games', type=int, default=3, help='Number of games to play')
    parser.add_argument('--lives', type=int, default=5, help='Number of lives per player')
    parser.add_argument('--neat_config', type=str, default='neat-config.txt', help='NEAT configuration file')
    parser.add_argument(
        '--generations',
        type=int,
        default=200,
        help='Number of generations to run the NEAT algorithm'
    )
    parser.add_argument(
        '--plot',
        action='store_true',
        help='Whether to plot'
    )

    parser.add_argument(
        '--test',
        type=str,
        default=None,
        help='Run the game in test mode (either "*" to test all available models or the name of a specific model)'
    )

    args = parser.parse_args()

    if args.agent == 'neat':
        # for i in range(50):
        agent = NEATRunner(settings=args)
    elif args.agent == 'dqn':
        raise Exception('DQN not implemented yet')
    elif args.agent == 'onlyup':
        agent = OnlyUpRunner(settings=args)
    elif args.agent == 'random':
        agent = RandomRunner(settings=args)
    elif args.agent == 'human':
        agent = HumanRunner(settings=args)
    else:
        raise Exception('Invalid agent')

    print(f'Running game with agent {args.agent}!')

    agent.run()
