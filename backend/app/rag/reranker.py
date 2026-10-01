from sentence_transformers import CrossEncoder

class Reranker:
    def __inti__(self):
        self.model=CrossEncoder("BAAI/bge-reranker-base")
    
    def rerank(self,query:str,documents,top_k:int=5):
        pairs=[
            (
                query,document.page_content,
            )
             for document in documents
        ]

        scores=self.model.predict(pairs)
        ranked=sorted(zip(documents,scores),key=lambda item:item[1],reverse=True)
        results=[]
        for document,score in ranked[:top_k]:
            document.metadata["rerank_score"]=float(score)

        return results


