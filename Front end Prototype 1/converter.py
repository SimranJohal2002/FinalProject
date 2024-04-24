from nbconvert import PythonExporter
import nbformat
import sys
import os


def ipynb_to_py(ipynb_file, py_file):
    with open(ipynb_file, 'r') as f:
        nb = nbformat.read(f, as_version=4)

    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(nb)

    with open(py_file, 'w') as f:
        f.write(source)


if not os.path.exists('./temp'): 
    os.makedirs('./temp')

#usage
ipynb_to_py(sys.argv[1], './temp/index.py')
