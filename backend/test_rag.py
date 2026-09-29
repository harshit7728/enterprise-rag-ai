import asyncio
from app.db.database import AsyncSessionLocal
from app.rag.langchain_retriever import  (
    PostgresRetriever
)

from app.rag.chain import generate_answer

async def main():
    question="What is the refund policy"

    async with AsyncSessionLocal() as db:
        retriever=PostgresRetriever(db=db,user_id=1,top_k=5)
        documents=await retriever.ainvoke(question)
        answer=await generate_answer(question=question,documents=documents)
        print("\n Answer \n")
        print(answer)


    
if __name__=='__main__':
    asyncio.run(main())