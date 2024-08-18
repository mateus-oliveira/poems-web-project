from sqlalchemy import Column, Integer, String, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)

    poems = relationship("Poem", back_populates="author")
    comments = relationship("Comment", back_populates="author")


class Poem(Base):
    __tablename__ = "poems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="poems")
    likes = relationship("Like", back_populates="poem")
    comments = relationship("Comment", back_populates="poem")


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint('user_id', 'poem_id', name='unique_like'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    poem_id = Column(Integer, ForeignKey("poems.id"))

    poem = relationship("Poem", back_populates="likes")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    poem_id = Column(Integer, ForeignKey("poems.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    poem = relationship("Poem", back_populates="comments")
    author = relationship("User", back_populates="comments")
