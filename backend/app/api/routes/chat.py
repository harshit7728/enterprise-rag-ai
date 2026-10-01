from fastapi import (
    APIRouter,Depends
)

from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import decode_access_token
from app.graph.workflow import create_rag_graph
from app.graph.streaming import stream_answer



router=APIRouter(prefix="/chat",tags=["Chat"])

async def chat_stream(request:dict,db:AsyncSession=Depends(get_db),user_id:int=Depends(decode_access_token)):
    query=request["query"]
    graph=create_rag_graph(db)

    state=await graph.ainvole({
        "query":query,
        "user_id":user_id,
        "retrived_documents":[],
        "reranked_documents":[],
        "context":"",
        "answer":"",
        "citations":[],
        "error":None
    })


    async def generator():
        async for token in stream_answer(question=query,context=state["context"]):
            yield token
    return StreamingResponse(
        generator(),media_type="text/plain"
    )


    