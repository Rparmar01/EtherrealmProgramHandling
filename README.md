# Etherrealm Program Handler 
This repo will take user input from Unreal Engine as a .text file, generate a 3D mesh file from the input, convert the mesh file (usually a .ply extension) to a baked .fbx object file using Blender, and finally copy the object file to a directory within Unreal Engine for use.

## Meshfile Folder
This is the folder where .ply or other mesh files generated by AI Models will be stored. If you just want to convert all the files in Meshfiles to obj files, Call "python ply_to_fbx.py". If the conversion is successful, you should see the output "". 

# Fine tuning

## Vertex Color mapping 
This is adding colors and textures to the obj model, since Shap-e by default gives you a colorless .obj file 
