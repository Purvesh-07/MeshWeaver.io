from meshweaver.cli import build_parser


def test_parser():

    parser = build_parser()

    assert parser is not None


def test_start_command():

    parser = build_parser()

    args = parser.parse_args(["start"])

    assert args.command == "start"


def test_submit_command():

    parser = build_parser()

    args = parser.parse_args(["submit"])

    assert args.command == "submit"


def test_status_command():

    parser = build_parser()

    args = parser.parse_args(["status"])

    assert args.command == "status"