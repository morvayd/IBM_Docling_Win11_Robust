# Extract Image Text - PDF Image Extraction and OCR Processing

## Overview

`Extract Image Text.py` is a dual-purpose Python script that provides two powerful options for extracting and processing images from PDFs and standalone image files. It combines PDF image extraction with OCR capabilities using both PyMuPDF (fitz) and IBM's Docling library with RapidOCR integration.

## Key Features

- **Two Processing Options:**
  1. Extract all images from PDFs with OCR on each image
  2. Process standalone image files with Docling's native RapidOCR

- **Automatic Image Extraction:** Extracts images from PDFs while preserving original format
- **OCR on Extracted Images:** Performs OCR on each extracted image
- **Multiple Output Formats:** Saves images, OCR text, and markdown output
- **Format Preservation:** Maintains original image file types (PNG, JPG, etc.)
- **Comprehensive Metadata:** Provides page numbers, image counts, and text statistics

## Requirements

### Python Packages

```bash
pip install PyMuPDF  # fitz
pip install pytesseract
pip install Pillow
pip install docling
```

### System Requirements

- **Tesseract OCR:** Must be installed on the system
  - macOS: `brew install tesseract`
  - Linux: `apt-get install tesseract-ocr`
  - Windows: Download from GitHub releases

### Local Models (for Option 6)

Models should be stored in the `models/` directory:
```
models/
└── RapidOcr/
    └── onnx/
        └── PP-OCRv4/
            ├── det/ch_PP-OCRv4_det_infer.onnx
            ├── rec/ch_PP-OCRv4_rec_infer.onnx
            └── cls/ch_ppocr_mobile_v2.0_cls_infer.onnx
```

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install PyMuPDF pytesseract Pillow docling
   ```

2. **Install Tesseract (system-level):**
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   ```

3. **Set up working directory:**
   ```bash
   cd ~/PythonVenv/IBMDocling
   ```

## Usage

The script provides two distinct options that can be run independently.

### Option 5: Extract Images from PDF with OCR

Extracts all images from a PDF file and performs OCR on each image.

#### Features:
- Extracts images from all pages
- Preserves original image format (PNG, JPG, etc.)
- Performs OCR on each extracted image
- Saves images and OCR text separately
- Provides detailed extraction statistics

#### Code Example:

```python
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

source_pdf = "2408.09869v5.pdf"
output_dir = "extracted_images"

# Open PDF and extract images
pdf_document = fitz.open(source_pdf)

for page_num in range(len(pdf_document)):
    page = pdf_document[page_num]
    image_list = page.get_images(full=True)
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = pdf_document.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        # Perform OCR
        image = Image.open(io.BytesIO(image_bytes))
        ocr_text = pytesseract.image_to_string(image)
        
        # Save image and text
        image_filename = f"{output_dir}/page{page_num+1}_img{img_index+1}.{image_ext}"
        text_filename = f"{output_dir}/page{page_num+1}_img{img_index+1}_ocr.txt"
```

#### Output Structure:

```
extracted_images/
├── page1_img1.png
├── page1_img1_ocr.txt
├── page2_img1.jpg
├── page2_img1_ocr.txt
├── page3_img1.png
└── page3_img1_ocr.txt
```

#### Sample Output:

```
Processing PDF: 2408.09869v5.pdf
Total pages: 15

Page 1: Found 2 image(s)
  Image 1 - OCR extracted 245 characters
  OCR Text Preview: Docling Technical Report...
  Saved: extracted_images/page1_img1.png
  Saved OCR text: extracted_images/page1_img1_ocr.txt

Page 2: Found 1 image(s)
  Image 1 - OCR extracted 189 characters
  OCR Text Preview: Figure 1: Architecture diagram...
  Saved: extracted_images/page2_img1.jpg
  Saved OCR text: extracted_images/page2_img1_ocr.txt

Total images extracted: 15
Images saved to: extracted_images/
```

### Option 6: Docling Native RapidOCR for Images

Process standalone image files directly using Docling's integrated RapidOCR engine.

#### Features:
- Direct image processing (no PDF required)
- Docling's native RapidOCR integration
- Markdown and plain text output
- Support for multiple image formats
- Detailed extraction statistics

#### Supported Image Formats:
- PNG (.png)
- JPEG (.jpg, .jpeg)
- TIFF (.tiff, .tif)
- BMP (.bmp)
- GIF (.gif)

#### Code Example:

```python
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import RapidOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, ImageFormatOption

artifacts_path = "models"

# Configure RapidOCR for images
ocr_options = RapidOcrOptions(force_full_page_ocr=True)
pipeline_options = PdfPipelineOptions(
    artifacts_path=artifacts_path,
    ocr_options=ocr_options
)

# Create converter
doc_converter = DocumentConverter(
    format_options={
        InputFormat.IMAGE: ImageFormatOption(pipeline_options=pipeline_options)
    }
)

# Process image
image_source = "my_image.png"
result = doc_converter.convert(image_source)
markdown_output = result.document.export_to_markdown()
```

#### Interactive Usage:

```
==============================================================
Docling Native RapidOCR - Image Processing
==============================================================

Supported formats: PNG, JPG, JPEG, TIFF, BMP, GIF
Example: my_image.png or path/to/image.jpg

Enter image filename: Images/Billboard.jpg

Processing image with Docling's native RapidOCR: Images/Billboard.jpg
Extracting text using RapidOCR...

✓ OCR Extraction complete!
Extracted text length: 245 characters

==============================================================
EXTRACTED TEXT:
==============================================================
WELCOME TO OUR STORE
SPECIAL OFFERS TODAY
...
==============================================================

✓ Full output saved to: Billboard_ocr_output.md
✓ Plain text saved to: Billboard_ocr_output.txt
```

#### Output Files:

For an image named `Billboard.jpg`:
- `Billboard_ocr_output.md` - Markdown formatted output
- `Billboard_ocr_output.txt` - Plain text output

## Configuration

### Working Directory

The script automatically sets the working directory:

```python
strUserID = getpass.getuser()
os.chdir(f"/Users/{strUserID}/PythonVenv/IBMDocling")
```

### Output Directory (Option 5)

Images are saved to the `extracted_images/` directory:

```python
output_dir = "extracted_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
```

### OCR Options (Option 6)

Configure RapidOCR behavior:

```python
ocr_options = RapidOcrOptions(
    force_full_page_ocr=True  # Always use OCR for images
)
```

## Output Details

### Option 5 Output

**Image Files:**
- Saved with original format (PNG, JPG, etc.)
- Named: `page{N}_img{M}.{ext}`
- Preserves original quality

**OCR Text Files:**
- Plain text format
- Named: `page{N}_img{M}_ocr.txt`
- Contains extracted text from corresponding image

**Console Output:**
```
Page 1: Found 2 image(s)
  Image 1 - OCR extracted 245 characters
  OCR Text Preview: Docling Technical Report[...]
  Saved: extracted_images/page1_img1.png
  Saved OCR text: extracted_images/page1_img1_ocr.txt
```

### Option 6 Output

**Markdown File:**
- Structured markdown format
- Named: `{image_name}_ocr_output.md`
- Preserves document structure

**Text File:**
- Plain text format
- Named: `{image_name}_ocr_output.txt`
- Raw extracted text

**Console Output:**
```
✓ OCR Extraction complete!
Extracted text length: 245 characters

==============================================================
EXTRACTED TEXT:
==============================================================
[Full extracted text displayed]
==============================================================

✓ Full output saved to: Billboard_ocr_output.md
✓ Plain text saved to: Billboard_ocr_output.txt
```

## Error Handling

### Option 5 Error Handling

```python
try:
    ocr_text = pytesseract.image_to_string(image)
    if ocr_text.strip():
        print(f"Image {img_index + 1} - OCR extracted {len(ocr_text)} characters")
    else:
        print(f"Image {img_index + 1} - No text detected")
except Exception as e:
    print(f"Image {img_index + 1} - OCR failed: {str(e)}")
    ocr_text = ""
```

### Option 6 Error Handling

```python
try:
    result = doc_converter.convert(image_source)
    markdown_output = result.document.export_to_markdown()
    
    if markdown_output.strip():
        print("✓ OCR Extraction complete!")
    else:
        print("⚠ No text detected in the image.")
        print("This could mean:")
        print("  - The image contains no text")
        print("  - The text is too small or unclear")
        print("  - The image format is not supported")
except Exception as e:
    print(f"✗ Error processing image: {str(e)}")
```

## Use Cases

### Option 5: PDF Image Extraction
- **Document Analysis:** Extract all figures and diagrams from research papers
- **Data Collection:** Gather images from multiple PDF documents
- **Text Mining:** Extract text from embedded images in PDFs
- **Archive Creation:** Create searchable image archives from PDFs

### Option 6: Standalone Image OCR
- **Single Image Processing:** Quick OCR on individual images
- **Batch Processing:** Process multiple standalone images
- **Format Conversion:** Convert images to searchable text
- **Quality Testing:** Test OCR accuracy on specific images

## Performance Considerations

### Option 5 Performance
- **Processing Time:** Depends on number of images and PDF size
- **Memory Usage:** Loads one page at a time to conserve memory
- **OCR Speed:** Tesseract processing time varies with image complexity
- **Storage:** Saves all images and text files to disk

### Option 6 Performance
- **Model Loading:** Initial load time for RapidOCR models
- **Processing Speed:** Generally faster than Tesseract
- **Memory Usage:** Efficient with local models
- **Accuracy:** High accuracy with RapidOCR engine

## Troubleshooting

### Common Issues

#### 1. Tesseract Not Found
```
Error: Tesseract not installed
```
**Solution:**
```bash
# macOS
brew install tesseract

# Linux
sudo apt-get install tesseract-ocr
```

#### 2. No Images Found in PDF
```
Total images extracted: 0
```
**Possible Causes:**
- PDF contains no embedded images
- Images are rendered as vector graphics
- PDF is text-only

#### 3. No Text Detected
```
⚠ No text detected in the image
```
**Solutions:**
- Check image quality and resolution
- Ensure text is clearly visible
- Try preprocessing the image
- Verify image contains actual text

#### 4. File Not Found
```
Error: File 'image.png' not found!
```
**Solution:**
- Verify file path is correct
- Check current working directory
- Use absolute paths if needed

### Model Issues (Option 6)

If RapidOCR models are missing:
```
Error: RapidOCR models not found
```

**Solution:**
Ensure models are in correct location:
```
models/RapidOcr/onnx/PP-OCRv4/
├── det/ch_PP-OCRv4_det_infer.onnx
├── rec/ch_PP-OCRv4_rec_infer.onnx
└── cls/ch_ppocr_mobile_v2.0_cls_infer.onnx
```

## Best Practices

### Image Quality
1. **Resolution:** Higher resolution improves OCR accuracy
2. **Contrast:** Ensure good contrast between text and background
3. **Orientation:** Keep text properly oriented
4. **Format:** Use lossless formats (PNG, TIFF) when possible

### File Organization
1. **Output Directories:** Keep extracted images organized
2. **Naming Conventions:** Use descriptive filenames
3. **Backup:** Keep original PDFs and images
4. **Documentation:** Save OCR results with source references

### Processing Strategy
1. **Test First:** Process a few pages/images before batch processing
2. **Review Results:** Check OCR accuracy on sample outputs
3. **Adjust Settings:** Modify OCR parameters if needed
4. **Error Handling:** Monitor console output for errors

## Advanced Usage

### Custom Output Directory

Modify the output directory:
```python
output_dir = "my_custom_folder"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
```

### Selective Image Extraction

Extract only specific image types:
```python
for img in enumerate(image_list):
    base_image = pdf_document.extract_image(xref)
    if base_image["ext"] == "png":  # Only PNG images
        # Process image
```

### Custom OCR Configuration

For Tesseract (Option 5):
```python
custom_config = r'--oem 3 --psm 6'
ocr_text = pytesseract.image_to_string(image, config=custom_config)
```

For RapidOCR (Option 6):
```python
ocr_options = RapidOcrOptions(
    force_full_page_ocr=True,
    # Add custom parameters as supported
)
```

## Integration Examples

### Batch Processing Multiple PDFs

```python
import os

pdf_folder = "pdfs"
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        source_pdf = os.path.join(pdf_folder, filename)
        # Process each PDF
```

### Combining with Other Tools

```python
# After extraction, process with other OCR engines
from PIL import Image
import easyocr

reader = easyocr.Reader(['en'])
result = reader.readtext(image_path)
```

## Limitations

1. **Vector Graphics:** Cannot extract text rendered as vectors
2. **Encrypted PDFs:** May not work with password-protected PDFs
3. **Complex Layouts:** Multi-column or complex layouts may be challenging
4. **Handwriting:** Limited support for handwritten text
5. **Image Quality:** Poor quality images will have poor OCR results

## Comparison: Option 5 vs Option 6

| Feature | Option 5 (PDF Extraction) | Option 6 (Direct Image) |
|---------|---------------------------|-------------------------|
| Input | PDF files | Image files |
| OCR Engine | Tesseract | RapidOCR |
| Output | Images + Text files | Markdown + Text |
| Use Case | Extract from PDFs | Process standalone images |
| Speed | Moderate | Fast |
| Accuracy | Good | High |
| Format Support | PDF embedded images | PNG, JPG, TIFF, BMP, GIF |

## References

- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Docling Documentation](https://docling-project.github.io/docling/)
- [RapidOCR](https://github.com/RapidAI/RapidOCR)

## License

Refer to the LICENSE file in the project directory.

## Notes

- Designed for macOS (paths may need adjustment for other OS)
- Requires local model storage for Option 6
- Both options can be used independently
- Suitable for both single-file and batch processing

## Author

Created for comprehensive image extraction and OCR processing with IBM Docling and PyMuPDF.