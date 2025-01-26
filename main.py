import time
import random
from tkinter import Tk, BOTH, Canvas
from collections import deque


class Window:
	def __init__(self, width, height):
		self.__root = Tk()
		self.__root.title("Maze Solver")
		self.__root.protocol("WM_DELETE_WINDOW", self.close)

		self.canvas = Canvas(self.__root, width=width, height=height)
		self.canvas.pack(fill=BOTH, expand=True)
		
		self.running = False

	def redraw(self):
		self.__root.update_idletasks()
		self.__root.update()
		return

	def draw_line(self, line, fill_color="black", width=2):
		line.draw(self.canvas, fill_color, width)

	def wait_for_close(self):
		self.running = True
		while self.running:
			self.redraw()

	def close(self):
		self.running = False


class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y


class Line:
	def __init__(self, start, end):
		self.start = start
		self.end = end
	
	def draw(self, canvas, fill_color, width=2):
		canvas.create_line(
			self.start.x,
			self.start.y,
			self.end.x,
			self.end.y,
			fill=fill_color,
			width=width
		)


class Cell:
	def __init__(self, top_left, bottom_right, window=None):
		self._top_left = top_left
		self._bottom_right = bottom_right

		self._win = window

		self.has_left_wall = True
		self.has_right_wall = True
		self.has_top_wall = True
		self.has_bottom_wall = True
		self.visited = False

	def draw(self):
		if not self._win:
			return
		top_left = self._top_left
		bottom_right = self._bottom_right

		top_right = Point(bottom_right.x, top_left.y)
		bottom_left = Point(top_left.x, bottom_right.y)

		bg_color = "#d9d9d9"  # Background color

		if self.has_top_wall:
			self._win.draw_line(Line(top_left, top_right))
		else:
			self._win.draw_line(Line(top_left, top_right), fill_color=bg_color)
		if self.has_right_wall:
			self._win.draw_line(Line(top_right, bottom_right))
		else:
			self._win.draw_line(Line(top_right, bottom_right), fill_color=bg_color)
		if self.has_bottom_wall:
			self._win.draw_line(Line(bottom_right, bottom_left))
		else:
			self._win.draw_line(Line(bottom_right, bottom_left), fill_color=bg_color)
		if self.has_left_wall:
			self._win.draw_line(Line(bottom_left, top_left))
		else:
			self._win.draw_line(Line(bottom_left, top_left), fill_color=bg_color)

	def draw_move(self, to_cell, undo=False, width=2):
		if not self._win:
			return
		start_x = (self._top_left.x + self._bottom_right.x) // 2
		start_y = (self._top_left.y + self._bottom_right.y) // 2
		end_x = (to_cell._top_left.x + to_cell._bottom_right.x) // 2
		end_y = (to_cell._top_left.y + to_cell._bottom_right.y) // 2

		bg_color = "#d9d9d9"  # Background color
		color = "gray" if undo else "red"
		
		if undo:
			self._win.draw_line(
				Line(Point(start_x, start_y), Point(end_x, end_y)),
				fill_color=bg_color,
				width=width
			)
			# Display the "undo" move
			self._win.draw_line(
				Line(Point(start_x, start_y), Point(end_x, end_y)),
				fill_color=color,
				width=2
			)
		else:
			self._win.draw_line(
				Line(Point(start_x, start_y), Point(end_x, end_y)),
				fill_color=color,
				width=width
			)


class Maze:
	def __init__(
			self,
			origin,
			num_rows, num_cols,
			cell_size_x, cell_size_y,
			window=None,
			seed=None
		):
		self.origin = origin
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.cell_size_x = cell_size_x
		self.cell_size_y = cell_size_y
		self.win = window
		if seed is not None:
			random.seed(seed)
		self._cells = []
		self._create_cells()

	def _create_cells(self):
		for i in range(self.num_cols):
			column = []
			for j in range(self.num_rows):
				column.append(Cell(Point(0, 0), Point(0, 0), self.win))
			self._cells.append(column)
		for i in range(self.num_cols):
			for j in range(self.num_rows):
				self._draw_cell(i, j)

	def _draw_cell(self, i, j):
		x0 = self.origin.x + i * self.cell_size_x
		y0 = self.origin.y + j * self.cell_size_y
		x1 = x0 + self.cell_size_x
		y1 = y0 + self.cell_size_y
		self._cells[i][j]._top_left = Point(x0, y0)
		self._cells[i][j]._bottom_right = Point(x1, y1)
		self._cells[i][j].draw()
		self._animate(sleep_time=0.01)

	def _animate(self, no_sleep=False, sleep_time=0.05):
		if not self.win:
			return
		self.win.redraw()
		if no_sleep:
			return
		time.sleep(sleep_time)
		return

	def _break_entrance_and_exit(self):
		self._cells[0][0].has_top_wall = False
		self._draw_cell(0, 0)
		self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
		self._draw_cell(self.num_cols - 1, self.num_rows - 1)

	def _break_walls_r(self, i, j):
		self._cells[i][j].visited = True
		while True:
			directions = []
			if i > 0 and not self._cells[i - 1][j].visited:
				directions.append((-1, 0))
			if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
				directions.append((1, 0))
			if j > 0 and not self._cells[i][j - 1].visited:
				directions.append((0, -1))
			if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
				directions.append((0, 1))

			if not directions:
				self._draw_cell(i, j)
				return

			di, dj = random.choice(directions)
			ni, nj = i + di, j + dj

			if di == -1:
				self._cells[i][j].has_left_wall = False
				self._cells[ni][nj].has_right_wall = False
			elif di == 1:
				self._cells[i][j].has_right_wall = False
				self._cells[ni][nj].has_left_wall = False
			elif dj == -1:
				self._cells[i][j].has_top_wall = False
				self._cells[ni][nj].has_bottom_wall = False
			elif dj == 1:
				self._cells[i][j].has_bottom_wall = False
				self._cells[ni][nj].has_top_wall = False
			self._draw_cell(i, j)
			self._draw_cell(ni, nj)

			self._break_walls_r(ni, nj)

	def _reset_cells_visited(self):
		for i in range(self.num_cols):
			for j in range(self.num_rows):
				self._cells[i][j].visited = False

	def break_walls(self):
		self._break_walls_r(0, 0)
		self._reset_cells_visited()

	def _solve_dfs_r(self, i, j):
		# self._animate()
		self._cells[i][j].visited = True

		if i == self.num_cols - 1 and j == self.num_rows - 1:
			return True

		directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		for di, dj in directions:
			ni, nj = i + di, j + dj
			if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows and not self._cells[ni][nj].visited:
				if (di == -1 and not self._cells[i][j].has_left_wall) or \
				   (di == 1 and not self._cells[i][j].has_right_wall) or \
				   (dj == -1 and not self._cells[i][j].has_top_wall) or \
				   (dj == 1 and not self._cells[i][j].has_bottom_wall):
					self._cells[i][j].draw_move(self._cells[ni][nj], width=8)
					self._animate(sleep_time=0.1)
					if self._solve_dfs_r(ni, nj):
						return True
					self._cells[i][j].draw_move(self._cells[ni][nj], undo=True, width=8)
					self._animate(sleep_time=0.1)

		return False

	def solve_dfs(self):
		return self._solve_dfs_r(0, 0)

	def _solve_bfs(self):
		queue = deque([(0, 0)])
		visited = set((0, 0))
		parent = {}

		while queue:
			i, j = queue.popleft()
			if (i, j) == (self.num_cols - 1, self.num_rows - 1):
				self._trace_bfs_path(parent, i, j)
				return True

			for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
				ni, nj = i + di, j + dj
				if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows and (ni, nj) not in visited:
					if (di == -1 and not self._cells[i][j].has_left_wall) or \
					   (di == 1 and not self._cells[i][j].has_right_wall) or \
					   (dj == -1 and not self._cells[i][j].has_top_wall) or \
					   (dj == 1 and not self._cells[i][j].has_bottom_wall):
						queue.append((ni, nj))
						visited.add((ni, nj))
						parent[(ni, nj)] = (i, j)
						self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)
						self._animate(sleep_time=0.1)

		return False

	def _trace_bfs_path(self, parent, i, j):
		trace_path = [(i, j)]
		current = (i, j)
		while parent.get(current, None) is not None and current != (0, 0):
			previous = parent[current]
			trace_path.append(previous)
			current = previous

		trace_path.reverse()
		for (ri, rj), (ni, nj) in zip(trace_path, trace_path[1:]):
			self._cells[ri][rj].draw_move(self._cells[ni][nj], width=8)
			self._animate()

	def solve_bfs(self):
		return self._solve_bfs()


def main():
	window = Window(800, 600)
	maze = Maze(Point(50, 50), 10, 10, 50, 50, window, seed=25)
	maze._break_entrance_and_exit()
	maze.break_walls()
	# maze.solve_dfs()
	maze.solve_bfs()
	window.wait_for_close()


if __name__ == "__main__":
	main()