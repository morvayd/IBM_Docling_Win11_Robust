#  Reference:  https://docling-project.github.io/docling/

#  Note:  (change from my file structure)
#  cd "C:\\DataSci\\PythonWorkArea\\IBMDocling\\IBMDoclingVenv"

#  "venv\Scripts\activate.bat"

#  venv\Scripts\python.exe

#
#  ---------- Option 1 - Internet Required ----------
#
#  Verify the installation is working while still connected to the internet.
from docling.document_converter import DocumentConverter

source = "https://arxiv.org/pdf/2408.09869"  # file path or URL - can download
converter = DocumentConverter()
doc = converter.convert(source).document

print(doc.export_to_markdown())  # output: "### Docling Technical Report[...]"

#
#  ---------- Option 2 - Docling Local ----------
#
#  Disconnected from the internet.  
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import RapidOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
import os

strUserID = os.getlogin()

#  Note:  (change from my file structure)
artifacts_path = "C:\\DataSci\\PythonWorkArea\\IBMDocling\\IBMDoclingVenv\\models"
pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path)

doc_converter = DocumentConverter (
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
})

#  Note:  /home/ UserID is needed. (change from my file structure)
source="C:\\DataSci\\PythonWorkArea\\IBMDocling\\IBMDoclingVenv\\2408.09869v5.pdf"
result = doc_converter.convert(source)

strExtract = ""
strExtract = result.document.export_to_markdown()
print (strExtract)

#
#  ---------- Document Packages ----------
#
venv\Scripts\python.exe -m pip freeze > requirements.txt

#  Then can compare on a new machine - 
#  to install using requirements.txt
#  venv\Scripts\python.exe -m pip install  -r requirements.txt