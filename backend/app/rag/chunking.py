from langchain_text_splitters import RecursiveCharacterTextSplitter 


splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=150)



def split_document(documents):
    return splitter.split_documents(documents)
