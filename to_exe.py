import os, subprocess, sys

def build(
    file,
    oneFile: bool = True,
    based: bool = True,
    icon: str = None,
    output: str = os.path.join(os.getcwd(), "build"),
    ) :

    
    if not os.path.exists(output):
        os.mkdir(output)
        
    args = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        ("--onedir", "--onefile")[oneFile],
        ("--console", "--windowed")[based],
        (*(f"--icon", icon), None)[icon is None],
        
        "--add-data", 
        f"{os.getcwd()}\\ezsgame;ezsgame", # Folder
        
        "--add-data",
        f"{os.getcwd()}\\ezsgame\\assets;icon.jpg", # File
        
        
        f"{os.getcwd()}\\{file}", # File
        
    ]
    
    # Clear a None value in args
    args = [x for x in args if x is not None]
    subprocess.run(args, cwd=output)
    

build("demo.py")