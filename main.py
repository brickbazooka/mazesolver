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
	def __init__(self, top_left, bottom_right, window):
		self._top_left = top_left
		self._bottom_right = bottom_right

		self._win = window

		self.has_left_wall = True
		self.has_right_wall = True
		self.has_top_wall = True
		self.has_bottom_wall = True

	def draw(self):
		top_left = self._top_left
		bottom_right = self._bottom_right

		top_right = Point(bottom_right.x, top_left.y)
		bottom_left = Point(top_left.x, bottom_right.y)

		if self.has_top_wall:
			self._win.draw_line(Line(top_left, top_right))
		if self.has_right_wall:
			self._win.draw_line(Line(top_right, bottom_right))
		if self.has_bottom_wall:
			self._win.draw_line(Line(bottom_right, bottom_left))
		if self.has_left_wall:
			self._win.draw_line(Line(bottom_left, top_left))

	def draw_move(self, to_cell, undo=False):
		start_x = (self._top_left.x + self._bottom_right.x) // 2
		start_y = (self._top_left.y + self._bottom_right.y) // 2
		end_x = (to_cell._top_left.x + to_cell._bottom_right.x) // 2
		end_y = (to_cell._top_left.y + to_cell._bottom_right.y) // 2

		color = "gray" if undo else "red"
		self._win.draw_line(Line(Point(start_x, start_y), Point(end_x, end_y)), fill_color=color)


def main():
	window = Window(800, 600)

	cell1 = Cell(Point(50, 50), Point(150, 150), window)
	cell1.has_top_wall = False
	cell1.draw()

	cell2 = Cell(Point(200, 50), Point(300, 150), window)
	cell2.has_right_wall = False
	cell2.draw()

	cell3 = Cell(Point(350, 50), Point(450, 150), window)
	cell3.has_bottom_wall = False
	cell3.draw()

	cell4 = Cell(Point(500, 50), Point(600, 150), window)
	cell4.has_left_wall = False
	cell4.draw()

	cell5 = Cell(Point(50, 200), Point(150, 300), window)
	cell5.has_top_wall = False
	cell5.has_right_wall = False
	cell5.draw()

	cell6 = Cell(Point(200, 200), Point(300, 300), window)
	cell6.has_right_wall = False
	cell6.has_bottom_wall = False
	cell6.draw()

	cell7 = Cell(Point(350, 200), Point(450, 300), window)
	cell7.has_bottom_wall = False
	cell7.has_left_wall = False
	cell7.draw()

	cell8 = Cell(Point(500, 200), Point(600, 300), window)
	cell8.has_left_wall = False
	cell8.has_top_wall = False
	cell8.draw()

	cell9 = Cell(Point(50, 350), Point(150, 450), window)
	cell9.draw()

	window.wait_for_close()


if __name__ == "__main__":
	main()