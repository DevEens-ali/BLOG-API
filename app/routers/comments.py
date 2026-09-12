from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Comment
from app.schemas import CommentCreate, CommentResponse


router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)



# CREATE COMMENT


@router.post("/", response_model=CommentResponse)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    new_comment = Comment(
        content=comment.content,
        author_id=comment.author_id,
        post_id=comment.post_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment



# GET ALL COMMENTS


@router.get("/", response_model=list[CommentResponse])
def get_all_comments(
    db: Session = Depends(get_db)
):
    comments = db.query(Comment).all()

    return comments



# GET COMMENT BY ID


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment_by_id(
    comment_id: int,
    db: Session = Depends(get_db)
):
    comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return comment



# UPDATE COMMENT


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    existing_comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not existing_comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    existing_comment.content = comment.content
    existing_comment.author_id = comment.author_id
    existing_comment.post_id = comment.post_id

    db.commit()
    db.refresh(existing_comment)

    return existing_comment



# DELETE COMMENT


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    existing_comment = db.query(Comment).filter(
        Comment.id == comment_id
    ).first()

    if not existing_comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    db.delete(existing_comment)
    db.commit()

    return {
        "message": "Comment deleted successfully"
    }