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

    def test_maze_entrance_and_exit(self):
        num_cols = 5
        num_rows = 5
        m4 = Maze(Point(0, 0), num_rows, num_cols, 10, 10)
        m4._break_entrance_and_exit()
        self.assertFalse(m4._cells[0][0].has_top_wall)
        self.assertFalse(m4._cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_reset_cells_visited(self):
        num_cols = 5
        num_rows = 5
        m5 = Maze(Point(0, 0), num_rows, num_cols, 10, 10)
        m5._break_walls_r(0, 0)
        m5._reset_cells_visited()
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(m5._cells[i][j].visited)

if __name__ == "__main__":
    unittest.main()