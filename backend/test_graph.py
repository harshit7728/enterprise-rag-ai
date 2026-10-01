import asyncio 
from app.db.database import AsyncSessionLocal
from app.graph.workflow import create_rag_graph

async def main():
    async with AsyncSessionLocal() as db:
        graph=create_rag_graph(db)
        result=await graph.ainvoke({
            "query":"what is the refund policy",
            "user_id":1,
            "retrieved_documents":[],
            "reranked_documents":[],
            "context":"",
            "answer":"",
            "citations":[],
            "error":None
        })

        print("ANswr")
        print(result["answer"])
        print(result["citations"])
    
if __name__=="__main__":
    asyncio.run(main())