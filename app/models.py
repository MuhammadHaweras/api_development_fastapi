from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.sql import expression
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default=expression.true())
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('now()'))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False,
                        server_default=text('now()'))