from langchain_core.documents import Document



def to_langchain_documents(rows):
    documents=[]
    for chunk ,distance in rows:
        metadata={
            **(chunk.metadata or {}),
            "chunk_id":chunk.id,
            "document_id":chunk.document_id,
            "page_number":chunk.page_number,
            "distance":float(distance)
        }

        documents.append(Document(page_content=chunk.content,metadata=metadata))
    return documents