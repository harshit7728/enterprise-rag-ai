import json
from .redis import redis_client
import hashlib

CACHE_TTL=60*10


def normalize_query(query:str)->str:
    return " ".join(query.lower().strip().split())
def build_cache_key(
        user_id:int,query:str,document_id:int|None=None
):
    normalized_query=normalize_query(query)
    query_hash=hashlib.sha256(
        normalized_query.encode("utf-8")
    ).hexdigest()

    document_scope=document_id or "all"


    return {
        f"rag:answer:"
        f"user:{user_id}"
        f"doc:{document_scope}"
        f"q:{query_hash}"
    }


async def get_cached_answer(user_id:int,query:str,document_id:int|None=None):
    key=build_cache_key(user_id=user_id,query=query,document_id=document_id)
    cached=await redis_client.get(key)
    if not cached:
        return None
    
    return json.load(cached)


async def cache_answer(user_id:int,query:str,answer:str,citations:list,document_id:int|None=None):
    key=build_cache_key(user_id=user_id,query=query,document_id=document_id)
    payload={
        "answer":answer,
        "citations":citations
    }

    await redis_client.set(
        key,json.dumps(payload),ex=CACHE_TTL
    )
