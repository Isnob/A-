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
    generate.add_argument("--width", type=int, default=50)
    generate.add_argument("--height", type=int, default=20)
    generate.add_argument("--start-x", type=int, default=1)
    generate.add_argument("--start-y", type=int, default=1)
    generate.add_argument("--finish-x", type=int, default=40)
    generate.add_argument("--finish-y", type=int, default=18)
    generate.add_argument("--density", type=float, default=0.5)

    simulate = subparsers.add_parser("run_cli_simulation")
    simulate.add_argument("name")
    simulate.add_argument("algorithm", choices=["astar", "bfs", "dijkstra"])
    simulate.add_argument("delay", type=float)

    delete = subparsers.add_parser("delete")
    delete.add_argument("name")

    return parser


def main():
    args = build_parser().parse_args()
    manager = Manager()

    if args.command == "generate":
        manager.generate_and_write_maze(
            args.name,
            CONFIG_PATH,
            width=args.width,
            height=args.height,
            start=(args.start_x, args.start_y),
            finish=(args.finish_x, args.finish_y),
            density=args.density,
        )
    elif args.command == "run_cli_simulation":
        manager.run_cli_simulation(args.name, CONFIG_PATH, algorithm=args.algorithm, delay=args.delay)
    elif args.command == "delete":
        manager.delete_maze(args.name, CONFIG_PATH)


if __name__ == "__main__":
    main()
