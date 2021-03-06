#!/usr/bin/env python
# encoding: utf-8
"""
/*******************************************************************

Part of the Fritzing project - http://fritzing.org
Copyright (c) 2007-08 Fachhochschule Potsdam - http://fh-potsdam.de

Fritzing is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Fritzing is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Fritzing.  If not, see <http://www.gnu.org/licenses/>.

generator.py

This script generates a svg or fzp file for breadboards to be used in Fritzing.
Edit it directly, then run it in the commmand line.

Run it in the commandline with this:
 python generator.py run [svg|fzp] > partdescription.xml
"""

import sys, os, uuid, zipfile
from datetime import date
from Cheetah.Template import Template


sL = {}
boardLayout = []
rowNets = []
lineNets = []
rowProps = {}
lineProps = {}

def setup():
	# Edit these variables below to generate different breadboards
	#
	# sL = searchList, a dict to use with the template 
	sL['title'] = "uCirKit-board"
	sL['moduleID'] = "uCirKit-boardModuleID"
	sL['svgFile'] = "uCirkit-board.svg"

	sL['label'] = "Bread"
	sL['taxonomy'] = "prototyping.breadboard.breadboard.uCirkit"
	
	# Most breadboards have rows and lines.
	# Rows are 5 holes verticaly
	# Lines are power/ground lines running horizontaly
	
	# Rows 
	rowHeight = 5 # You probably never need to change this, but who knows
	rowsInterBlockSpacing = 2
	rowProps['startsAtX'] = 1
	rowProps['startsAtYWithLetter'] = 'A'
	rowProps['segmentLength'] = 30
	rowProps['interSegmentSpacing'] = 2
	rowProps['numberOfSegments'] = 1	
		
	# Lines
	numberOfLinesPerSet = 2
	interRowsLinesSpacing = 4
	lineProps['startAtX'] = 2
	lineProps['subSegmentLength'] = 5
	lineProps['interSubSegmentSpacing'] = 1
	lineProps['segmentLength'] = 5 # measures in subSegments
	lineProps['interSegmentSpacing'] = 10
	lineProps['numberOfSegments'] = 1
	lineProps['endsAtYWithLetter'] = 'Z'
	
	# Layout
	# boardLayout.append( ("lines", numberOfLinesPerSet) )
	boardLayout.append( ("spacing", interRowsLinesSpacing) )
	boardLayout.append( ("rows", rowHeight) )
	boardLayout.append( ("spacing", rowsInterBlockSpacing) )
	boardLayout.append( ("rows", rowHeight) )
	boardLayout.append( ("spacing", interRowsLinesSpacing) )
	# boardLayout.append( ("lines", numberOfLinesPerSet) )
	
	return

def displayUsage():
	print """Fritzing Breadboard generator
Usage:
	python generator.py run [fzp & svg name]
"""

def makeUUID():
    "creates an 8 character hex UUID"
    return str(uuid.uuid1())
    
def makeDate():
    "creates a date formatted as YYYY-MM-DD"
    return date.today().isoformat()

def getUserName():
	"gets the full user name if available"
	try:
		import pwd
		return pwd.getpwuid(os.getuid())[4]
	except:
		return os.getlogin()

def calculateTotal(typeToCount, boardLayout):
	count = 0
	for item in boardLayout:
		if item[0] == typeToCount:
			count += item[1]
	return count



def getTemplatefile(fileName):
	thisScriptPath = sys.argv[0]
	thisScriptFolder = os.path.split(thisScriptPath)[0]
	expectedTemplate = os.path.join(thisScriptFolder, fileName)
	if os.path.exists(expectedTemplate):
		return expectedTemplate
	else:
		print "Script Package Incomplete: Couldn't find the svg template file."
		sys.exit()

def main():
	if len(sys.argv) >= 2 and sys.argv[1] == 'run':
		file_svg = open('svg.breadboard.'+sys.argv[2]+'.svg', 'w')
		file_icon = open('svg.icon.'+sys.argv[2]+'icon.svg', 'w')
		file_fzp = open('part.'+sys.argv[2]+'.fzp', 'w')
		f_zipFile = zipfile.ZipFile(sys.argv[2]+'.fzpz', 'w',zipfile.ZIP_DEFLATED)  
		setup()
		# Check if we can identify all y positions with a single letter
		numberOfRowCols = calculateTotal('rows', boardLayout)
		numberOfLines = calculateTotal('lines', boardLayout)
		
		if (numberOfRowCols + numberOfLines) > 26:
			print "TO MUCH LINES OR ROWS. The script does not know how to name them right. Aborting generation of part"
			sys.exit()
	
		# Make Nets
		maxSizeX = 0
		incrementalY = 0
		incrLetterY = rowProps['startsAtYWithLetter']
		incrLineYLetterOrd = ord(lineProps['endsAtYWithLetter']) - (numberOfLines - 1)
		for item in boardLayout:
			if item[0] == 'rows':
				incrementalX = 0
				for segment in range(rowProps['numberOfSegments']):
					for positionX in range(rowProps['segmentLength']):
						row = {}
						net = []
						row['id'] = "bus%d-%d" % (positionX + incrementalX, incrementalY)
						for posY in range(item[1]):
							dot = {}
							dot['x'] = positionX + incrementalX
							dot['y'] = incrementalY + posY
							charY = chr(ord(incrLetterY) + posY)
							posXid = positionX + rowProps['startsAtX'] + incrementalX
							if posXid < 1: posXid += 99
							dot['id'] = charY + str(posXid)
							net.append(dot)
						row['net'] = net
						rowNets.append(row)
					incrementalX += positionX + rowProps['interSegmentSpacing']
					if (incrementalX - rowProps['interSegmentSpacing'] + 1) > maxSizeX:
						maxSizeX = incrementalX - rowProps['interSegmentSpacing'] + 1
				incrLetterY = chr(ord(incrLetterY) + item[1])
			elif item[0] == 'lines':
				for line in range(item[1]):
					incrementalX = 0
					for segment in range(lineProps['numberOfSegments']):
						thisLine = {}
						net = []
						thisLine['id'] = "bus%s-%d" % (chr(incrLineYLetterOrd + line), lineProps['startAtX'] + incrementalX)
						subIncrX = 0
						for subSegment in range(lineProps['segmentLength']):
							for posX in range(lineProps['subSegmentLength']):
								dot = {}
								dot['x'] = lineProps['startAtX'] + posX + subIncrX + incrementalX
								dot['y'] = incrementalY + line
								charY = chr(incrLineYLetterOrd + line)
								posXid = dot['x'] + rowProps['startsAtX']
								if posXid < 1: posXid += 99
								dot['id'] = charY + str(posXid)
								net.append(dot)
							subIncrX += lineProps['subSegmentLength'] + lineProps['interSubSegmentSpacing']
						thisLine['net'] = net
						lineNets.append(thisLine)
						incrementalX += subIncrX + lineProps['interSegmentSpacing'] - 1
						if (incrementalX - lineProps['interSegmentSpacing'] + lineProps['startAtX']) > maxSizeX:
							maxSizeX = incrementalX - lineProps['interSegmentSpacing'] + lineProps['startAtX']
				incrLineYLetterOrd += line + 1
			incrementalY += item[1]
		
		# Add these nets to the searchList
		sL['rows'] = rowNets
		sL['lines'] = lineNets
		# Add the size to the searchList
		totalX = (18.3 + 9 * maxSizeX)
		totalY = (9 + 9 * incrementalY)
		sizeDict = {}
		sizeDict['pxWidth'] = "%.3f" % (totalX)
		sizeDict['pxHeight'] = "%.3f" % (totalY)
		sizeDict['realWidth'] = "%.4fin" % (totalX / 90.0)
		sizeDict['realHeight'] = "%.4fin" % (totalY / 90.0)
		sL['size'] = sizeDict
		
		#OUTPUT
		metaData = {}
		metaData['moduleID'] = makeUUID()
		# TODO for the real generator use the UUID
		metaData['moduleID'] = sL['moduleID']
		metaData['date'] = makeDate()
		metaData['author'] = getUserName()
		sL['metaData'] = metaData
		# -------------------fzp
		fzp = Template(file=getTemplatefile("breadboard_fzp.tmpl"), searchList = [sL])
		file_fzp.write(str(fzp))
		# print fzp

		# -------------------svg
		svg = Template(file=getTemplatefile("breadboard_svg.tmpl"), searchList = [sL])
		file_svg.write(str(svg))
		file_icon.write(str(svg))
		# print svg
		# print file_svg.name
		# f_zipFile.write(file_svg.name)
		# f_zipFile.write(file_icon.name)
		# f_zipFile.write(file_fzp.name)
		# print f_zipFile.namelist()
		file_svg.close()
		file_fzp.close()
		f_zipFile.close()
	else:
		displayUsage()


if __name__ == '__main__':
	main()
