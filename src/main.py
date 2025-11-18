import argparse
import pathlib

from src.core.manager import Manager

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


def build_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate")
    generate.add_argument("name")

    simulate = subparsers.add_parser("simulate")
    simulate.add_argument("name")
    simulate.add_argument("algorithm", choices=["astar", "bfs", "dijkstra"])
    simulate.add_argument("delay")

    delete = subparsers.add_parser("delete")
    delete.add_argument("name")

    return parser


def main():
    args = build_parser().parse_args()
    manager = Manager()

    if args.command == "generate":
        manager.generate_and_write_maze(args.name, CONFIG_PATH)
    elif args.command == "simulate":
        manager.start_simulation(args.name, CONFIG_PATH, algorithm=args.algorithm, delay=args.delay)
    elif args.command == "delete":
        manager.delete_maze(args.name, CONFIG_PATH)


if __name__ == "__main__":
    main()
