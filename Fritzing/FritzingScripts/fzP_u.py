import xml.etree.ElementTree as ET
import zipfile
import os.path
import os
import sys
import re

# RexRule = r"(?p<y>d{2,3})(?p<x>d{3})"
# XYRex = re.compile(RexRule)

listXY = []
# listY = []
def displayUsage():
   print "Usage: python fzP.py [input fzz file path]"

def main():
   if(len(sys.argv)!= 2):
      displayUsage()

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
         if 'uCirKit-boardModuleID' in IdRef:
            IndexRef = eachElement.get("modelIndex")
            print 'Breadboard: '+ IdRef + ' <'+IndexRef+'>'

         # titleText = eachElement.find('./title')
         # print titleText
         HasTitle = eachElement.find('title')
         
         if 'WireModuleID' in IdRef and HasTitle is not None:
            # print 'Wire: '+ IdRef
            bothAreBreadboard = 0
            listtmp = []
            # listYtmp = []
            for eachWire in eachElement.find("views/breadboardView/connectors"):
               # print eachWire
               
               for eachConnects in eachWire.find("connects"):
                  IndexConnect = eachConnects.get("modelIndex")
                  # print IndexConnect
                  if IndexConnect == IndexRef:
                     # print IndexConnect
                     bothAreBreadboard = bothAreBreadboard+1
                     IdConnect = eachConnects.get("connectorId")
                     # print IdConnect
                     XYvalue = re.match(r"([A-Z])(\d{1,2})", IdConnect)
                     if XYvalue:
                        # print XYvalue.group()
                        listtmp.append([XYvalue.group(1),XYvalue.group(2)])
                        # print listtmp
            # print bothAreBreadboard
            if bothAreBreadboard == 2:
               listXY.append(listtmp)
               # listY.append(listYtmp)
               # print '*'

   print len(listXY),'wire(s).'
   outputPairText.write(str(len(listXY))+"\n")

   for i in xrange(0, len(listXY)):
      # print i
      pairString = 'WirePair<'+str(listXY[i])+'>'
      outputPairText.write(str(listXY[i])+"\n")
      print pairString

if __name__ == '__main__':
   main()
