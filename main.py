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

        def run_neat() -> tuple[int, list[int]]:
            return neat_agent._run_single_test('hard - 8%.pkl')

        def run_ddqn() -> tuple[int, list[int]]:
            return dqn_agent._run_single_test('hard - 99%.pth')

        def run_onlyup() -> tuple[int, list[int]]:
            return onlyup_agent.run()

        def run_random() -> tuple[int, list[int]]:
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

        print('NEAT Results:', neat_results)
        print('DDQN Results:', ddqn_results)
        print('OnlyUp Results:', onlyup_results)
        print('Random Results:', random_results)

        neat_wins = sum([wins for wins, remaining_steps in neat_results])
        ddqn_wins = sum([wins for wins, remaining_steps in ddqn_results])
        onlyup_wins = sum([wins for wins, remaining_steps in onlyup_results])
        random_wins = sum([wins for wins, remaining_steps in random_results])

        neat_average_win_rate = neat_wins / len(neat_results)
        ddqn_average_win_rate = ddqn_wins / len(neat_results)
        onlyup_average_win_rate = onlyup_wins / len(neat_results)
        random_average_win_rate = random_wins / len(neat_results)

        neat_average_remaining_steps = sum([remaining_steps for wins, remaining_steps in neat_results]) / len(neat_results)
        ddqn_average_remaining_steps = sum([remaining_steps for wins, remaining_steps in ddqn_results]) / len(neat_results)
        onlyup_average_remaining_steps = sum([remaining_steps for wins, remaining_steps in onlyup_results]) / len(neat_results)
        random_average_remaining_steps = sum([remaining_steps for wins, remaining_steps in random_results]) / len(neat_results)

        plt.plot([wins for wins, remaining_steps in neat_results], label='NEAT')
        plt.plot([wins for wins, remaining_steps in ddqn_results], label='DDQN')
        plt.plot([wins for wins, remaining_steps in onlyup_results], label='OnlyUp')
        plt.plot([wins for wins, remaining_steps in random_results], label='Random')

        print(f'NEAT: {neat_average_win_rate} wins, {neat_average_remaining_steps} remaining steps')
        print(f'DDQN: {ddqn_average_win_rate} wins, {ddqn_average_remaining_steps} remaining steps')
        print(f'OnlyUp: {onlyup_average_win_rate} wins, {onlyup_average_remaining_steps} remaining steps')
        print(f'Random: {random_average_win_rate} wins, {random_average_remaining_steps} remaining steps')

        plt.title('Agents Comparison (100 iterations, 100 games each) - Hard Difficulty')
        plt.xlabel('Iteration')
        plt.ylabel('Win Rate')
        plt.legend()
        plt.show()
    else:
        print(f'Running game with agent {args.agent}!')

        agent.run()
