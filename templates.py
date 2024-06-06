import os 
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]:%(message)s')
list_of_file=[
    "Data/",
    "Research/research.ipynb",
    "src/__init__.py",
    "src/logger/__init__.py",
    "src/logger/logger.py",
    "src/exception/__init__.py",
    "src/exception/exception.py",
    "src/utils/__init__.py",
    "src/utils/utils.py",
    "static/css/style.css",
    "static/images/",
    "static/js/home.js",
    "templates/Home.html",
    "templates/About.html",
    "templates/Contact.html",
    "templates/Publications.html",
    "templates/index.html",
    "setup.py", 
    "app.py",
    ".gitignore",
    ".env",
    "README.md",
    "requirements.txt",
]

for files in list_of_file:
    file_path=Path(files)

    file_dir,file_name=os.path.split(files)

    if file_dir!="":
        os.makedirs(file_dir,exist_ok=True)
        logging.info(f"Creating file directory:{file_dir} for the file :{file_name}")

    if (not os.path.exists(file_path)) or(os.path.getsize(file_path)==0):
        with open(file_path,'w') as f:
            pass
            logging.info(f"Creating empty file:{file_path}")
    else:
        logging.info(f"{file_name} is already created")