# IBM Docling OCR Toolkit

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docling](https://img.shields.io/badge/IBM-Docling-blue.svg)](https://docling-project.github.io/docling/)

A comprehensive toolkit for document processing and OCR (Optical Character Recognition) using IBM's Docling library and multiple OCR engines. This repository provides three powerful Python scripts for offline document processing, multi-engine OCR comparison, and image extraction with text recognition.

## 🚀 Features

- **Offline Document Processing** - Process PDFs without internet connectivity using local models
- **Multi-Engine OCR** - Compare results from EasyOCR, Tesseract, and RapidOCR
- **Batch Processing** - Process multiple images or documents automatically
- **Image Extraction** - Extract and OCR images from PDF documents
- **Markdown Export** - Convert documents to structured markdown format
- **Document Chunking** - Intelligent text segmentation for large documents
- **Local Model Storage** - All models stored locally for complete offline operation

## 📋 Table of Contents

- [Scripts Overview](#scripts-overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Detailed Documentation](#detailed-documentation)
- [Requirements](#requirements)
- [Model Setup](#model-setup)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 📦 Scripts Overview

### 1. Docling Local (`Docling Local.py`)

Process PDF documents using IBM's Docling library with locally stored models. Supports multiple processing modes including document chunking and native OCR integration.

**Key Features:**
- 5 processing options (internet-based verification, local processing, chunking, RapidOCR, EasyOCR)
- Offline operation with local models
- Markdown export with preserved document structure
- Table and figure detection
- Metadata extraction

**Use Cases:**
- Offline PDF processing
- Document conversion to markdown
- Large document chunking
- Research paper analysis

[📖 Full Documentation](Docling_Local_README.md)

### 2. Docling OCR Compare (`Docling OCR Compare.py`)

Multi-engine OCR batch processor that compares results from three different OCR engines and automatically selects the best output.

**Key Features:**
- Tests 3 OCR engines: EasyOCR, Tesseract, RapidOCR
- Batch processing of entire image folders
- Automatic best result selection
- Comprehensive comparison reports
- Confidence scoring

**Use Cases:**
- Challenging image OCR
- Quality comparison between OCR engines
- Batch image text extraction
- OCR accuracy testing

[📖 Full Documentation](Docling_OCR_Compare_README.md)

### 3. Extract Image Text (`Extract Image Text.py`)

Dual-purpose script for extracting images from PDFs with OCR, and processing standalone images using Docling's RapidOCR.

**Key Features:**
- Extract all images from PDF documents
- OCR on extracted images
- Standalone image processing
- Multiple output formats (markdown, text)
- Format preservation

**Use Cases:**
- PDF image extraction
- Figure and diagram extraction from research papers
- Standalone image OCR
- Creating searchable image archives

[📖 Full Documentation](Extract_Image_Text_README.md)

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Tesseract OCR (system-level installation)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/IBMDocling.git
cd IBMDocling
```

### Step 2: Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Python Dependencies

```bash
#  ----- Best - Error Free -----
pip install -r requirements.txt
```

Or install individually:

```bash
pip install docling
pip install easyocr
pip install pytesseract
pip install rapidocr-onnxruntime
pip install PyMuPDF
pip install Pillow
pip install sentencepiece
pip install transformers
```

### Step 4: Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from [GitHub Releases](https://github.com/tesseract-ocr/tesseract)

## 🚀 Quick Start

### Process a PDF Document Offline

```python
python3 "Docling Local.py"
# Select Option 2 for local PDF processing
```

### Compare OCR Engines on Images

```bash
python3 "Docling OCR Compare.py"
# Enter folder name when prompted (e.g., "Images")
```

### Extract Images from PDF

```python
python3 "Extract Image Text.py"
# Use Option 5 for PDF image extraction
```

## 📚 Detailed Documentation

Each script has comprehensive documentation:

- **[Docling Local Documentation](Docling_Local_README.md)** - Complete guide for PDF processing with local models
- **[Docling OCR Compare Documentation](Docling_OCR_Compare_README.md)** - Multi-engine OCR comparison guide
- **[Extract Image Text Documentation](Extract_Image_Text_README.md)** - Image extraction and OCR guide

## 📋 Requirements

### Python Packages

| Package | Purpose | Script |
|---------|---------|--------|
| docling | IBM's document processing library | All |
| easyocr | High-accuracy OCR engine | OCR Compare, Docling Local |
| pytesseract | Tesseract OCR wrapper | OCR Compare, Extract Image |
| rapidocr-onnxruntime | Fast OCR engine | OCR Compare, Docling Local |
| PyMuPDF (fitz) | PDF processing | Extract Image |
| Pillow | Image processing | All |
| sentencepiece | Tokenization | Docling Local |
| transformers | Model loading | Docling Local |

### System Requirements

- **Operating System:** macOS, Linux, or Windows
- **RAM:** 8GB minimum, 16GB recommended
- **Storage:** 5GB for models and dependencies
- **Tesseract OCR:** System-level installation required

## 🗂️ Model Setup

Models should be organized in the `models/` directory:

```
models/
├── ds4sd--CodeFormulaV2/          # Formula recognition
├── ds4sd--docling-layout-heron/   # Layout detection
├── ds4sd--SmolDocling-256M-preview/ # Document processing
├── ibm-granite--granite-docling-258M/ # Granite models
├── EasyOcr/                       # EasyOCR models
│   ├── craft_mlt_25k.pth
│   ├── english_g2.pth
│   └── latin_g2.pth
├── RapidOcr/                      # RapidOCR models
│   └── onnx/PP-OCRv4/
│       ├── det/ch_PP-OCRv4_det_infer.onnx
│       ├── rec/ch_PP-OCRv4_rec_infer.onnx
│       └── cls/ch_ppocr_mobile_v2.0_cls_infer.onnx
└── models--sentence-transformers--all-MiniLM-L6-v2/ # Tokenizer
```

### Downloading Models

1. **Docling Models:** Download from [Hugging Face](https://huggingface.co/ds4sd)
2. **EasyOCR Models:** Auto-download on first run or manual download
3. **RapidOCR Models:** Download from [RapidOCR GitHub](https://github.com/RapidAI/RapidOCR)
4. **Tokenizer Models:** Download from Hugging Face or use the script's auto-download

## 💡 Usage Examples

### Example 1: Process PDF with Local Models

```python
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

artifacts_path = "models"
pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path)

doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

result = doc_converter.convert("document.pdf")
markdown_output = result.document.export_to_markdown()
print(markdown_output)
```

### Example 2: Batch OCR with Multiple Engines

```bash
python3 "Docling OCR Compare.py"
# Enter: Images
# Script processes all images and generates comparison reports
```

### Example 3: Extract Images from PDF

```python
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

pdf_document = fitz.open("document.pdf")
output_dir = "extracted_images"

for page_num in range(len(pdf_document)):
    page = pdf_document[page_num]
    image_list = page.get_images(full=True)
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = pdf_document.extract_image(xref)
        image_bytes = base_image["image"]
        
        # Perform OCR
        image = Image.open(io.BytesIO(image_bytes))
        ocr_text = pytesseract.image_to_string(image)
        
        # Save results
        with open(f"{output_dir}/page{page_num+1}_img{img_index+1}_ocr.txt", "w") as f:
            f.write(ocr_text)
```

## 🔍 Troubleshooting

### Common Issues

#### Models Not Found
```
Error: Models not found in expected location
```
**Solution:** Verify models are in the `models/` directory with correct structure.

#### Tesseract Not Installed
```
Error: Tesseract not installed
```
**Solution:** Install Tesseract using system package manager (see Installation section).

#### Import Errors
```
ModuleNotFoundError: No module named 'docling'
```
**Solution:** Activate virtual environment and install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### No Text Detected
```
⚠ No text detected in the image
```
**Solutions:**
- Check image quality and resolution
- Ensure good contrast between text and background
- Try different OCR engines
- Verify image contains readable text

### Performance Tips

1. **GPU Acceleration:** Enable GPU for EasyOCR if available
2. **Batch Processing:** Process multiple files in one session
3. **Model Caching:** Keep models loaded for repeated operations
4. **Image Quality:** Use high-resolution images for better accuracy

## 📊 Comparison: OCR Engines

| Feature | EasyOCR | Tesseract | RapidOCR |
|---------|---------|-----------|----------|
| **Accuracy** | High | Good | High |
| **Speed** | Moderate | Fast | Very Fast |
| **Languages** | 80+ | 100+ | Chinese/English |
| **GPU Support** | Yes | No | No |
| **Best For** | Complex layouts | Standard documents | Fast processing |
| **Preprocessing** | Built-in | Manual | Built-in |

## 🎯 Use Cases

### Research & Academia
- Extract text from research papers
- Process scanned documents
- Extract figures and tables
- Create searchable archives

### Business & Enterprise
- Document digitization
- Invoice processing
- Form recognition
- Archive management

### Development & Testing
- OCR accuracy testing
- Engine comparison
- Batch processing automation
- Quality assurance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [IBM Docling Project](https://docling-project.github.io/docling/) - Document processing framework
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - OCR engine
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - OCR engine
- [RapidOCR](https://github.com/RapidAI/RapidOCR) - Fast OCR engine
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF processing

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

## 🔗 References

- [Docling Documentation](https://docling-project.github.io/docling/)
- [EasyOCR Documentation](https://github.com/JaidedAI/EasyOCR)
- [Tesseract Documentation](https://github.com/tesseract-ocr/tesseract)
- [RapidOCR Documentation](https://github.com/RapidAI/RapidOCR)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)

---

**Made with ❤️ for offline document processing and OCR**

