import os 
import time 
import signal


# PREREQUISITE: nbconvert must be installed and all prerequisites of shap-e notebook must be installed before running.

def signal_handler(signum, frame):
    # Handle the signal here (e.g., read the variable and execute code)
    print(f"Received signal {signum}. Executing ProgramHandler.py logic.")
    # Add your code to execute in response to the signal
     # print(f"Text content received: {scriptPromptFileWatcher.readText}")


def runJob(promptInput):
    # Another way to access the prompt input 
    '''
    infile = open('sample_text_input.txt', 'r')
    promptString = str(infile.read())
    infile.close()
    print("Prompt string is", promptString)
    '''
    # Call the Shap-e Model with promptInput as the prompt
    

    # Run ply to fbx conversion script to bake ply mesh to fbx object file
    # os.system("python ply_to_fbx.py")

    #Export fbx object to engine (Unreal Engine in this case)




