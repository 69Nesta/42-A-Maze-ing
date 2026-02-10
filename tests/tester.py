from mazegen import MazeApp
from pytest import CaptureFixture


def test_no_file(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/non_existent_file.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: Config file not found.\n'


def test_too_big(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/too_big.txt')
    captured = capsys.readouterr()
    assert captured.err != ''


def test_entry_point_out_of_bounds(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/entry_point_out_of_bounds.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: Entry coordinates are out of bounds\n'


def test_exit_point_out_of_bounds(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/exit_point_out_of_bounds.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: Exit coordinates are out of bounds\n'


def test_negative_dimensions(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/negative_dimensions.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: Maze dimensions must be positive integers\n'


def test_non_integer_dimensions(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/non_integer_dimensions.txt')
    captured = capsys.readouterr()
    assert captured.err == \
        'Error: Invalid value " 1e" for key "height". On line 5.\n'


def test_missing_parameters(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/missing_parameters.txt')
    captured = capsys.readouterr()
    assert captured.err == \
        'Error: Config file is missing required key: "exit".\n'


def test_invalid_parameter_values(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/invalid_parameter_values.txt')
    captured = capsys.readouterr()
    assert captured.err == \
        'Error: Invalid value "yes" for key "perfect". On line 20.\n'


def test_too_small(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/too_small.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: Maze dimensions must be at least 5x5\n'


def test_logo_too_big(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/logo_too_big.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: The logo is too big\n'


def test_logo_on_entry_or_exit(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/logo_on_entry_or_exit.txt')
    captured = capsys.readouterr()
    assert captured.err == \
        'Error: The logo can t be on the exit or the start\n'


def test_logo_inaccessible_areas(capsys: CaptureFixture[str]) -> None:
    MazeApp('tests/logo_inaccessible_areas.txt')
    captured = capsys.readouterr()
    assert captured.err == \
        'Error: Logo invalid, there must be no inaccessible areas\n'
