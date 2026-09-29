from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader
)

def load_pdf(file_path:str):
    path=Path(file_path)
    if path.suffix.lower()!=".pdf":
        raise ValueError("only pdf files are supported currently")
    
    loader=PyPDFLoader(str(path))

    return loader.load()