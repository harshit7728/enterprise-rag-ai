from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.document import DocumentChunk

async def save_chunks(db:AsyncSession,document_id:int,chunks:list[dict],):
    for chunk in chunks:
        db_chunk=DocumentChunk(document_id=document_id,chunk_index=chunk['chunk_index'],content=chunk["content"],page_number=chunk['metadata'].get("page"),metadata=chunk["metadata"],embeddings=chunk["embedding"])

        db.commit(db_chunk)
    await db.commit()