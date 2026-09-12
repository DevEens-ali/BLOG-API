from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session


from app.database import get_db
from app.models import Category
from app.schemas import CategoryCreate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    new_category = Category(
        name=category.name
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.get("/all_categories", response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    all_categories = db.query(Category).all()

    return all_categories

@router.put("/update_category/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    existing_category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not existing_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    existing_category.name = category.name

    db.commit()
    db.refresh(existing_category)

    return existing_category

@router.delete("/Delete_Category/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    existing_category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not existing_category:
        raise HTTPException(
            status_code=404,
            detail="Data Not Found"
        )

    db.delete(existing_category)
    db.commit()

    return {"message": "Category Deleted Successfully"}

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db)
):
    existing_category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not existing_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return existing_category

@router.delete("/delete_all_categories")
def delete_all_categories(
    db: Session = Depends(get_db)
):
    categories = db.query(Category).all()

    if not categories:
        raise HTTPException(
            status_code=404,
            detail="No categories found"
        )

    for category in categories:
        db.delete(category)

    db.commit()

    return {
        "message": "All categories deleted successfully"
    }