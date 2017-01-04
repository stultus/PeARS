from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from cStringIO import StringIO
from StringIO import StringIO
import urllib2
from urllib2 import Request
import requests
import sys

#Thanks to https://quantcorner.wordpress.com/2014/03/16/parsing-pdf-files-with-python-and-pdfminer/

def convert_pdf_to_txt(url):
  open = urllib2.urlopen(Request(url)).read()

  # Cast to StringIO object
  memory_file = StringIO(open)

  # Create a PDF parser object associated with the StringIO object
  parser = PDFParser(memory_file)

  # Create a PDF document object that stores the document structure
  document = PDFDocument(parser)

  rsrcmgr = PDFResourceManager()
  retstr = StringIO()
  codec = 'utf-8'
  laparams = LAParams()

  device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

  interpreter = PDFPageInterpreter(rsrcmgr, device)

  for page in PDFPage.create_pages(document):
    interpreter.process_page(page)

  text = retstr.getvalue()

  device.close()
  retstr.close()
  return text

print convert_pdf_to_txt(sys.argv[1])
