from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.document import DocumentChunk
from app.rag.embeddings import embeddings

async def similarity_search(db:AsyncSession,query:str,user_id:int,top_k:int=10,document_id:int| None=None):
    query_vector=await embeddings.aembed_query(query)
    conditions=[DocumentChunk.document.has(user_id=user_id)]
    if document_id is not None:
        conditions.append(DocumentChunk.document_id ==document_id)

    
    distance=(DocumentChunk.embedding.cosine_distance(query_vector))
    statement=(
        select(DocumentChunk,distance.label("distance")).join(DocumentChunk.document).where(*conditions).order_by(distance).limit(top_k)
    )

    result=await db.execute(statement)
    return result.all()