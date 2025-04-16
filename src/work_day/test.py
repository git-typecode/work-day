import argparse
import os
import sys


def commands(parser: argparse.ArgumentParser):
    # parser = argparse.ArgumentParser(description="Your program description.")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(
        title="Subcommands", dest="command", required=True, metavar="COMMAND"
    )

    # Subparser for the 'update' command
    update_parser = subparsers.add_parser("update", help="Update start or stop time")
    update_parser.add_argument("--start-time", help="Update start time")
    update_parser.add_argument("--stop-time", help="Update stop time")
    update_parser.set_defaults(func=update)

    # Subparser for the 'start' command
    start_parser = subparsers.add_parser("start", help="Start the process")
    start_parser.set_defaults(func=start)

    # Subparser for the 'stop' command
    stop_parser = subparsers.add_parser("stop", help="Stop the process")
    stop_parser.set_defaults(func=stop)

    # Subparser for the 'print' command
    print_parser = subparsers.add_parser("print", help="Print information")
    print_parser.set_defaults(func=print_command)

    # Subparser for the '-c' command
    comment_parser = subparsers.add_parser("c", help="Add a comment")
    comment_parser.add_argument("comment", help="Comment text")
    comment_parser.set_defaults(func=add_comment)

    args = parser.parse_args()

    print(args)

    # Call the appropriate function based on the subcommand
    args.func(args)


def main():
    parser = argparse.ArgumentParser(
        prog="Work Day",
        description="Logs times and activites during a work day.",
        epilog="Work Day at your service",
    )

    commands(parser)


def update(args):
    if args.start_time:
        print(f"Update command executed with start-time: {args.start_time}")
    elif args.stop_time:
        print(f"Update command executed with stop-time: {args.stop_time}")
    else:
        print("Invalid update command")


def start(args):
    print(f"Start command executed: {args.command}")


def stop(args):
    print("Stop command executed")


def print_command(args):
    print("Print command executed")


def add_comment(args):
    print(f"Comment added: {args.comment}")


def tests():

    print("sys.path:")
    print(sys.path)
    print("PYTHONPATH:")
    print(os.getenv("PYTHONPATH"))


if __name__ == "__main__":
    tests()
