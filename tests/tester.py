from mazegen import MazeApp


def test_no_file(capsys):
    MazeApp('tests/non_existent_file.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: Config file not found.\n'


def test_too_big(capsys):
    MazeApp('tests/too_big.txt')
    captured = capsys.readouterr()
    assert captured.err != ''


def test_entry_point_out_of_bounds(capsys):
    MazeApp('tests/entry_point_out_of_bounds.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: Entry coordinates are out of bounds\n'


def test_exit_point_out_of_bounds(capsys):
    MazeApp('tests/exit_point_out_of_bounds.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: Exit coordinates are out of bounds\n'


def test_negative_dimensions(capsys):
    MazeApp('tests/negative_dimensions.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: Maze dimensions must be positive integers\n'


def test_non_integer_dimensions(capsys):
    MazeApp('tests/non_integer_dimensions.txt')
    captured = capsys.readouterr()
    assert captured.err == \
        'Error: Invalid value " 1e" for key "height". On line 5.\n'


def test_missing_parameters(capsys):
    MazeApp('tests/missing_parameters.txt')
    captured = capsys.readouterr()
    assert captured.err == \
        'Error: Config file is missing required key: "exit".\n'


def test_invalid_parameter_values(capsys):
    MazeApp('tests/invalid_parameter_values.txt')
    captured = capsys.readouterr()
    assert captured.err == \
        'Error: Invalid value "yes" for key "perfect". On line 20.\n'


def test_too_small(capsys):
    MazeApp('tests/too_small.txt')
    captured = capsys.readouterr()
    assert captured.err == 'Error: list index out of range\n'
