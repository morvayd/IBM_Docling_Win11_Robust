#  Win11 install and setup

#  Note:  (change from my file structure)
cd "C:\DataSci\PythonWorkArea\IBMDocling\IBMDoclingVenv"

#  Initial venv creation
python -m venv venv

#  Very specific to the venv created - verify before activating.
"venv\Scripts\activate.bat"

#  Install docling - defaults to RapidOCR
venv\Scripts\python.exe -m pip install docling

#  Download the docling models to use locally
#  Note:  (change from my file structure)
docling-tools models download --all -o "models"

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
venv\Scripts\python.exe
