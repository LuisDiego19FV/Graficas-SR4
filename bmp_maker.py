#bmp_maker
#Por Luis Diego Fernandez
#v-2-19-19
import sys
import math
import struct
import random

class bmpImage:

	# Define init(). Attributes Initializer
	def __init__(self):
		# image data
		self.image_data = bytes()

		# image attributes
		self.width = 400
		self.height = 400
		self.bits_per_pixel = 32
		self.row_bytes = 1600
		self.row_padding = 0

		# viewport
		self.vp_x = 0
		self.vp_y = 0
		self.vp_width = 0
		self.vp_height = 0

		# clear colors
		self.clearRgbRed = 0
		self.clearRgbGreen = 0
		self.clearRgbBlue = 0

		# paint colors
		self.paintRgbRed = 0
		self.paintRgbGreen = 0
		self.paintRgbBlue = 0

	# Define rgbToByte(int, int, int). Converts RGB to bytes
	# returns: 4 bytes indicating the RGB of a pixel
	def rgbToByte(self, r,g,b):
		data = struct.pack('B', b)
		data += struct.pack('B', g)
		data += struct.pack('B', r)
		data += struct.pack('B', 0)

		return data

	# Define glCreateWindow(int, int). Creates the header for the BMP image (MUST BE USE AFTER INIT
	# TO CREATE THE IMAGE WITHOUT ANY PROBLEM
	# returns: 0 on success
	def glCreateWindow(self, new_width, new_height):

		self.width = new_width
		self.height = new_height
		self.row_bytes = new_width * 4
		self.row_padding = int(math.ceil(int(self.row_bytes / 4.0))) * 4 - self.row_bytes

		data =  bytes('BM', 'utf-8')
		data += struct.pack('i', 26 + 4 * self.width * self.height)
		data += struct.pack('h', 0)
		data += struct.pack('h', 0)
		data += struct.pack('i', 26)
		data += struct.pack('i', 12)
		data += struct.pack('h', self.width)
		data += struct.pack('h', self.height)
		data += struct.pack('h', 1)
		data += struct.pack('h', 32)

		self.image_data = data

		self.z_buffer = [
	      [-float('inf') for x in range(self.width)]
	      for y in range(self.height)
	    ]

		return 0

	# Define glViewPort(int, int, int, int). Establish an area of work for the painting process
	# returns: 0 on success
	def glViewPort(self, viewport_x, viewport_y, viewport_width, viewport_height):

		self.vp_x = viewport_x
		self.vp_y = viewport_y
		self.vp_width = viewport_width
		self.vp_height = viewport_height

		return 0

	# Define glClear(). It paints the whole image in a specific rgb color.
	# returns: 0 on success
	def glClear(self):

		first = True
		pixel = self.rgbToByte(self.clearRgbRed, self.clearRgbGreen, self.clearRgbBlue)

		for y in range(self.height):

			if (first):
				data = pixel * self.width
				first = False
			else:
				data += pixel * self.width

			# padding for each line
			for x in range(self.row_padding):
				data += bytes('\x00', 'utf-8')

		self.image_data += data

		return 0

	#Define glClearColor(float, float, float). It change the colors used for the glClear
	# returns: 0 on success
	def glClearColor(self,r,g,b):

		# the rgb data for glClear is store after converting the rgb numbers from float to integers
		# on a scale from 0 to 255
		self.clearRgbRed = int(math.ceil(float(r/1)*255))
		self.clearRgbGreen = int(math.ceil(float(g/1)*255))
		self.clearRgbBlue = int(math.ceil(float(b/1)*255))

		return 0

	# Define glVertex(int, int). Paints an individual pixel
	# returns: 0 on success
	def glVertex(self,x, y):

		# painting cordinates
		pcx = self.vp_x + x
		pcy = self.vp_y + y

		# changes the data of an individual pixel
		data = self.image_data[:26 + ((pcy - 1) * (self.width + self.row_padding) + (pcx - 1)) * 4]
		data += self.rgbToByte(self.paintRgbRed, self.paintRgbGreen, self.paintRgbBlue)
		data += self.image_data[30 + ((pcy - 1) * (self.width + self.row_padding) + (pcx - 1)) * 4:]

		self.image_data = data

		return 0

	# Define glColor(). Paint the whole viewport
	# returns: 0 on success
	def glVertexPaintVp(self):

		for y in range(self.vp_height):
			for x in range(self.vp_width):
				self.glVertex(x,y)

		return 0

	# Define glColor(float, float, float). It change the colors used for painting a specific pixel
	# returns: 0 on success
	def glColor(self,r,g,b):

		# the rgb data for the pixel painting is store after converting the rgb numbers from float
		# to integers on a scale from 0 to 255
		self.paintRgbRed = int(math.ceil(float(r/1)*255))
		self.paintRgbGreen = int(math.ceil(float(g/1)*255))
		self.paintRgbBlue = int(math.ceil(float(b/1)*255))

		return 0

	# Define glLine(). Paints a point anaywhere in the image.
	# returns: 0 on success
	def glPoint(self,x,y):
		x = round((x+1)*(self.width/2))
		y = round((y+1)*(self.height/2))

		self.glVertex(x,y)

		return 0

	# Define glLine(). Paints a line from point (xi,yi) to (xf,yf)
	# returns: 0 on success
	def glLine(self,xi,yi,xf,yf):

		xi = round((xi+1)*(self.width/2))
		xf = round((xf+1)*(self.width/2))
		yi = round((yi+1)*(self.height/2))
		yf = round((yf+1)*(self.height/2))

		dy = yf - yi
		dx = xf - xi

		if (dx == 0):
			for y in range(dy + 1):
				self.glVertex(xi,y + yi)

			return 0

		m = dy/dx
		grad = m <= 1 and m >= 0

		if grad and xi > xf:
			xi, xf = xf, xi
			yi, yf = yf, yi
			dy = yf - yi
			dx = xf - xi
			m = dy/dx
			grad = m <= 1 and m >= 0

		elif yi > yf:
			xi, xf = xf, xi
			yi, yf = yf, yi
			dy = yf - yi
			dx = xf - xi
			m = dy/dx
			grad = m <= 1 and m >= 0

		if (grad):
			for x in range(dx + 1):
				y = round(m*x + yi)
				self.glVertex(x+xi,y)
		else:
			m = 1/m
			for y in range(dy + 1):
				x = round(m*y + xi)
				self.glVertex(x,y + yi)

		return 0

	# Define glPolyFiller(). Paints a figure given the vertices in a list.
	# returns: 0 on success
	def glPolyFiller(self, vertices, z_coordinate):

		# lista para guardar los puntos de la figura
		figurePoints = []

		# se reutiliza el codigo para hacer lineas solo que se guarda cada punto
		# que se pinta en figurePoints
		for i in range(len(vertices)):

			xi = vertices[i][0]
			yi = vertices[i][1]

			if i == len(vertices)-1:
				xf = vertices[0][0]
				yf = vertices[0][1]

			else:
				xf = vertices[i+1][0]
				yf = vertices[i+1][1]

			dy = yf - yi
			dx = xf - xi

			if (dx == 0):
				for y in range(dy + 1):
					figurePoints.append([xi,y + yi])
					if z_coordinate >= self.z_buffer[xi][y+yi]:
						self.glVertex(xi,y + yi)
						self.z_buffer[xi][y+yi] = z_coordinate
			else:
				m = dy/dx
				grad = m <= 1 and m >= 0

				if grad and xi > xf:
					xi, xf = xf, xi
					yi, yf = yf, yi
					dy = yf - yi
					dx = xf - xi
					m = dy/dx
					grad = m <= 1 and m >= 0

				elif yi > yf:
					xi, xf = xf, xi
					yi, yf = yf, yi
					dy = yf - yi
					dx = xf - xi
					m = dy/dx
					grad = m <= 1 and m >= 0

				if (grad):
					for x in range(dx + 1):
						y = round(m*x + yi)
						figurePoints.append([x+xi,y])
						if z_coordinate >= self.z_buffer[x+xi][y]:
							self.glVertex(x+xi,y)
							self.z_buffer[x+xi][y] = z_coordinate
				else:
					m = 1/m
					for y in range(dy + 1):
						x = round(m*y + xi)
						figurePoints.append([x,y + yi])
						if z_coordinate >= self.z_buffer[x][y+yi]:
							self.glVertex(x,y + yi)
							self.z_buffer[x][y+yi] = z_coordinate


		# avoids processing the same point twice.
		avoidPoints = []

		for point in figurePoints:

			if point[1] not in avoidPoints:

				# finds which points are in the same y coordinate in the figure.
				pointsToPaint = []
				for i in range(len(figurePoints)):
					if figurePoints[i][1] == point[1] and figurePoints[i][1] != figurePoints[i-1][1]:
						pointsToPaint.append(figurePoints[i][0])

				# order the points
				pointsToPaint.sort()
				pointsLen = len(pointsToPaint)

				if pointsLen%2 == 0:
					for i in range(0,pointsLen,2):
						for xToDraw in range(pointsToPaint[i],pointsToPaint[i+1]):
							if z_coordinate >= self.z_buffer[xToDraw][point[1]]:
								self.glVertex(xToDraw,point[1])
								self.z_buffer[xToDraw][point[1]] = z_coordinate
				else:
					for xToDraw in range(pointsToPaint[0],pointsToPaint[len(pointsToPaint)-1]):
						if z_coordinate >= self.z_buffer[xToDraw][point[1]]:
							self.glVertex(xToDraw,point[1])
							self.z_buffer[xToDraw][point[1]] = z_coordinate

				avoidPoints.append(point[1])

		return 0

	# Define glObjReader(). Makes BMP out of a flat .obj
	# Return 0 on success
	def glObjReader(self,objectName,scale,translate_x, translate_y):

		# Opens obj file
		file = open(objectName + '.obj')
		lines = file.read().splitlines()

		# Vertices and faces
		vertices = []
		faces = []

		# read lines
		for line in lines:

			try:
				prefix, value = line.split(' ',1)
			except ValueError:
				continue

			# read vertices
			if prefix == 'v':
				vertices.append(list(map(float, value.split(' '))))

			# read faces
			elif prefix == 'f':
				section = []
				for face in value.split(' '):
					try:
						section.append(list(map(int, face.split('/'))))
					except ValueError:
						try:
							section.append(list(map(int, face.split('//'))))
						except ValueError:
							break
				faces.append(section)

		counter = 0
		print("This object has: " + str(len(faces)) + " faces")
		for face in faces:

			# prints porcentage of the process done
			counter += 1
			if counter%50 == 0:
				sys.stdout.write('\r'+(str(float(counter*100/len(faces)))[0:4] + "% Complete"))

			pollygon = []
			z_coordinate = 0
			x_avg = 0
			y_avg = 0

			# gets all the vertices in a face
			for i in range(len(face)):
				x = int((vertices[face[i][0]-1][0]/scale + translate_x)*self.width)
				y = int((vertices[face[i][0]-1][1]/scale + translate_y)*self.height)
				z = int(vertices[face[i][0]-1][2])

				x_avg += x
				y_avg += y
				z_coordinate += z

				pollygon.append([x,y])

			# avarage of each cooordinate
			x_avg = x_avg/len(face)
			y_avg = y_avg/len(face)
			z_coordinate = z_coordinate/len(face)

			# gets the grey scale to use for the painting
			grey = (abs(x_avg-self.width/2)/(self.width/-2) + abs(y_avg-self.height/2)/(self.height/-2) + 2)/2
			self.glColor(grey, grey, grey)

			# paints the face
			self.glPolyFiller(pollygon,z_coordinate)

		sys.stdout.write('\r'+"100% Complete ")

		return 0

	# Define glFinish(). Takes the image_data and makes a file out of it
	# returns: 0 on success
	def glFinish(self):

		# Makes the image file
		img = open('out.bmp', 'wb')
		img.write(self.image_data)

		return 0

	# Define glFinishWN(). Takes the image_data and makes a file out of it with
	# a specif name
	# returns: 0 on success
	def glFinishWN(self, fileName):

		# Makes the image file
		img = open(fileName, 'wb')
		img.write(self.image_data)

		return 0
