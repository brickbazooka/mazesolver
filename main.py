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


def main():
	window = Window(800, 600)

	black_line = Line(Point(100, 100), Point(200, 200))
	window.draw_line(line=black_line, fill_color="black")

	red_line = Line(Point(200, 200), Point(300, 100))
	window.draw_line(line=red_line, fill_color="red")

	blue_line = Line(Point(300, 100), Point(400, 200))
	window.draw_line(line=blue_line, fill_color="blue")

	yellow_line = Line(Point(400, 200), Point(500, 100))
	window.draw_line(line=yellow_line, fill_color="yellow")

	window.wait_for_close()


if __name__ == "__main__":
	main()