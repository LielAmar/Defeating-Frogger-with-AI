import os

import argparse

from dqn_runner import DQNRunner
from neat_runner import NEATRunner


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")
    runner = NEATRunner(config_path)
    runner.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the game')

    parser.add_argument('--agent', choices=['neat', 'dqn'], default='neat', help='The type of agent to play the game')
    parser.add_argument('--test', action='store_true', help='Run the game in test mode')

    args = parser.parse_args()

    print(f'Running game with agent {args.agent}!')

    if args.agent == 'neat':
        if args.test:
            NEATRunner("neat-config.txt").test_run()
        else:
            NEATRunner("neat-config.txt").run()
    elif args.agent == 'dqn':
        DQNRunner().run()
