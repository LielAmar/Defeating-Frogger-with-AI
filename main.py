"""
This file is the main entry point for the game. It allows the user to run the game with different agents and settings.
"""
import argparse
import concurrent

import matplotlib.pyplot as plt

from src.agents.dqn.dqn_runner import DQNRunner
from src.agents.human.human_runner import HumanRunner
from src.agents.neat.neat_runner import NEATRunner
from src.agents.onlyup.onlyup_runner import OnlyUpRunner
from src.agents.random.random_runner import RandomRunner


def plot_results(agent_name, results):
    plt.plot(results)
    plt.title(f'{agent_name} Test Results (100 iterations, 100 games each)')
    plt.xlabel('Iteration')
    plt.ylabel('Win Rate')
    plt.show()


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

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run the game in debug mode'
    )

    parser.add_argument(
        '--multi_test',
        action='store_true',
        help='Run the game multiple times to get average results'
    )

    args = parser.parse_args()

    if args.agent == 'neat':
        agent = NEATRunner(settings=args)
    elif args.agent == 'dqn':
        agent = DQNRunner(settings=args)
    elif args.agent == 'onlyup':
        agent = OnlyUpRunner(settings=args)
    elif args.agent == 'random':
        agent = RandomRunner(settings=args)
    elif args.agent == 'human':
        agent = HumanRunner(settings=args)
    else:
        raise Exception('Invalid agent')

    if args.multi_test:
        neat_agent = NEATRunner(settings=args)
        dqn_agent = DQNRunner(settings=args)
        onlyup_agent = OnlyUpRunner(settings=args)
        random_agent = RandomRunner(settings=args)

        neat_results = []
        ddqn_results = []
        onlyup_results = []
        random_results = []


        def run_neat():
            return neat_agent._run_single_test('hard - 8%.pkl')

        def run_ddqn():
            return dqn_agent._run_single_test('hard - 99%.pth')

        def run_onlyup():
            return onlyup_agent.run()

        def run_random():
            return random_agent.run()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(100):
                futures = []

                futures.append(executor.submit(run_neat))
                futures.append(executor.submit(run_ddqn))
                futures.append(executor.submit(run_onlyup))
                futures.append(executor.submit(run_random))

                for future in futures:
                    result = future.result()
                    if future == futures[0]:
                        neat_results.append(result)
                    elif future == futures[1]:
                        ddqn_results.append(result)
                    elif future == futures[2]:
                        onlyup_results.append(result)
                    else:
                        random_results.append(result)

        print(f'NEAT: {neat_results}')
        print(f'DDQN: {ddqn_results}')
        print(f'OnlyUp: {onlyup_results}')
        print(f'Random: {random_results}')

        plt.plot(neat_results, label='NEAT')
        plt.plot(ddqn_results, label='DDQN')
        plt.plot(onlyup_results, label='OnlyUp')
        plt.plot(random_results, label='Random')

        plt.title('Agents Comparison (100 iterations, 100 games each) - Hard Difficulty')
        plt.xlabel('Iteration')
        plt.ylabel('Win Rate')
        plt.legend()
        plt.show()
    else:
        print(f'Running game with agent {args.agent}!')

        agent.run()
