import time
from tkinter import Tk, BOTH, Canvas


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

	def draw_move(self, to_cell, undo=False):
		if not self._win:
			return
		start_x = (self._top_left.x + self._bottom_right.x) // 2
		start_y = (self._top_left.y + self._bottom_right.y) // 2
		end_x = (to_cell._top_left.x + to_cell._bottom_right.x) // 2
		end_y = (to_cell._top_left.y + to_cell._bottom_right.y) // 2

		color = "gray" if undo else "red"
		self._win.draw_line(
			Line(Point(start_x, start_y), Point(end_x, end_y)),
			fill_color=color
		)


class Maze:
	def __init__(
			self,
			origin,
			num_rows, num_cols,
			cell_size_x, cell_size_y,
			window=None
		):
		self.origin = origin
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.cell_size_x = cell_size_x
		self.cell_size_y = cell_size_y
		self.win = window
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
		self._animate()

	def _animate(self):
		if not self.win:
			return
		self.win.redraw()
		time.sleep(0.05)

	def _break_entrance_and_exit(self):
		self._cells[0][0].has_top_wall = False
		self._draw_cell(0, 0)
		self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
		self._draw_cell(self.num_cols - 1, self.num_rows - 1)


def main():
	window = Window(800, 600)
	maze = Maze(Point(50, 50), 10, 10, 50, 50, window)
	maze._break_entrance_and_exit()
	window.wait_for_close()


if __name__ == "__main__":
	main()