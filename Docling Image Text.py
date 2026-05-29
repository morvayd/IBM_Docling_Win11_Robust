
#
#  ---------- Option 5 - Extract Images from PDF with OCR ----------
#
#  Extract all images from PDF, perform OCR on each image, and save with original file type
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import getpass
import os

strUserID = getpass.getuser()
#  Note:  (change from my file structure)
os.chdir("/Users/"+strUserID+"/PythonVenv/IBMDocling")

# Create output directory for images
output_dir = "extracted_images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

source_pdf = "2408.09869v5.pdf"

try:
    # Open the PDF
    pdf_document = fitz.open(source_pdf)
    
    print(f"\nProcessing PDF: {source_pdf}")
    print(f"Total pages: {pdf_document.page_count}\n")
    
    image_count = 0
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        
        # Get list of images on the page
        image_list = page.get_images(full=True)
        
        if image_list:
            print(f"Page {page_num + 1}: Found {len(image_list)} image(s)")
        
        # Process each image
        for img_index, img in enumerate(image_list):
            xref = img[0]  # XREF number
            
            # Extract image
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]  # Get original file extension (png, jpg, etc.)
            
            # Convert bytes to PIL Image for OCR
            image = Image.open(io.BytesIO(image_bytes))
            
            # Perform OCR on the image
            try:
                ocr_text = pytesseract.image_to_string(image)
                if ocr_text.strip():
                    print(f"  Image {img_index + 1} - OCR extracted {len(ocr_text)} characters")
                    print(f"  OCR Text Preview: {ocr_text[:100]}...")
                else:
                    print(f"  Image {img_index + 1} - No text detected")
            except Exception as e:
                print(f"  Image {img_index + 1} - OCR failed: {str(e)}")
                ocr_text = ""
            
            # Save image with original file type
            image_count += 1
            image_filename = f"{output_dir}/page{page_num + 1}_img{img_index + 1}.{image_ext}"
            
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            
            print(f"  Saved: {image_filename}")
            
            # Optionally save OCR text to a separate file
            if ocr_text.strip():
                text_filename = f"{output_dir}/page{page_num + 1}_img{img_index + 1}_ocr.txt"
                with open(text_filename, "w", encoding="utf-8") as text_file:
                    text_file.write(ocr_text)
                print(f"  Saved OCR text: {text_filename}")
            
            print()
    
    pdf_document.close()
    
    print(f"\nTotal images extracted: {image_count}")
    print(f"Images saved to: {output_dir}/")
    
except Exception as e:
    print(f"Error processing PDF: {str(e)}")

#
#  ---------- Option 6 - Docling Native RapidOCR for Images ----------
#
#  Use Docling's built-in RapidOCR to process image files directly
#  Supports: PNG, JPG, JPEG, TIFF, BMP, and other common image formats
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import RapidOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption, ImageFormatOption

import getpass
import os

strUserID: str = getpass.getuser()
#  Note:  (change from my file structure)
os.chdir(path="/Users/"+strUserID+"/PythonVenv/IBMDocling")

artifacts_path = "models"

# Configure RapidOCR options for image processing
ocr_options: any = RapidOcrOptions(
    force_full_page_ocr=True  # Always use OCR for images
)

# Add OCR options to the pipeline
pipeline_options: any = PdfPipelineOptions(
    artifacts_path=artifacts_path,
    ocr_options=ocr_options
)

# Create converter with RapidOCR enabled for images
doc_converter: any = DocumentConverter(
    format_options={
        InputFormat.IMAGE: ImageFormatOption(pipeline_options=pipeline_options)
    }
)

# Prompt user for image filename
print("\n" + "="*60)
print("Docling Native RapidOCR - Image Processing")
print("="*60)
print("\nSupported formats: PNG, JPG, JPEG, TIFF, BMP, GIF")
print("Example: my_image.png or path/to/image.jpg\n")

image_source: str = input("Enter image filename: ").strip()
#  source = "2408.09869v5.pdf"

# Check if file exists
if not os.path.exists(path=image_source):
    print(f"\nError: File '{image_source}' not found!")
    print(f"Current directory: {os.getcwd()}")
else:
    try:
        print(f"\nProcessing image with Docling's native RapidOCR: {image_source}")
        print("Extracting text using RapidOCR...\n")
        
        # Convert the image - RapidOCR will extract text
        result: any = doc_converter.convert(image_source)
        
        # Export to markdown
        markdown_output: any = result.document.export_to_markdown()
        
        if markdown_output.strip():
            print("✓ OCR Extraction complete!")
            print(f"Extracted text length: {len(markdown_output)} characters\n")
            print("="*60)
            print("EXTRACTED TEXT:")
            print("="*60)
            print(markdown_output)
            print("="*60)
            
            # Save to file
            base_name: str = os.path.splitext(os.path.basename(image_source))[0]
            output_file: str = f"{base_name}_ocr_output.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown_output)
            print(f"\n✓ Full output saved to: {output_file}")
            
            # Also save as plain text
            text_output_file: str = f"{base_name}_ocr_output.txt"
            with open(text_output_file, "w", encoding="utf-8") as f:
                f.write(markdown_output)
            print(f"✓ Plain text saved to: {text_output_file}")
        else:
            print("⚠ No text detected in the image.")
            print("This could mean:")
            print("  - The image contains no text")
            print("  - The text is too small or unclear")
            print("  - The image format is not supported")
        
    except Exception as e:
        print(f"\n✗ Error processing image with RapidOCR: {str(e)}")
        print("\nTroubleshooting:")
        print("  - Verify the image file is not corrupted")
        print("  - Check that the image format is supported")
        print("  - Ensure the image contains readable text")
