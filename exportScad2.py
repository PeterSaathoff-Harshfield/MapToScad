from scipy import misc
import time
import datetime

# name = "02.png"
# name = "sf-small.png"
name = "sf-large.png"

image = misc.imread(name)
# print(image)

width = len(image[0])
height = len(image)
pixelCount = width * height

print("width: " + str(width))
print("height: " + str(height))
print("pixels: " + str(pixelCount))

darkPixels = 0
otherPixels = 0

# highest = 0

# outputArray = []
intermediateArray = []
outputArray = []

def readImage():
	
	for row in range(0, height):
		col = []
		for column in range(0, width):

			# print("x " + str(row) + " y " + str(column))
			pixel = image[row][column]
			z = int(pixel[0]) + int(pixel[1]) + int(pixel[2])
			
			if (z < 130):
				# outputArray[row][column] = 0
				col.append(0)
			else:
				z = (z - 100) / 30.0
				# if (z < 5):
					# z = 0
				# outputArray[row][column] = z
				col.append(z)
			
			# if (z < 0):
				# print("whoa, less than 0")
			# if (z > highest):
				# highest = z
			# if (z == 51):
				# continue
			# if (z < 200):
				# continue
			# if (z >= 35):
				# z -= 35
			# z = int(z / 12)
			# if (z < 5):
				# continue
			
				
			
			# outputArray.append([row, column, z])
	
		intermediateArray.append(col)


def serializeArray():
	secondaryArray = intermediateArray
	for rowIndex, row in enumerate(intermediateArray):
		for colIndex, pixel in enumerate(row):
			if (pixel != 0):
				score = 0
				# print("row: " + str(rowIndex))
				if (rowIndex > 0):
					if (intermediateArray[rowIndex - 1][colIndex] == 0):
						score += 1
				if (rowIndex < height - 1):
					if (intermediateArray[rowIndex + 1][colIndex] == 0):
						score += 1
				if (colIndex > 0):
					if (intermediateArray[rowIndex][colIndex - 1] == 0):
						score += 1
				if (colIndex < width - 1):
					if (intermediateArray[rowIndex][colIndex + 1] == 0):
						score += 1
				
				if (score > 2):
					# outputArray.append([rowIndex, colIndex, pixel])
					secondaryArray[rowIndex][colIndex] = 0
	
	
	tertiaryArray = secondaryArray
	for rowIndex, row in enumerate(secondaryArray):
		for colIndex, pixel in enumerate(row):
			if (pixel != 0):
				score = 0
				# print("row: " + str(rowIndex))
				if (rowIndex > 0):
					if (secondaryArray[rowIndex - 1][colIndex] == 0):
						score += 1
				if (rowIndex < height - 1):
					if (secondaryArray[rowIndex + 1][colIndex] == 0):
						score += 1
				if (colIndex > 0):
					if (secondaryArray[rowIndex][colIndex - 1] == 0):
						score += 1
				if (colIndex < width - 1):
					if (secondaryArray[rowIndex][colIndex + 1] == 0):
						score += 1
				
				if (score > 3):
					# outputArray.append([rowIndex, colIndex, pixel])
					tertiaryArray[rowIndex][colIndex] = 0
	
	
	for rowIndex, row in enumerate(secondaryArray):
		for colIndex, pixel in enumerate(row):
			if (pixel != 0):
				score = 0
				# print("row: " + str(rowIndex))
				if (rowIndex > 0):
					if (tertiaryArray[rowIndex - 1][colIndex] == 0):
						score += 1
				if (rowIndex < height - 1):
					if (tertiaryArray[rowIndex + 1][colIndex] == 0):
						score += 1
				if (colIndex > 0):
					if (tertiaryArray[rowIndex][colIndex - 1] == 0):
						score += 1
				if (colIndex < width - 1):
					if (tertiaryArray[rowIndex][colIndex + 1] == 0):
						score += 1
				
				if (score < 3):
					outputArray.append([rowIndex, colIndex, pixel])
					
			
def constructScad(data):
	c = 0
	output = ""
	output += "union() {\n"
	output += "translate([0, 0, -5]) {cube([" + str(height) + ", " + str(width) + ", 5]);}\n"
	output += "union() {\n"
	
	for point in data:
		row = point[0]
		column = point[1]
		z = point[2]
		
		s = "translate([" +\
			str(row) + ", " +\
			str(column) + ", " +\
			"0]) {" +\
			"cube([" +\
			"1, 1, " +\
			str(z) + "]);}\n"
		
		output += s
		if (c == 100):
			output += "}\n"
			output += "union() {\n"
			c = 0
		c += 1
	
	output += "}\n"
	output += "}"
	
	return output




readImage()
# print(intermediateArray)
serializeArray()
outputScadText = constructScad(outputArray)



ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
filename = st + ".scad"
with open(filename, 'a') as out:
	out.write(outputScadText + '\n')

print("output length: " + str(len(outputArray)))

# print("highest: " + str(highest))

# print("dark pixels: " + str(darkPixels))
# print("other pixels: " + str(otherPixels))
# print(pixelCount - darkPixels - otherPixels)