import asyncio 
from app.db.database import AsyncSessionLocal
from app.rag.langchain_retriever import (
    PostgresRetriever
)

async def main():
    async with AsyncSessionLocal() as db:
        retriver=PostgresRetriever(db=db,user_id=1,top_k=5)
        documents=await retriver.ainvoke("What is the refund policy")
        for doc in documents:
            print("="*80)
            print(doc.page_content)
            print(doc.metadata)





if __name__=="__main__":
    asyncio.run(main())
