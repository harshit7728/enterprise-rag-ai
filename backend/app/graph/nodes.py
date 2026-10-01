from app.graph.state import RAGState
from app.rag.langchain_retriever import (
    PostgresRetriever
)
from app.llm.provider import llm
from app.rag.prompt import rag_prompt
from app.rag.context import build_context
from app.rag.reranker import Reranker
from app.cache.cache import get_cached_answer

reranker=Reranker()

async def analyze_query(state:RAGState)->dict:
    query=state["query"].strip()
    if not query:
        return {
            "error":"Query cannot be emmpty"
        }
    
    return {
        "query":query
    }



async def retrieve_document(state:RAGState,db)->dict:
    retriever=PostgresRetriever(db=db,user_id=state['user_id'],top_k=20)

    documents=await retriever.ainvoke(state["query"])
    return {
        "retriveddocumemts"
    }






async def build_rag_context(state:RAGState)->dict:
    context=build_context(state["reranked_documents"])
    return {
        "context":context
    }


async def generate_answer(state:RAGState)->dict:
    messages=rag_prompt.formate_messages(
        context=state["context"],question=state["query"]
    )

    response=await llm.ainvoke(messages)
    return {
        "answer":response.content
    }


async def build_citations(
        state:RAGState
):
    citations=[]
    for document in state['reranked_documents']:
        metadata=document.metadata

        citations.append({
            "document_id":metadata.get("document_id"),
            "page_number":metadata.get("page_number"),
            "chunk_id":metadata.get("chunk_id")
        })

    return {
        "citations"
    }



async def rerank_documents(state:RAGState)->dict:
    documents=state(
        "retrieved_documents"
    )
    rank_documents=reranker.rerank(query=state["query"],documents=documents,top_k=5)

    return {
        "reranked_documents":rank_documents
    }



async def check_cache_node(state:RAGState)->dict:
    cached=await get_cached_answer(
        user_id=state["user_id"],
        query=state["query"],
        document_id=state.get("document_id")
    )

    if cached is None:
        return {
            "cached":False
        }
    return {
        "cached":True,
        "answer":cached['anser'],
        "citations":cached['citations']
    }


def cache_router(state:RAGState)->str:
    if state.get("cached"):
        return "cached"
    return "miss"


def document_router(state:RAGState)->str:
    documents=state.get("reranked_documents",[])
    if not documents:
        return "no_documents"
    
    return "documents_found"


async def fallback_node(state:RAGState)->dict:
    return {
        "answer":(
            "I could not find relevent information ",
            "in the documents available to you"
        ),
        "citations":[]
    }



async def cache_node(state:RAGState)->dict:
    await cache_node(user_id=state["user_id"],query=state['query'],answer=state['answer'])
    return {}
