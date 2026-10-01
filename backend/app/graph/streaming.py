from app.llm.provider import llm 
from app.rag.prompt import rag_prompt

async def stream_answer(question:str,context:str):
    message=rag_prompt.formate_message(
        context=context,question=question
    )

    async for chunk in llm.astream(message):
        if chunk.content:
            yield chunk.content