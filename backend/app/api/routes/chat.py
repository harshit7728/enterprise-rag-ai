from fastapi import (
    APIRouter,Depends
)
from pydantic import BaseModel

from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import decode_access_token,get_current_user
from app.graph.workflow import create_rag_graph
from app.graph.streaming import stream_answer
from app.cache.rate_limit import check_rate_limit



router=APIRouter(prefix="/chat",tags=["Chat"])

# @router.post("/chat/stream")
# async def chat_stream(request:dict,db:AsyncSession=Depends(get_db),user_id:int=Depends(decode_access_token)):
#     await check_rate_limit(user_id)
#     query=request["query"]
#     graph=create_rag_graph(db)

#     state=await graph.ainvole({
#         "query":query,
#         "user_id":user_id,
#         "retrived_documents":[],
#         "reranked_documents":[],
#         "context":"",
#         "answer":"",
#         "citations":[],
#         "cached":False,
#         "error":None
#     })


#     async def generator():
#         async for token in stream_answer(question=query,context=state["context"]):
#             yield token
#     return StreamingResponse(
#         generator(),media_type="text/plain"
#     )



class ChatRequest(BaseModel):
    query:str
    document_id:int|None=None
    

async def chat_stream(
        request:ChatRequest,
        user_id:int=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    await check_rate_limit(user_id)
    graph=create_rag_graph(db)
    initial_state={
        "query":request.query,
        "user_id":user_id,
        "retrived_documents":[],
        "reranked_documents":[],
        "context":"",
        "answer":"",
        "citations":[],
        "cached":False,
        "error":None
    }

    async def event_generator():
        async for event in graph.astream_event(initial_state,version='v2'):

             if event['event']=="on_chat_model_stream":
                 chunk=event['data']['chunk']
                 if chunk.content:
                     yield chunk.content

    return StreamingResponse(
        event_generator,media_type="text/plain",
    )
    
