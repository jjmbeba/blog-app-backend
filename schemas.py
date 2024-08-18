from __future__ import annotations
import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    posts: list[Post]

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    description: str | None = None
    content: str


class PostCreate(PostBase):
    pass


class FavoriteBase(BaseModel):
    user_id: int
    post_id: int


class FavoriteCreate(FavoriteBase):
    pass


class Favorite(FavoriteBase):
    id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    user_id: int
    post_id: int


class Comment(CommentBase):
    id: int
    user_id: int
    post_id: int

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class PostWithAttributes(Post):
    author: User
    tags: list[Tag] = []
    favorites: list[Favorite] = []


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserWithAttributes(User):
    posts: list[Post] = []
    favorites: list[Favorite] = []
    comments: list[Comment] = []
