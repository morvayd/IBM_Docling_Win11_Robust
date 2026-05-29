# Docling OCR Compare - Multi-Engine OCR Batch Processor

## Overview

`Docling OCR Compare.py` is a sophisticated batch OCR processing tool that uses multiple OCR engines to extract text from images. The script automatically compares results from different OCR methods and selects the best output, making it ideal for challenging images where a single OCR engine might fail.

## Key Features

- **Multi-Engine Approach:** Tests 3 different OCR engines on each image
- **Batch Processing:** Process entire folders of images automatically
- **Automatic Best Selection:** Chooses the OCR result with the most extracted text
- **Comprehensive Comparison:** Saves detailed comparison of all methods
- **Robust Error Handling:** Continues processing even if individual methods fail
- **Detailed Reporting:** Provides confidence scores and character counts
- **Multiple Output Formats:** Saves both comparison files and best results

## Supported OCR Engines

### 1. EasyOCR (Primary)
- **Best for:** Complex layouts, challenging images
- **Accuracy:** High accuracy mode
- **Features:**
  - Confidence scores for each text region
  - Paragraph detection
  - Multi-language support (configured for English)
  - Local model storage

### 2. Tesseract OCR (Secondary)
- **Best for:** Preprocessed images, standard documents
- **Features:**
  - Multiple PSM (Page Segmentation Mode) configurations
  - Image preprocessing (contrast enhancement, sharpening)
  - Automatic mode selection for best results
  - Grayscale conversion

### 3. RapidOCR Direct (Tertiary)
- **Best for:** Fast processing, Chinese/English text
- **Features:**
  - Direct ONNX model usage
  - PP-OCRv4 models
  - Confidence scoring
  - Efficient processing

## Requirements

### Python Packages
```bash
pip install easyocr
pip install pytesseract
pip install rapidocr-onnxruntime
pip install Pillow
```

### System Requirements
- **Tesseract:** Must be installed on the system
  - macOS: `brew install tesseract`
  - Linux: `apt-get install tesseract-ocr`
  - Windows: Download from GitHub releases

### Local Models

Models should be stored in the `models/` directory:

```
models/
├── EasyOcr/
│   ├── craft_mlt_25k.pth
│   ├── english_g2.pth
│   └── latin_g2.pth
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
   pip install easyocr pytesseract rapidocr-onnxruntime Pillow
   ```

2. **Install Tesseract (system-level):**
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   ```

3. **Download OCR models:**
   - EasyOCR models will download automatically on first run
   - RapidOCR models should be placed in `models/RapidOcr/`

## Usage

### Basic Usage

Run the script and follow the prompts:

```bash
python3 "Docling OCR Compare.py"
```

The script will:
1. Ask for the folder name containing images
2. Scan for all supported image formats
3. Process each image with all available OCR engines
4. Save comparison and best results

### Interactive Example

```
BATCH OCR EXTRACTION - Multi-Engine Approach
==============================================================

Enter folder name containing images (e.g., Images): Images

✓ Found folder: Images
✓ Found 3 image(s) to process

Images found:
  • Billboard.jpg
  • ImageInImage.tiff
  • Xsem1.png

STARTING BATCH PROCESSING
==============================================================
```

### Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- TIFF (.tiff, .tif)
- BMP (.bmp)
- GIF (.gif)

## Output Files

For each processed image, the script generates two files:

### 1. Comparison File
**Filename:** `{image_name}_all_methods_comparison.txt`

Contains results from all OCR methods:
```
IMAGE: Billboard.jpg
======================================================================

======================================================================
METHOD: EasyOCR
======================================================================

Status: SUCCESS - Extracted 245 characters

[Extracted text content...]

======================================================================
METHOD: Tesseract
======================================================================

Status: SUCCESS - Extracted 198 characters

[Extracted text content...]

======================================================================
METHOD: RapidOCR_Direct
======================================================================

Status: FAILED - No text extracted

# No text was detected by this OCR method.
# Possible reasons:
#   - Image quality too low
#   - Text too small or unclear
#   - Poor contrast between text and background
```

### 2. Best Result File
**Filename:** `{image_name}_fixed_ocr_output.txt`

Contains only the best OCR result:
```
OCR Method: EasyOCR
======================================================================

[Best extracted text content...]
```

## How It Works

### Processing Pipeline

1. **Image Discovery:**
   - Scans specified folder for image files
   - Filters by supported extensions
   - Lists all found images

2. **Multi-Engine Processing:**
   - **EasyOCR:** High-accuracy extraction with confidence scores
   - **Tesseract:** Multiple PSM modes with preprocessing
   - **RapidOCR:** Direct ONNX model processing

3. **Result Comparison:**
   - Tracks all results (including failures)
   - Compares character counts
   - Selects method with longest output

4. **File Generation:**
   - Saves comprehensive comparison file
   - Saves best result separately
   - Provides detailed statistics

### OCR Method Details

#### EasyOCR Processing
```python
reader = easyocr.Reader(
    ['en'],
    model_storage_directory='models/EasyOcr',
    download_enabled=False,
    gpu=False,
    verbose=False
)
result = reader.readtext(image_path, detail=1, paragraph=False)
```

**Output includes:**
- Bounding boxes for each text region
- Extracted text
- Confidence scores (0-1)

#### Tesseract Processing
```python
# Image preprocessing
img = img.convert('L')  # Grayscale
img = ImageEnhance.Contrast(img).enhance(2.0)  # Contrast
img = img.filter(ImageFilter.SHARPEN)  # Sharpen

# Multiple PSM modes
configs = ['--psm 6', '--psm 3', '--psm 11', '--psm 12']
```

**PSM Modes:**
- PSM 6: Uniform block of text
- PSM 3: Fully automatic page segmentation
- PSM 11: Sparse text
- PSM 12: Sparse text with OSD

#### RapidOCR Processing
```python
engine = RapidOCR(
    det_model_path=det_model,
    rec_model_path=rec_model,
    cls_model_path=cls_model
)
result, elapse = engine(image_path)
```

**Features:**
- Text detection (det)
- Text recognition (rec)
- Text classification (cls)

## Performance Statistics

The script provides detailed statistics:

```
✓ Successfully processed: 2/3 images
✗ Failed to extract text: 1/3 images

✓ All output files saved to: Images/
```

For each image:
```
✓ 2 method(s) extracted text
🏆 Best: EasyOCR (245 characters)
✓ Comparison saved to: Billboard_all_methods_comparison.txt
✓ Best result saved to: Billboard_fixed_ocr_output.txt
```

## Error Handling

### Graceful Degradation
- If one OCR engine fails, others continue
- Missing dependencies are reported but don't stop processing
- Corrupted images are skipped with error messages

### Failure Documentation
Failed methods are documented in comparison files:
```
Status: FAILED - No text extracted

# No text was detected by this OCR method.
# Possible reasons:
#   - Image quality too low
#   - Text too small or unclear
#   - Poor contrast between text and background
#   - Image contains no readable text
#   - OCR engine not properly configured
```

## Troubleshooting

### No Text Extracted

If all methods fail:

1. **Check image quality:**
   - Is the text clear and readable?
   - Is there sufficient contrast?

2. **Try image preprocessing:**
   - Increase resolution
   - Adjust contrast/brightness
   - Convert to different format

3. **Verify installations:**
   ```bash
   pip list | grep -E "easyocr|pytesseract|rapidocr"
   tesseract --version
   ```

### Missing Dependencies

Install missing OCR engines:
```bash
pip install easyocr
pip install pytesseract
pip install rapidocr-onnxruntime
```

### Model Not Found

For RapidOCR, ensure models are in correct location:
```
models/RapidOcr/onnx/PP-OCRv4/
├── det/ch_PP-OCRv4_det_infer.onnx
├── rec/ch_PP-OCRv4_rec_infer.onnx
└── cls/ch_ppocr_mobile_v2.0_cls_infer.onnx
```

## Best Practices

### Image Preparation
1. **Resolution:** Higher resolution generally improves accuracy
2. **Contrast:** Ensure good contrast between text and background
3. **Format:** PNG or TIFF for best quality
4. **Orientation:** Ensure text is properly oriented

### Batch Processing
1. **Organize images:** Keep images in dedicated folders
2. **Consistent naming:** Use descriptive filenames
3. **Review results:** Check comparison files for quality assessment
4. **Iterate:** Reprocess failed images with preprocessing

### Performance Optimization
1. **GPU acceleration:** Enable GPU for EasyOCR if available
2. **Parallel processing:** Process multiple images simultaneously
3. **Model caching:** Keep models loaded for batch operations

## Advanced Usage

### Custom Configuration

Modify OCR parameters in the script:

```python
# EasyOCR - Add more languages
reader = easyocr.Reader(['en', 'fr', 'de'])

# Tesseract - Custom PSM modes
configs = ['--psm 6 --oem 3']

# RapidOCR - Adjust confidence threshold
# (modify in source code)
```

### Integration

Use functions independently:
```python
from script import extract_with_easyocr

text = extract_with_easyocr("my_image.png")
if text:
    print(f"Extracted: {text}")
```

## Output Analysis

### Confidence Scores

EasyOCR and RapidOCR provide confidence scores:
```
1. [95.23%] WELCOME
2. [87.45%] TO OUR
3. [92.18%] STORE
```

Higher percentages indicate more confident detections.

### Character Count Comparison

The script uses character count as a quality metric:
- More characters often indicates better extraction
- However, verify accuracy manually for critical applications

## Limitations

1. **Handwriting:** Limited support for handwritten text
2. **Complex layouts:** May struggle with multi-column layouts
3. **Low quality:** Very low-resolution images may fail
4. **Special characters:** Some symbols may not be recognized
5. **Language support:** Configured for English by default

## Future Enhancements

Potential improvements:
- GPU acceleration support
- Additional OCR engines (PaddleOCR, TrOCR)
- Image preprocessing pipeline
- Confidence-based selection (not just length)
- Multi-language support
- Parallel processing for large batches

## References

- [EasyOCR Documentation](https://github.com/JaidedAI/EasyOCR)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [RapidOCR](https://github.com/RapidAI/RapidOCR)

## License

Refer to the LICENSE file in the project directory.

## Credits

Made with Bob - Enhanced OCR solution for challenging images.