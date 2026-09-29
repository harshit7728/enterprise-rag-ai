import asyncio
from app.llm.provider import llm
async def main():
    response=await llm.ainvoke("explain  RAG in two sentences")
    print(response.content)



if __name__=="__main__":

    asyncio.run(main())
