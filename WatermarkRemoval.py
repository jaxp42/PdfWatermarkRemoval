import os
from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.generic import TextStringObject, NameObject
from PyPDF4.utils import b_

# print("Buscando archivos en " + os.path.realpath(sys.argv[0]))

entries = os.scandir('./')
textsToRemove = ['watermark']
outputFile = r"output.pdf"

for entry in entries:
    name = entry.name
    if name.endswith('.pdf'):
        print(name)
        source = PdfFileReader(name, "rb")
        output = PdfFileWriter()

        for pageNumber in range(source.getNumPages()):
            page = source.getPage(pageNumber)
            pageText = page.extractText()
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, source)

            for operands, operator in content.operations:
                if operator == b_("Tj"):
                    text = operands[0]

                    if isinstance(text, str):
                        for textToRemove in textsToRemove:
                            if textToRemove in text:
                                print('Eliminando contenido de la página ' + str(pageNumber))
                                print(operands[0])
                                operands[0] = TextStringObject('')

            page.__setitem__(NameObject('/Contents'), content)
            output.addPage(page)

            with open(outputFile, "wb") as outputStream:
                output.write(outputStream)
