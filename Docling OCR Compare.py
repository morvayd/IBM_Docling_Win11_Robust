#!/usr/bin/env python3
"""
Fix OCR Extraction - Enhanced solution for images that don't extract text
Uses multiple strategies to improve OCR accuracy
"""

import os
import getpass

# Change to working directory
strUserID = getpass.getuser()
os.chdir(f"/Users/{strUserID}/PythonVenv/IBMDocling")

def extract_with_easyocr(image_path):
    """
    EasyOCR - Often better for challenging images
    More accurate than RapidOCR for complex layouts
    """
    try:
        import easyocr
        
        print("\n" + "="*60)
        print("Using EasyOCR (High Accuracy Mode)")
        print("="*60)
        
        # Initialize with English language
        # Using your local models directory
        reader = easyocr.Reader(
            ['en'],
            model_storage_directory='models/EasyOcr',
            download_enabled=False,
            gpu=False,
            verbose=False
        )
        
        print(f"Processing: {image_path}")
        
        # Extract text with detailed results
        result = reader.readtext(image_path, detail=1, paragraph=False)
        
        if result:
            # Extract text and confidence scores
            extracted_lines = []
            print(f"\n✓ Detected {len(result)} text regions:\n")
            
            for idx, (bbox, text, confidence) in enumerate(result, 1):
                print(f"  {idx}. [{confidence:.2%}] {text}")
                extracted_lines.append(text)
            
            full_text = "\n".join(extracted_lines)
            
            print(f"\n✓ Total characters extracted: {len(full_text)}")
            return full_text
        else:
            print("✗ No text detected")
            return None
            
    except ImportError:
        print("✗ EasyOCR not installed. Install with: pip install easyocr")
        return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

def extract_with_tesseract(image_path):
    """
    Tesseract - Good fallback option
    Works well with preprocessed images
    """
    try:
        import pytesseract
        from PIL import Image, ImageEnhance, ImageFilter
        
        print("\n" + "="*60)
        print("Using Tesseract OCR (with preprocessing)")
        print("="*60)
        
        print(f"Processing: {image_path}")
        
        # Load and preprocess image
        img = Image.open(image_path)
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        # Sharpen
        img = img.filter(ImageFilter.SHARPEN)
        
        # Extract text with different PSM modes
        configs = [
            '--psm 6',  # Assume uniform block of text
            '--psm 3',  # Fully automatic page segmentation
            '--psm 11', # Sparse text
            '--psm 12', # Sparse text with OSD
        ]
        
        best_text = ""
        best_config = ""
        
        for config in configs:
            try:
                text = pytesseract.image_to_string(img, config=config)
                if len(text.strip()) > len(best_text.strip()):
                    best_text = text
                    best_config = config
            except:
                continue
        
        if best_text.strip():
            print(f"✓ Best result with config: {best_config}")
            print(f"✓ Characters extracted: {len(best_text)}")
            print(f"✓ Preview:\n{best_text[:300]}...")
            return best_text
        else:
            print("✗ No text detected")
            return None
            
    except ImportError:
        print("✗ Tesseract not installed. Install with: pip install pytesseract")
        return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

def extract_with_rapidocr_direct(image_path):
    """
    RapidOCR Direct - Bypass Docling wrapper
    Sometimes more effective than the Docling integration
    """
    try:
        from rapidocr_onnxruntime import RapidOCR
        
        print("\n" + "="*60)
        print("Using RapidOCR (Direct Mode)")
        print("="*60)
        
        print(f"Processing: {image_path}")
        
        # Check if models exist
        det_model = "models/RapidOcr/onnx/PP-OCRv4/det/ch_PP-OCRv4_det_infer.onnx"
        rec_model = "models/RapidOcr/onnx/PP-OCRv4/rec/ch_PP-OCRv4_rec_infer.onnx"
        cls_model = "models/RapidOcr/onnx/PP-OCRv4/cls/ch_ppocr_mobile_v2.0_cls_infer.onnx"
        
        if not all(os.path.exists(m) for m in [det_model, rec_model, cls_model]):
            print("✗ RapidOCR models not found in expected location")
            return None
        
        # Initialize engine
        engine = RapidOCR(
            det_model_path=det_model,
            rec_model_path=rec_model,
            cls_model_path=cls_model
        )
        
        # Extract text
        result, elapse = engine(image_path)
        
        if result:
            print(f"✓ Detected {len(result)} text regions:\n")
            
            extracted_lines = []
            for idx, line in enumerate(result, 1):
                bbox, text, confidence = line
                # Convert confidence to float if it's a string, handle percentage formatting
                try:
                    conf_value = float(confidence)
                    print(f"  {idx}. [{conf_value:.2%}] {text}")
                except (ValueError, TypeError):
                    print(f"  {idx}. [{confidence}] {text}")
                extracted_lines.append(text)
            
            full_text = "\n".join(extracted_lines)
            print(f"\n✓ Total characters extracted: {len(full_text)}")
            return full_text
        else:
            print("✗ No text detected")
            return None
            
    except ImportError:
        print("✗ RapidOCR not installed. Install with: pip install rapidocr-onnxruntime")
        return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

def process_single_image(image_path, output_folder):
    """Process a single image and save results to output folder"""
    print(f"\n{'='*70}")
    print(f"Processing: {os.path.basename(image_path)}")
    print(f"{'='*70}")
    
    # Try each method and track all results (including failures)
    all_results = {}
    successful_results = {}
    
    # Method 1: EasyOCR (usually best for difficult images)
    text = extract_with_easyocr(image_path)
    if text:
        all_results['EasyOCR'] = text
        successful_results['EasyOCR'] = text
    else:
        all_results['EasyOCR'] = None
    
    # Method 2: Tesseract with preprocessing
    text = extract_with_tesseract(image_path)
    if text:
        all_results['Tesseract'] = text
        successful_results['Tesseract'] = text
    else:
        all_results['Tesseract'] = None
    
    # Method 3: RapidOCR Direct
    text = extract_with_rapidocr_direct(image_path)
    if text:
        all_results['RapidOCR_Direct'] = text
        successful_results['RapidOCR_Direct'] = text
    else:
        all_results['RapidOCR_Direct'] = None
    
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Always save comparison file with all methods
    comparison_file = os.path.join(output_folder, f"{base_name}_all_methods_comparison.txt")
    with open(comparison_file, "w", encoding="utf-8") as f:
        f.write(f"IMAGE: {os.path.basename(image_path)}\n")
        f.write(f"{'='*70}\n\n")
        
        for method, text in all_results.items():
            f.write(f"\n{'='*70}\n")
            f.write(f"METHOD: {method}\n")
            f.write(f"{'='*70}\n\n")
            
            if text:
                f.write(f"Status: SUCCESS - Extracted {len(text)} characters\n\n")
                f.write(text)
            else:
                f.write("Status: FAILED - No text extracted\n\n")
                f.write("# No text was detected by this OCR method.\n")
                f.write("# Possible reasons:\n")
                f.write("#   - Image quality too low\n")
                f.write("#   - Text too small or unclear\n")
                f.write("#   - Poor contrast between text and background\n")
                f.write("#   - Image contains no readable text\n")
                f.write("#   - OCR engine not properly configured\n")
            
            f.write(f"\n\n")
    
    print(f"✓ Comparison saved to: {os.path.basename(comparison_file)}")
    
    # Save best result if any method succeeded
    if successful_results:
        # Find best result (longest text)
        best_method, best_text = max(successful_results.items(), key=lambda x: len(x[1]))
        
        print(f"\n✓ {len(successful_results)} method(s) extracted text")
        print(f"🏆 Best: {best_method} ({len(best_text)} characters)")
        
        # Save best result
        output_file = os.path.join(output_folder, f"{base_name}_fixed_ocr_output.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"OCR Method: {best_method}\n")
            f.write("="*70 + "\n\n")
            f.write(best_text)
        print(f"✓ Best result saved to: {os.path.basename(output_file)}")
        
        return True
    else:
        print("\n✗ No methods successfully extracted text")
        return False

def main():
    print("\n" + "="*70)
    print("BATCH OCR EXTRACTION - Multi-Engine Approach")
    print("="*70)
    print("\nThis script processes all images in a folder using multiple")
    print("OCR engines to extract text.\n")
    
    # Get folder path
    folder_path = input("Enter folder name containing images (e.g., Images): ").strip()
    
    if not os.path.exists(folder_path):
        print(f"\n✗ Error: Folder '{folder_path}' not found!")
        print(f"Current directory: {os.getcwd()}")
        return
    
    if not os.path.isdir(folder_path):
        print(f"\n✗ Error: '{folder_path}' is not a directory!")
        return
    
    print(f"\n✓ Found folder: {folder_path}")
    
    # Get all image files
    image_extensions = {'.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.gif'}
    image_files = []
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            if ext in image_extensions:
                image_files.append(file_path)
    
    if not image_files:
        print(f"\n✗ No image files found in '{folder_path}'")
        print(f"Supported formats: {', '.join(image_extensions)}")
        return
    
    print(f"\n✓ Found {len(image_files)} image(s) to process")
    print("\nImages found:")
    for img in image_files:
        print(f"  • {os.path.basename(img)}")
    
    # Process all images
    print(f"\n{'='*70}")
    print("STARTING BATCH PROCESSING")
    print(f"{'='*70}")
    
    successful = 0
    failed = 0
    
    for image_path in image_files:
        if process_single_image(image_path, folder_path):
            successful += 1
        else:
            failed += 1
    
    # Final summary
    print("\n" + "="*70)
    print("BATCH PROCESSING COMPLETE")
    print("="*70)
    print(f"\n✓ Successfully processed: {successful}/{len(image_files)} images")
    if failed > 0:
        print(f"✗ Failed to extract text: {failed}/{len(image_files)} images")
    print(f"\n✓ All output files saved to: {folder_path}/")
    
    if failed > 0:
        print("\nTroubleshooting suggestions for failed images:")
        print("  1. Check image quality - is the text clear and readable?")
        print("  2. Try increasing image resolution/size")
        print("  3. Ensure good contrast between text and background")
        print("  4. Check if the image actually contains text")
        print("  5. Try converting the image to a different format (PNG, JPG)")
        print("\nInstall missing OCR engines:")
        print("  pip install easyocr")
        print("  pip install pytesseract")
        print("  pip install rapidocr-onnxruntime")

if __name__ == "__main__":
    main()

# Made with Bob
