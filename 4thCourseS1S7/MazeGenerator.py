import matplotlib.pyplot as plt
import random

class Direction:
	Left = 0
	UP = 1
	Right = 2
	Down = 3

class Cell:
	def __init__(self,x,y,color=0):
		self.x = x
		self.y = y
		self.color = color
		self.walls = [True,True,True,True]
		
	def draw(self):
		x = self.x
		y = self.y
		dir = [0,1]
		for wall in self.walls:
			next_x = x + dir[0]
			next_y = y + dir[1]
			if wall:
				plt.plot([x,next_x],[y,next_y],c='k')
			x = next_x
			y = next_y
			dir[0],dir[1] = dir[1],-dir[0]

class Maze:
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.initGrid()

	def initGrid(self):
		self.maze = []
		for y in range(0,self.height):
			row = []
			for x in range(0,self.width):
				row.append(Cell(x,y,0))
			self.maze.append(row)
			
	def isInGrid(self,x,y):
		return (x >= 0 and y >= 0 and x < self.width and y < self.height)
	
	def depthFirstSearchGeneration(self):
		visited = [[False]*self.width for i in range(self.height)]
		start_x = random.randint(0, self.width-1)
		start_y = random.randint(0, self.height-1)
		stack = [[start_x,start_y]]
		while len(stack) > 0:
			curr_cell = stack[-1]
			visited[curr_cell[1]][curr_cell[0]] = True
			available_cells = []
			available_dirs = []
			dir_x,dir_y = 0,1
			for i in range(4):
				cell_x = curr_cell[0] + dir_x
				cell_y = curr_cell[1] + dir_y
				if self.isInGrid(cell_x,cell_y) and not visited[cell_y][cell_x]:
					available_cells.append([cell_x,cell_y])
					available_dirs.append([dir_x,dir_y])
				dir_x,dir_y = dir_y,-dir_x
			if len(available_cells) == 0:
				stack.pop()
			else:
				next_id = random.randint(0, len(available_cells)-1)
				cell = available_cells[next_id]
				dir = available_dirs[next_id]
				stack.append(cell)
				if dir == [-1,0]:
					self.maze[curr_cell[1]][curr_cell[0]].walls[0] = False
					self.maze[cell[1]][cell[0]].walls[2] = False
				elif dir == [0,1]:
					self.maze[curr_cell[1]][curr_cell[0]].walls[1] = False
					self.maze[cell[1]][cell[0]].walls[3] = False
				elif dir == [1,0]:
					self.maze[curr_cell[1]][curr_cell[0]].walls[2] = False
					self.maze[cell[1]][cell[0]].walls[0] = False
				else:
					self.maze[curr_cell[1]][curr_cell[0]].walls[3] = False
					self.maze[cell[1]][cell[0]].walls[1] = False
					
	def draw(self):
		plt.plot([0,0,self.width,self.width,0],[0,self.height,self.height,0,0],'k')
		for y in range(0,self.height):
			for x in range(0,self.width):
				self.maze[y][x].draw()
		plt.show()
		

if __name__ == "__main__":
	maze = Maze(50,50)
	maze.depthFirstSearchGeneration()
	maze.draw()