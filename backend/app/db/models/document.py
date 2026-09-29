from datetime import datetime
from sqlalchemy import (
    DateTime,ForeignKey,Integer,JSON,Text,String,
)

from sqlalchemy.orm import Mapped,mapped_column,relationship

from pgvector.sqlalchemy import Vector

from app.db.base import Base

class Document(Base):
    __tablename__="documents"

    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    title:Mapped[str]=mapped_column(String(225),nullable=False)
    file_name:Mapped[str]=mapped_column(String(225),nullable=False)
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=datetime.utcnow,nullable=False)
    chunks:Mapped[list["DocumentChunk"]]=relationship(back_populates="document",cascade="all,delete-orphan")



class DocumentChunk(Base):
    __tablename__="document_chunks"
    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    document_id:Mapped[int]=mapped_column(ForeignKey("documents.id",ondelete="CASCADE"),nullable=False,index=True)
    chunk_index:Mapped[int]=mapped_column(Integer,nullable=False)
    content:Mapped[str]=mapped_column(Text,nullable=False)
    page_number:Mapped[int|None]=mapped_column(Integer,nullable=True)
    metadata:Mapped[dict]=mapped_column(JSON,default=dict)
    embedding:Mapped[list[float]]=mapped_column(Vector(3072),nullable=False)
    document:Mapped["Document"]=relationship(back_populates="chunks")
