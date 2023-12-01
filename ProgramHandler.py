import os 
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# PREREQUISITE: nbconvert must be installed and all prerequisites of shap-e notebook must be installed before running.



# Specify the path to your Jupyter Notebook file
notebook_path = f''

# Read the notebook
with open(notebook_path) as f:
    notebook = nbformat.read(f, as_version=4)

# Create an ExecutePreprocessor. The timeout=-1 means no timeout for cell execution, but this can be adjusted
execute_processor = ExecutePreprocessor(timeout=-1)

# Execute the notebook
execute_processor.preprocess(notebook, {'metadata': {'path': '.'}})

# Save modified notebooks (Will preserve updated output within notebook)
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbformat.write(notebook, f)


# Run ply to fbx conversion script to bake ply mesh to fbx object file
os.system("python ply_to_fbx.py")

#Export fbx object to engine (Unreal Engine in this case)

