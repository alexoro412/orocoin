def calcArea(p1,p2,p3):
	#p1,p2,p3 = [x,y,z] of each point
	m11 = 1
	m12 = 1
	m13 = 1

	m21 = p2[0]-p1[0]
	m22 = p2[1]-p1[1]
	m23 = p2[2]-p1[2]
	m31 = p3[0]-p1[0]
	m32 = p3[1]-p1[1]
	m33 = p3[2]-p1[2]

	a = m31*m22*m13
	b = m32*m23*m11
	c = m33*m21*m12
	d = m11*m22*m33
	e = m12*m23*m31
	f = m13*m21*m32

	return abs(0.5*(a+b+c-d-e-f))

def parseSTL(filename):
	f = open(filename)
	content = f.readlines() #3-5
	vertexes = []
	for i in range(0,len(content)):
		line = content[i].split()
		if line[0] == 'vertex':
			vertexes.append(content[i])
	# print vertexes
	# print len(vertexes)
	sum = 0
	for i in range(0,len(vertexes),3):
		line = vertexes[i].split()
		l1 = parseLine(vertexes[i].split())
		l2 = parseLine(vertexes[i+1].split())
		l3 = parseLine(vertexes[i+2].split())
		sum += calcArea(l1,l2,l3)
	# print 'sum: '
	return sum
	#print vertexes
	# print parseLine(content[3].split())

	# print calcArea(l1,l2,l3)
	f.close()

def parseLine(line):
	if line[0] == 'vertex':
		return [float(line[1]),float(line[2]),float(line[3])]

#print " 1    | {}  {}  {}  |".format(m11,m12,m13)
#print "--- * | {} {} {}|".format(m21,m22,m23)
#print " 2    | {} {} {}  |".format(m31,m32,m33)

print parseSTL("/Users/alexoro/static/box.stl")
