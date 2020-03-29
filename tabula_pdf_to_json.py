import os
import tabula

PDFs = './PDFs/'
JSONs = './JSONs/'

for filename in os.listdir(PDFs):
    pdf_filename = os.path.join(PDFs, filename)
    json_filename = os.path.join(JSONs, filename).replace('.pdf', '.json')
    tabula.convert_into(pdf_filename, json_filename,
                        output_format="json", pages="all")

