import numpy as np
import matplotlib.pyplot as plt
import random

def grad(count):
	pw = 5
	colors = []	
	for i in range(count):
		c = float(255*i)/count
		color = "#{0:02x}{1:02x}{2:02x}".format(int(((255-c)*255)**(0.5)), int((255-c)**pw/255**(pw-1)), int((255-c)**pw/255**(pw-1)))
		colors += [color]
	return colors

Dirs = [[-1,0],[0,1],[1,0],[0,-1]]

class Cell:
	def __init__(self,x,y,color=0):
		self.x = x
		self.y = y
		self.color = color
		self.walls = [True,True,True,True]
		
	def draw(self):
		x = self.x
		y = self.y
		for i in range(4):
			next_x = x + Dirs[(i+1)%4][0]
			next_y = y + Dirs[(i+1)%4][1]
			if self.walls[i]:
				plt.plot([x,next_x],[y,next_y],c='k')
			x = next_x
			y = next_y

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
			
	def getRandomPosition(self):
		start_x = random.randint(0, self.width-1)
		start_y = random.randint(0, self.height-1)
		return [start_x,start_y]
			
	def isInGrid(self,x,y):
		return (x >= 0 and y >= 0 and x < self.width and y < self.height)
	
	def depthFirstSearchGeneration(self):
		visited = [[False]*self.width for i in range(self.height)]
		start = self.getRandomPosition()
		stack = [start]
		while len(stack) > 0:
			x = stack[-1][0]
			y = stack[-1][1]
			visited[y][x] = True
			available_dirs = []
			for i in range(4):
				cell_x = x + Dirs[i][0]
				cell_y = y + Dirs[i][1]
				if self.isInGrid(cell_x,cell_y) and not visited[cell_y][cell_x]:
					available_dirs.append(i)
			if len(available_dirs) == 0:
				stack.pop()
			else:
				next_id = random.choice(available_dirs)
				next_x = x + Dirs[next_id][0]
				next_y = y + Dirs[next_id][1]
				stack.append([next_x,next_y])
				self.maze[y][x].walls[next_id] = False
				self.maze[next_y][next_x].walls[(next_id+2)%4] = False
					
	def drawPath(self):
		visited = [[False]*self.width for i in range(self.height)]
		start = self.getRandomPosition()
		finish = self.getRandomPosition()
		stack = [start]
		while stack[-1] != finish:
			x = stack[-1][0]
			y = stack[-1][1]
			visited[y][x] = True
			ok = False
			for i in range(4):
				next_x = x + Dirs[i][0]
				next_y = y + Dirs[i][1]
				wall = self.maze[y][x].walls[i]
				if not wall and self.isInGrid(next_x,next_y) and not visited[next_y][next_x]:
					stack.append([next_x,next_y])
					ok = True
					break
			if not ok:
				stack.pop()
		stack = np.array(stack) + [0.5,0.5]
		plt.scatter(stack[:,0],stack[:,1],c=grad(stack.shape[0]))
		plt.scatter(start[0] + 0.5,start[1] + 0.5,c='g',s=30)
		plt.scatter(finish[0] + 0.5,finish[1] + 0.5,c='b',s=30)
					
					
	def draw(self):
		plt.plot([0,0,self.width,self.width,0],[0,self.height,self.height,0,0],'k')
		for y in range(0,self.height):
			for x in range(0,self.width):
				self.maze[y][x].draw()
		self.drawPath()
		plt.show()
		

if __name__ == "__main__":
	maze = Maze(100,100)
	maze.depthFirstSearchGeneration()
	maze.draw()