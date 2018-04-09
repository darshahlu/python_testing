# Launching jupyter
1. Clone the repository and navigate to the python_testing directory.
2. The requirements are:
```
pip install jupyter
pip install pytest
pip install pytest-cov
pip install pytest-django
pip install ipytest
pip install git+https://github.com/akaihola/ipython_pytest
```
3. ```cd jupyter_presentation```
4. Currently the notebook is configured to be available at http://localhost/tree?token=LittleMonkey! See jupyter_notebook_config.py.:
    1. c.NotebookApp.ip = 'localhost'
    2. c.NotebookApp.token = 'LittleMonkey!'
5. Launch the server by running this command: ```jupyter notebook```
