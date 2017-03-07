#!/usr/bin/python

import PythonMagick		# Convert PDf to image
import sys
import glob
from PyPDF2 import PdfFileWriter, PdfFileReader

sourcePdf = sys.argv[1]
pdfname = sourcePdf[:4]

infile = PdfFileReader(open(sourcePdf,'rb'))
totalPages = infile.getNumPages()

# Convert Multi-page pdf to single pages of pdf
for i in range(totalPages):
	page = infile.getPage(i)
	outfile = PdfFileWriter()
	outfile.addPage(page)
	with open(pdfname+"-%02d.pdf"%i,'wb') as f:
		outfile.write(f)

# List of all pdf pages
pdfList = []
for i in range(totalPages):
	pdfList.append(pdfname+"-0"+str(i)+".pdf")

#print "PDF List: ",pdfList

# Convert each pdf into images
for i in range(totalPages):
	img = PythonMagick.Image()
	img.density("500")
	img.read(pdfList[i])
	outimg= pdfList[i].split(".")[0]+".PNG"
	img.write(outimg)

# req_img[]  Hold our images list
# final_text[]  hold our final text
req_img= []
final_text = []

for name in glob.glob('*.PNG'):
	req_img.append(name)

#print "req_name = ",req_img
