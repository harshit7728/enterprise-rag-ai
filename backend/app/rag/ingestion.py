from langchain_core.documents import Document as LCDocument
from .chunking import split_document
from .loaders import load_pdf
from .embeddings import embeddings

async def ingest_pdf(file_path:str):
    documents=load_pdf(file_path)
    chunks=split_document(documents)
    texts=[chunk.page_content for chunk in chunks]
    vectors=await embeddings.aembed_documents(texts)
    result=[]
    for index,(chunk,vector) in enumerate(zip(chunks,vectors)):
        results.append({
            "chunk_index":index,
            "content":chunk.page_content,
            "embedding":vector,
            "metadata":chunk.metadata,
        })

    return result