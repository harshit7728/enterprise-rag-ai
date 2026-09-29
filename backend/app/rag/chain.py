from app.llm.provider import llm 
from .context import build_context
from .prompt import rag_prompt


async def  generate_answer(
        question:str,
        documents

):
    context=build_context(documents)
    message=rag_prompt.format_messages(
        context=context,question=question
    )
    response=await llm.ainvoke(message)

    return response.content