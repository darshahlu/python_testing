# Getting started

## Clone the repository
```
git clone https://github.com/darshahlu/python_testing.git
cd python_testing
```

## Create Environment and Install Dependencies (venv method)
```
c:\Python36\python.exe -m venv c:\dev\venvs\python-testing-win
c:\dev\venvs\python-testing-win\Scripts\activate.bat
pip install -r requirements-py363-win.txt
```

## Launch the Jupyter Notebook
```
cd jupyter_presentation
jupyter notebook
```

## Run the example pytests from command line
From the root repo directory:
```
pytest
```

## Run the example pytests from an IDE
Make sure coverage is disabled (see pytest.ini and --no-cov option), as coverage breaks debuggers.
