import argparse


def build_parser():

    parser = argparse.ArgumentParser(
        prog="meshweaver",
        description="MeshWeaver CLI",
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    subparsers.add_parser(
        "start",
        help="start a node",
    )

    subparsers.add_parser(
        "submit",
        help="submit a task",
    )

    subparsers.add_parser(
        "status",
        help="show mesh status",
    )

    return parser


def main():

    parser = build_parser()

    args = parser.parse_args()

    if args.command == "start":
        print("starting node")

    elif args.command == "submit":
        print("submitting task")

    elif args.command == "status":
        print("showing status")

    else:
        parser.print_help()