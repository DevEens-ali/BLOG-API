from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from app.rate_limiter import rate_limit

from app.database import get_db
from app.models import Post
from app.schemas import PostCreate, PostResponse, PostUpdate
import math


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



# CREATE POST


@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db)
):
    new_post = Post(
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        category_id=post.category_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



# GET ALL POSTS


# @router.get("/", response_model=list[PostResponse])
# def get_all_posts(
#     db: Session = Depends(get_db)
# ):
#     posts = db.query(Post).all()

#     return posts

# @router.get("/")
# def get_all_post(
#     page:int = Query(1,ge =1),
#     limit :int = Query(10,ge=1),
#     db:Session = Depends(get_db)
# ):
#     offset = (page-1)*limit
#     posts = db.query(Post).offset(offset).limit(limit).all()
#     return{
#         "page": page,
#         "limit": limit,
#         "items": posts
#     }

@router.get("/")
def get_all_posts(
    request: Request,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    author_id: int | None = Query(None),
    category_id: int | None = Query(None),
    search: str | None = Query(None),
    sort: str = Query("created_at"),
    order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    client_ip = request.client.host
    rate_limit(client_ip)

    query = db.query(Post)

    if author_id is not None:
        query = query.filter(Post.author_id == author_id)

    if category_id is not None:
        query = query.filter(Post.category_id == category_id)

    if search is not None:
        query = query.filter(
            (Post.title.ilike(f"%{search}%")) |
            (Post.content.ilike(f"%{search}%"))
        )

    sort_fields = {
        "title": Post.title,
        "created_at": Post.created_at,
        "updated_at": Post.updated_at
    }

    if sort not in sort_fields:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    if order == "asc":
        query = query.order_by(sort_fields[sort].asc())

    elif order == "desc":
        query = query.order_by(sort_fields[sort].desc())

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort order"
        )

    offset = (page - 1) * limit

    total = query.count()

    posts = query.offset(offset).limit(limit).all()

    pages = math.ceil(total / limit)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
        "items": posts
    }

   
    
    

    






# GET POST BY ID


@router.get("/{post_id}", response_model=PostResponse)
def get_post_by_id(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


# UPDATE POST


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db)
):
    existing_post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not existing_post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.category_id = post.category_id

    db.commit()
    db.refresh(existing_post)

    return existing_post


# DELETE POST


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    existing_post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not existing_post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    db.delete(existing_post)
    db.commit()

    return {
        "message": "Post deleted successfully"
    }