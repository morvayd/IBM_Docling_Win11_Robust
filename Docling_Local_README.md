# Docling Local - PDF Document Processing with Local Models

## Overview

`Docling Local.py` is a comprehensive Python script that demonstrates various methods for processing PDF documents using IBM's Docling library with locally stored models. The script provides multiple options for document conversion, OCR processing, and text chunking, all designed to work offline without internet connectivity.

## Features

- **5 Processing Options:**
  1. Internet-based document conversion (verification)
  2. Local PDF processing with offline models
  3. Document chunking for large documents
  4. Native RapidOCR integration
  5. Native EasyOCR integration

- **Offline Operation:** All models stored locally in the `models/` directory
- **Multiple OCR Engines:** Support for RapidOCR and EasyOCR
- **Document Chunking:** Intelligent text segmentation using HybridChunker
- **Markdown Export:** Convert documents to markdown format
- **Metadata Extraction:** Access document structure, page count, and table detection

## Requirements

### Python Packages
```bash
pip install docling
pip install sentencepiece
pip install transformers
```

### Local Models Required

The script expects the following models in the `models/` directory:

1. **Docling Models:**
   - Layout detection models
   - Formula recognition models
   - Document classification models

2. **OCR Models:**
   - RapidOCR models (PP-OCRv4)
   - EasyOCR models (English)

3. **Tokenizer Models:**
   - sentence-transformers/all-MiniLM-L6-v2

## Installation

1. **Set up Python environment:**
   ```bash
   cd ~/PythonVenv/IBMDocling
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download models:**
   - Models should be placed in the `models/` directory
   - The script includes paths to local model storage

## Usage

### Option 1: Internet-Based Verification

Tests the installation with internet connectivity:

```python
from docling.document_converter import DocumentConverter

source = "https://arxiv.org/pdf/2408.09869"
converter = DocumentConverter()
doc = converter.convert(source).document
print(doc.export_to_markdown())
```

### Option 2: Local PDF Processing

Process PDFs offline using local models:

```python
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions

artifacts_path = "models"
pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path)

doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

result = doc_converter.convert("document.pdf")
markdown_output = result.document.export_to_markdown()
```

### Option 3: Document Chunking

Split large documents into manageable chunks:

```python
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer

tokenizer = HuggingFaceTokenizer(
    tokenizer=AutoTokenizer.from_pretrained(local_model_path),
    max_tokens=1024
)
chunker = HybridChunker(tokenizer=tokenizer, max_tokens=1024)

doc = converter.convert(source).document
chunks = list(chunker.chunk(doc))

# Access individual chunks
for i, chunk in enumerate(chunks):
    text = list(chunk)[0][1]
    print(f"Chunk {i}: {text}")
```

### Option 4: RapidOCR Processing

Use Docling's native RapidOCR for text extraction:

```python
from docling.datamodel.pipeline_options import RapidOcrOptions

ocr_options = RapidOcrOptions(
    force_full_page_ocr=False  # Set to True to force OCR on all pages
)

pipeline_options = PdfPipelineOptions(
    artifacts_path=artifacts_path,
    ocr_options=ocr_options
)
```

**Features:**
- Automatic OCR when text is not extractable
- Optional forced OCR on all pages
- Integrated with Docling's document structure

### Option 5: EasyOCR Processing

Alternative OCR engine with different language support:

```python
from docling.datamodel.pipeline_options import EasyOcrOptions

ocr_options = EasyOcrOptions(
    force_full_page_ocr=False
)

pipeline_options = PdfPipelineOptions(
    artifacts_path=artifacts_path,
    ocr_options=ocr_options
)
```

## Configuration

### File Paths

The script automatically configures paths based on the current user:

```python
strUserID = getpass.getuser()
strPath = f"/Users/{strUserID}/PythonVenv/IBMDocling"
os.chdir(path=strPath)
```

### Model Storage

Models are stored in the `models/` directory with the following structure:
```
models/
├── ds4sd--CodeFormulaV2/
├── ds4sd--docling-layout-heron/
├── ds4sd--SmolDocling-256M-preview/
├── RapidOcr/
├── EasyOcr/
└── models--sentence-transformers--all-MiniLM-L6-v2/
```

## Output

### Markdown Export
Documents are converted to markdown format with:
- Preserved document structure
- Tables and figures
- Headings and formatting
- Extracted text content

### Metadata
Access document information:
```python
print(f"Pages: {len(result.document.pages)}")
print(f"Tables detected: {table_count}")
```

### File Output
Results can be saved to files:
```python
output_file = os.path.splitext(source)[0] + "_output.md"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(markdown_output)
```

## Error Handling

The script includes comprehensive error handling:
- Try-except blocks for conversion failures
- Graceful handling of missing models
- User-friendly error messages
- Fallback options for failed operations

## Performance Considerations

- **Chunking:** May show token length warnings (can be disregarded)
- **OCR Processing:** Slower than direct text extraction
- **Model Loading:** Initial load time for local models
- **Memory Usage:** Large documents may require significant RAM

## Troubleshooting

### Common Issues

1. **Models not found:**
   - Verify models are in the correct directory
   - Check file paths in the script

2. **Import errors:**
   - Ensure all dependencies are installed
   - Activate the virtual environment

3. **OCR failures:**
   - Check image quality in PDF
   - Try different OCR engines (RapidOCR vs EasyOCR)

4. **Chunking errors:**
   - Token length warnings can be ignored
   - Adjust max_tokens parameter if needed

## Package Management

### Save current environment:
```bash
venv/bin/python3 -m pip freeze > requirements.txt
```

### Install from requirements:
```bash
venv/bin/python3 -m pip install -r requirements.txt
```

## References

- [Docling Documentation](https://docling-project.github.io/docling/)
- IBM Docling Project
- RapidOCR Documentation
- EasyOCR Documentation

## Notes

- Designed for macOS (paths may need adjustment for other OS)
- Requires local model storage for offline operation
- Supports multiple document formats (PDF, DOCX, XLSX, PPTX)
- All processing can be done without internet connectivity

## License

Refer to the LICENSE file in the project directory.

## Author

Created for offline document processing with IBM Docling.