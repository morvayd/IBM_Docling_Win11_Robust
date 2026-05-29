#  Reference:  https://docling-project.github.io/docling/

#  Note:  (change from my file structure)
#  cd ~/PythonVenv/IBMDocling

#  source venv/bin/activate

#  venv/bin/python3

#
#  ---------- Option 1 - Internet Required ----------
#
#  Verify the installation is working while still connected to the internet
from docling.document_converter import DocumentConverter

from typing import Any

source = "https://arxiv.org/pdf/2408.09869"  # file path or URL - can download
converter: Any= DocumentConverter()
doc: Any= converter.convert(source).document

print(doc.export_to_markdown())  # output: "### Docling Technical Report[...]"

#
#  ---------- Option 2 - Docling Local ----------
#
#  Disconnected from the internet.  
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import RapidOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

from typing import Any
import getpass
import os

strUserID: str = getpass.getuser()
#  Note:  (change from my file structure)
strPath: str = "/Users/"+strUserID+"/PythonVenv/IBMDocling"
os.chdir(path=strPath)

artifacts_path = "models"
pipeline_options: Any = PdfPipelineOptions(artifacts_path=artifacts_path)

doc_converter: Any = DocumentConverter (
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
})

source="2408.09869v5.pdf"
result: Any = doc_converter.convert(source)

strExtract: Any = ""
strExtract: Any = result.document.export_to_markdown()
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

from typing import Any
import getpass
import os

strUserID: str = getpass.getuser()
#  Note:  (change from my file structure)
strPath: str = "/Users/"+strUserID+"/PythonVenv/IBMDocling"
os.chdir(path=strPath)

artifacts_path = "models"
pipeline_options: Any = PdfPipelineOptions(artifacts_path=artifacts_path)

converterPDF: Any = DocumentConverter (
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

local_minilm_l6_v2: str = strPath+"/models/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/c9745ed1d9f207416be6d2e6f8de32d1f16199bf"
tokenizer: Any = HuggingFaceTokenizer(tokenizer=AutoTokenizer.from_pretrained(local_minilm_l6_v2),max_tokens=1024)
chunker: Any = HybridChunker(tokenizer=tokenizer, max_tokens=1024)

source="2408.09869v5.pdf"

#  Downloads to C:\Users\<userID>\.cache\huggingface\hub\models--sentence-transformers--all-MiniLM-L6-v2
#  All other docs (docx, xlsx, pptx) will load at once - Use chunking.
#  Convert it ready for chunking.
try:
    doc: Any = converterPDF.convert(source=source).document
    print ("\nNote:  When the chunker command runs, it gives an error regarding token lengths.  Please disregard, no data has been lost or ignored. \n")
    chunk_iter: Any = chunker.chunk(doc)
    chunks: list[Any] = list(chunk_iter)
except:
    chunks: list[Any] = ""
    extracted_text = "No valid PDF data found."

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
#  ---------- Option 4 - Docling Native RapidOCR ----------
#
#  Use Docling's built-in RapidOCR for OCR processing
#  This is more integrated than Option 4's pytesseract approach
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import RapidOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

from typing import Any
import getpass
import os

strUserID: str = getpass.getuser()
#  Note:  (change from my file structure)
strPath: str = "/Users/"+strUserID+"/PythonVenv/IBMDocling"
os.chdir(path=strPath)

artifacts_path = "models"

# Configure RapidOCR options
# force_full_page_ocr=True will OCR all pages, even if text is extractable
# force_full_page_ocr=False (default) will only OCR when necessary
ocr_options: Any = RapidOcrOptions(
    force_full_page_ocr=False  # Set to True to force OCR on all pages
)

# Add OCR options to the pipeline
pipeline_options: Any = PdfPipelineOptions(
    artifacts_path=artifacts_path,
    ocr_options=ocr_options
)

# Create converter with RapidOCR enabled
doc_converter: Any = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

source: str = input("Enter document filename: ").strip()
#  source = "2408.09869v5.pdf"

try:
    print(f"\nProcessing PDF with Docling's native RapidOCR: {source}")
    print("This will use RapidOCR for text extraction when needed...\n")
    
    # Convert the document - RapidOCR will be used automatically
    result: Any = doc_converter.convert(source)
    
    # Export to markdown
    markdown_output: Any = result.document.export_to_markdown()
    print("Conversion complete!")
    print(f"Extracted text length: {len(markdown_output)} characters\n")
    print("First 500 characters of output:")
    print(markdown_output[:500])
    print("\n...")
    
    # Optionally save to file
    output_file = os.path.splitext(source)[0]+"_rapidocr_out.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    print(f"\nFull output saved to: {output_file}")
    
    # Access document structure for more details
    print(f"\nDocument metadata:")
    print(f"  Pages: {len(result.document.pages)}")
    
    # Count tables by iterating through document items safely
    table_count = 0
    try:
        for item in result.document.body:
            if hasattr(item, 'label') and 'table' in str(item.label).lower():
                table_count += 1
    except Exception:
        # If iteration fails, try alternative approach
        try:
            if hasattr(result.document, 'tables'):
                table_count = len(result.document.tables)
        except Exception:
            table_count = 0
    
    print(f"  Tables detected: {table_count}")
    
except Exception as e:
    print(f"Error processing PDF with RapidOCR: {str(e)}")
    
#
#  ---------- Option 5 - Docling Native EasyOCR ----------
#
#  Use Docling's built-in EasyOCR for OCR processing
#  This is an alternative to RapidOCR with different language support
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

from typing import Any
import getpass
import os

strUserID: str = getpass.getuser()
#  Note:  (change from my file structure)
strPath: str = "C:/Users/"+strUserID+"/PythonVenv/IBMDocling"
os.chdir(path=strPath)

artifacts_path = "models"

# Configure EasyOCR options
# force_full_page_ocr=True will OCR all pages, even if text is extractable
# force_full_page_ocr=False (default) will only OCR when necessary
ocr_options: Any = EasyOcrOptions(
    force_full_page_ocr=False  # Set to True to force OCR on all pages
)

# Add OCR options to the pipeline
pipeline_options: Any = PdfPipelineOptions(
    artifacts_path=artifacts_path,
    ocr_options=ocr_options
)

# Create converter with EasyOCR enabled
doc_converter: Any = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

source: str = input("Enter document filename: ").strip()
#  source = "2408.09869v5.pdf"

try:
    print(f"\nProcessing PDF with Docling's native EasyOCR: {source}")
    print("This will use EasyOCR for text extraction when needed...\n")
    
    # Convert the document - EasyOCR will be used automatically
    result: Any = doc_converter.convert(source)
    
    # Export to markdown
    markdown_output: Any = result.document.export_to_markdown()
    print("Conversion complete!")
    print(f"Extracted text length: {len(markdown_output)} characters\n")
    print("First 500 characters of output:")
    print(markdown_output[:500])
    print("\n...")
    
    # Optionally save to file
    output_file = os.path.splitext(source)[0]+"_easyocr_out.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(markdown_output)
    print(f"\nFull output saved to: {output_file}")
    
    # Access document structure for more details
    print(f"\nDocument metadata:")
    print(f"  Pages: {len(result.document.pages)}")
    
    # Count tables by iterating through document items safely
    table_count = 0
    try:
        for item in result.document.body:
            if hasattr(item, 'label') and 'table' in str(item.label).lower():
                table_count += 1
    except Exception:
        # If iteration fails, try alternative approach
        try:
            if hasattr(result.document, 'tables'):
                table_count = len(result.document.tables)
        except Exception:
            table_count = 0
    
    print(f"  Tables detected: {table_count}")
    
except Exception as e:
    print(f"Error processing PDF with EasyOCR: {str(e)}")



#
#  ---------- Document Packages ----------
#
#  For Win11 - Utilize requiements.txt - do not overwrite
#  venv/bin/python3 -m pip freeze > requirements.txt

#  Then can compare on a new machine -
#  to install using requirements.txt
#  venv/bin/python3 -m pip install  -r requirements.txt
