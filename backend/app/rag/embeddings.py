from langchain_google_genai import GoogleGenerativeAIEmbeddings


from app.core.config import settings

embeddings=GoogleGenerativeAIEmbeddings(model="gemini-embedding-2",google_api_key=settings.google_api_key)