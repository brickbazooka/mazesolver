import unittest

from main import Maze, Point

class Tests(unittest.TestCase):
    def test_maze_create_cells_5x5(self):
        num_cols = 5
        num_rows = 5
        m2 = Maze(Point(0, 0), num_rows, num_cols, 10, 10)
        self.assertEqual(len(m2._cells), num_cols)
        self.assertEqual(len(m2._cells[0]), num_rows)

    def test_maze_create_cells_12x10(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)
    
    def test_maze_create_cells_15x10(self):
        num_cols = 15
        num_rows = 10
        m3 = Maze(Point(0, 0), num_rows, num_cols, 10, 10)
        self.assertEqual(len(m3._cells), num_cols)
        self.assertEqual(len(m3._cells[0]), num_rows)

if __name__ == "__main__":
    unittest.main()