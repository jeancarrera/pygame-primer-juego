# import sys
# import os

# from cx_Freeze import setup, Executable

# documentos = ['assets']

# exe = Executable(script='player.py', base= 'Win32GUI')

# setup(
#     name= "Arcade game",
#     version= "1.0.1",
#     description= "Game created in order to learn the pygame library",  
#     author= "Jeancarrera",
#     options= {'build_exe':{'include_files':documentos}},
#     executables= [exe]
#     )

import sys
import os
from cx_Freeze import setup, Executable

documentos = ['assets']

exe = Executable(script='player.py', base= 'Win32GUI')

setup(
    name = "Arcade game",
    version ="1.0",
    description = "Game created in order to learn the pygame library",
    author = "Straight Coding",
    options = {'build_exe': {'include_files': documentos}},
    executables = [exe]
    

)

