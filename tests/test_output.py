import os

def test_maze_map_exists():
    assert os.path.exists("/app/maze_map.txt"), "maze_map.txt not found"

def test_maze_map_not_empty():
    with open("/app/maze_map.txt") as f:
        data = f.read().strip()
    assert len(data) > 0, "maze_map.txt is empty"

def test_maze_has_walls():
    with open("/app/maze_map.txt") as f:
        data = f.read()
    assert "#" in data, "Maze does not contain walls"
