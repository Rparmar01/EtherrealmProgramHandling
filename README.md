NOTE: This is a private repo to replace Point-eAutomatedFlow for use as Point-e is deprecated in favor of Shap-e for Etherrealm.

# Etherrealm Program Handler 
This repo will take user input from Unreal Engine as a .text file, generate a 3D mesh file from the input, convert the mesh file (usually a .ply extension) to a baked .fbx object file using Blender, and finally copy the object file to a directory within Unreal Engine for use.

# How it Works 
Currently, ProgramHandler.py is supposed to run on game startup, observing whether SavedText.txt has changed. Once the text file is updated, the file calls ShapeModelCaller to run a job, which will then issue an HTTP request to the API that is hosting the text-to-3d model for a mesh file (and once implemented, necessary color/texture files). If correct mesh files are given as a response, then the game will import the meshfiles. Otherwise, if the response times out or if the meshfiles are corrupted/incorrect, the program will let the user know that either the request timed out or that the object file was corrupted. The user will need to define the API key in settings. 

## Meshfile Folder
*** For now, only one Generated Mesh will be allowed to load into the game at a time. In the future, I will add save slots to the meshfiles so the user can preload generated meshes into slots and call them as many times as they want in-game ***

This folder will be known as GeneratedMeshes locally in the game files within the Unreal Engine file directory. GeneratedMaterials is a separate folder that will store specific material textures.  
This is the folder where .ply or other mesh files generated by AI Models will be stored. If you just want to convert all the files in Meshfiles to obj files, Call "python ply_to_fbx.py". If the conversion is successful, you should see the output "". 

# Fine tuning

## Vertex Color mapping 
This is adding colors and textures to the obj model, since Shap-e by default gives you a colorless .obj file. Since there is a preset materials in Unreal Engine for all generated meshes for now, this will be implemented in the future to give more acurrate colors to generated objects
