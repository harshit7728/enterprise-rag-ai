from typing import List
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun, AsyncCallbackManagerForRetrieverRun
from pydantic import ConfigDict, Field

from .retriever import similarity_search
from .document_mapper import to_langchain_documents

class PostgresRetriever(BaseRetriever):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: object = Field(exclude=True)
    user_id: int
    top_k: int = 10
    document_id: int | None = None

    # 1. Mandatory Sync Implementation (Raises error if someone calls it synchronously)
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        raise NotImplementedError("PostgresRetriever only supports asynchronous operations via ainvoke().")

    # 2. Corrected Async Implementation
    async def _aget_relevant_documents(
        self, query: str, *, run_manager: AsyncCallbackManagerForRetrieverRun
    ) -> List[Document]:
        rows = await similarity_search(
            db=self.db,
            query=query,
            user_id=self.user_id,
            top_k=self.top_k,
            document_id=self.document_id
        )
        return to_langchain_documents(rows)
