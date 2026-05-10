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
import getpass

strUserID = getpass.getuser()
#  Note:  (change from my file structure)
os.chdir("C:\\DataSci\\PythonWorkArea\\IBMDocling\\IBMDoclingVenv")

artifacts_path = "models"
pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path)

converterPDF = DocumentConverter (
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
})

source="2408.09869v5.pdf"
#  doc = doc_converter.convert(source)
doc = converterPDF.convert(source=source).document

strExtract = ""
strExtract = doc.export_to_markdown()
print (strExtract)

#
#  ---------- Option 3 - Docling Local Chunks ----------
#

#  Disconnected from the internet.  
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import RapidOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

import sentencepiece
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer

import getpass
import os

strUserID = getpass.getuser()
#  Note:  (change from my file structure)
os.chdir("C:\\DataSci\\PythonWorkArea\\IBMDocling\\IBMDoclingVenv")

artifacts_path = "models"
pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path)

converterPDF = DocumentConverter (
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
})

#  Setup local chunker -  First Time Run 
#  -  Will download the model 
#  - Then can comment out and use local path for subsequent runs.
#  - Better - copy folder "models--sentence-transformers--all-MiniLM-L6-v2"
#  - From ~/.cache/huggingface/hub/ to the models folder in the venv.  
'''
tokenizer = HuggingFaceTokenizer(tokenizer=AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2"), max_tokens=512)
'''
local_minilm_l6_v2 = "C:\\DataSci\\PythonWorkArea\\IBMDocling\\IBMDoclingVenv\\models\\models--sentence-transformers--all-MiniLM-L6-v2\\snapshots\\c9745ed1d9f207416be6d2e6f8de32d1f16199bf"
tokenizer = HuggingFaceTokenizer(tokenizer=AutoTokenizer.from_pretrained(local_minilm_l6_v2),max_tokens=1024)
chunker = HybridChunker(tokenizer=tokenizer, max_tokens=1024)

source="2408.09869v5.pdf"

#  Downloads to C:\Users\<userID>\.cache\huggingface\hub\models--sentence-transformers--all-MiniLM-L6-v2
#  All other docs (docx, xlsx, pptx) will load at once - Use chunking.
#  Convert it ready for chunking.
doc = converterPDF.convert(source=source).document
chunk_iter = chunker.chunk(doc)

chunks = list(chunk_iter)

'''
len(chunks)  # output: 30
i = 0
list(chunks[i])[0][1]  # output: "### Docling Technical Report[...]"
#  Gets the output text of the first chunk
'''

#  Print the chunks out
for i in range(0, len(chunks)):
    print(f"Chunk {i} - Tokens: {len(list(chunks[i])[0][1].split())}")
    print("\n"+list(chunks[i])[0][1])

#  print(chunks[0].export_to_markdown())  # output: "### Docling Technical Report[...]"

#
#  ---------- Document Packages ----------
#
venv\Scripts\python.exe -m pip freeze > requirements.txt

#  Then can compare on a new machine - 
#  to install using requirements.txt
#  venv\Scripts\python.exe -m pip install  -r requirements.txt
#  Then can compare on a new machine - 
#  to install using requirements.txt
#  venv\Scripts\python.exe -m pip install  -r requirements.txt
