from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post
from app.schemas import PostCreate, PostResponse, PostUpdate


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


@router.get("/", response_model=list[PostResponse])
def get_all_posts(
    db: Session = Depends(get_db)
):
    posts = db.query(Post).all()

    return posts



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