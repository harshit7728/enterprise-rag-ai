from langchain_core.documents import Document

def build_context(documents:list[Document])->str:
    parts=[]

    for doc in documents:
        metadata=doc.metadata
        document_id=metadata.get('document_id')
        page=metadata.get("page_number")
        parts.append(f"""
            [Document ID:{document_id}]
            [Page: {page}]
            {doc.page_content}

          """)
    return "\n\n---\n\n".join(parts)
