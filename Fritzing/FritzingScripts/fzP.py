import xml.etree.ElementTree as ET
import zipfile
import os.path
import os
import sys
import re

# RexRule = r"(?p<y>d{2,3})(?p<x>d{3})"
# XYRex = re.compile(RexRule)

listX = []
listY = []


if(len(sys.argv)!= 2):
   print 'No input fzz file. Usage: python fzP.py [input fzz file path]'

elif(len(sys.argv)== 2):
   # print 'Argument List:', str(sys.argv[1])
   zfile = zipfile.ZipFile(str(sys.argv[1]))
   for name in zfile.namelist():
     (dirname, filename) = os.path.split(name)
     # print "Decompressing " + filename + " on " + dirname
     dirname = str(sys.argv[1]).rsplit('/',1)[0]+"/"+dirname
     zfile.extract(name, dirname)

   # print str(sys.argv[1]).rsplit('.',1)[0]
   outputPairText = open(str(sys.argv[1]).rsplit('.',1)[0]+".txt",'w')

   fzTree = ET.parse(dirname+"/"+name)
   fzTreeRoot = fzTree.getroot()

   # thisBreadBoard = fzTreeRoot.module.instances.instance
   # for child in thisBreadBoard:
   #    print child
   for eachElement in fzTreeRoot.findall("./instances/instance"):
      IdRef = eachElement.get("moduleIdRef")
      # if 'PerfboardModuleID' in IdRef:
      #    print 'Breadboard: '+ IdRef
      #    for eachConnector in eachElement.findall("./views/breadboardView/connectors/connector"):
      #       # print eachConnector
      #       IdConnector = eachConnector.get("connectorId")
      #       print 'Connector: '+ IdConnector

      # titleText = eachElement.find('./title')
      # print titleText
      HasTitle = eachElement.find('title')
      
      if 'WireModuleID' in IdRef and HasTitle is not None:
         # print 'Wire: '+ IdRef
         for eachWire in eachElement.find("views/breadboardView/connectors"):
            # print eachWire
            for eachConnects in eachWire.find("connects"):
               IdConnect = eachConnects.get("connectorId")
               # print IdConnect
               XYvalue = re.match(r"connector(\d{1,3})(\d{3})", IdConnect)
               if XYvalue:
                  # print XYvalue.group()
                  listX.append(int(XYvalue.group(2)))
                  listY.append(int(XYvalue.group(1)))

print len(listX)/2,'wire(s).'
outputPairText.write(str(len(listX)/2)+"\n")

for i in xrange(0, len(listX), 2):
   # print i
   pairString = 'WirePair<['+str(listX[i])+','+str(listY[i])+'],['+str(listX[i+1])+','+str(listY[i+1])+']>'
   outputPairText.write(str(listX[i])+","+str(listY[i])+","+str(listX[i+1])+","+str(listY[i+1])+"\n")
   print pairString
