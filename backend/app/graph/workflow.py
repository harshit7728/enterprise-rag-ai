from langgraph.graph import (
    END,START,StateGraph)
from app.graph.state import RAGState
from app.graph.nodes import (
    analyze_query,build_rag_context,generate_answer,rerank_documents,build_citations,fallback_node,cache_router,cache_node,check_cache_node,document_router)

from app.rag.langchain_retriever import (
    PostgresRetriever
)

def create_retriver_node(db):
    async def retrieve(state:RAGState)->dict:
        retriever=PostgresRetriever(
            db=db,user_id=state["user_id"],top_k=20
        )
        documents=await retriever.ainvoke(state["query"])

        return {
            "retrieved_documents":documents
        }
    return retrieve


def create_rag_graph(db):
    builder=StateGraph(RAGState)
    builder.add_node(
        "analyze_query",analyze_query
    )
    builder.add_node(
        "retrieve",create_retriver_node
    )
    builder.add_node(
        "rerank",rerank_documents

    )
    builder.add_node(
        "build_context",build_rag_context

    )

    builder.add_node(
        "generate",generate_answer
    )
    builder.add_node(
        "citations",build_citations
    )
    builder.add_node(
        "cache",cache_node
    )
    builder.add_node("check_cache",check_cache_node)
    builder.add_node("fallback",fallback_node)

    #edges
    builder.add_edge(START,"check_cache")
    builder.add_conditional_edges("check_cache",cache_router,{
        'cached':END,
        'miss':"analyze_query"
    })
    builder.add_edge("analyze_query","retrieve")

    builder.add_edge('retrieve','rerank')
    builder.add_conditional_edges(
        "rerank",document_router,{
            'no_documents':'fallback',
            'documents_found':'build_context'
        }
    )
    builder.add_edge('rerank','build_context')
    builder.add_edge('build_context','generate')
    builder.add_edge('generate','citation')
    builder.add_edge('citations','cache')
    builder.add_edge('cache',END)
    builder.add_edge('fallback',END)
    
    return builder.compile()

