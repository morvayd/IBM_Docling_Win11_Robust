#  Win11 install and setup

#  Note:  (change from my file structure)
cd %userprofile%\PythonVenv\IBMDocling

#  ---- Only 1st Time Creation ----
    #  Initial venv creation - will overwrite any venv created
    python -m venv venv

#  Very specific to the venv created - verify before activating.
venv\Scripts\activate.bat

#  Must utilize the requirements.txt file!
venv\Scripts\python -m pip install -r requirements.txt

#  Upgrade pip
venv\Scripts\python -m pip install --upgrade pip

#  ---- or ----
    #  Install docling - defaults to RapidOCR - Use GPU
    venv\Scripts\python -m pip install docling

    #  ---------- If needed ----------
    
    # Install EasyOCR (best for difficult images)
    venv\Scripts\python -m pip install easyocr

    # Install Tesseract wrapper
    venv\Scripts\python -m pip install pytesseract

    # Install RapidOCR direct
    venv\Scripts\python -m pip install rapidocr-onnxruntime

    # Install image processing
    venv\Scripts\python -m pip install pillow


#  Xcheck Verify Installed - may take time to complete
docling --version

#  Download the docling models to use locally - download new at new installation
#  Note:  (change from my file structure)
docling-tools models download --all -o "./models"
#  Using the CLI: `docling --artifacts-path=models FILE` 
#  Note:  May need to download the following model specifically
#  Folder:  models--sentence-transformers--all-MiniLM-L6-v2

#
#  ---------- Optional ----------
#
#  Set environment variable for local model use
#  Linux:
#  export DOCLING_ARTIFACTS_PATH=</path/to/models>

#  Windows:
#  set DOCLING_ARTIFACTS_PATH=<C:\path\to\models>"

#
#  ---------- Running Python ----------
#
venv\Scripts\python
