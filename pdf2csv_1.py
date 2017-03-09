#!/usr/bin/python

import sys
from PIL import Image as PI
from PyPDF2 import PdfFileWriter, PdfFileReader
import PythonMagick										#	 Convert PDf to image
import glob
import pyocr
import pyocr.builders
import io

sourcePdf = sys.argv[1]
pdfname = sourcePdf[:4]

infile = PdfFileReader(open(sourcePdf,'rb'))
totalPages = infile.getNumPages()

# Convert Multi-page pdf to single pages of pdf
print "Converting Multi-page pdf to single pages of pdf"
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
print "Converting each pdf into images"
for i in range(totalPages):
	img = PythonMagick.Image()
	img.density("500")
	img.read(pdfList[i])
	outimg= pdfList[i].split(".")[0]+".jpeg"
	img.write(outimg)

# req_img[]  Hold our images list
# final_text[]  hold our final text
req_image= []
final_text = []

for name in glob.glob('*.jpeg'):
	req_image.append(name)

#print "req_name = ",req_img

# Get the Tool from OCR Library and Language that are used by PyOCR
tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[2]					#[2]  : English Language

#getting text from Image
print "Getting text from Image"
for img in req_image:
	with open(img, 'rb') as fp:
		txt = tool.image_to_string(
			PI.open(fp,'r'),
			lang=lang,
			builder=pyocr.builders.TextBuilder()
		)
	final_text.append(txt)

#print final_text

data = final_text[0].splitlines(0)							# Data item without newlinw characters

# Each element in final_list start with unicode character 'u'
# removing unicode 'u' from eack element of final_text list
new_data = [item.encode('utf8') for item in data]			# Data without unicode; removing u from prifix
print data
