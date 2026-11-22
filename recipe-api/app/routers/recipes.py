"""API endpoints (routes) for recipes."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/recipes", tags=["Recipes"])


def get_recipe_or_404(recipe_id: int, db: Session = Depends(get_db)):
    """Shared helper: find the recipe or return a clear 404 error."""
    recipe = crud.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe


@router.post("", response_model=schemas.RecipeOut, status_code=status.HTTP_201_CREATED)
def create_recipe(data: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, data)


@router.get("", response_model=List[schemas.RecipeOut])
def list_recipes(
    skip: int = Query(0, ge=0, description="How many recipes to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max recipes to return"),
    search: Optional[str] = Query(None, description="Search in the title"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db),
):
    return crud.list_recipes(db, skip, limit, search, category)


@router.get("/{recipe_id}", response_model=schemas.RecipeOut)
def read_recipe(recipe=Depends(get_recipe_or_404)):
    return recipe


@router.put("/{recipe_id}", response_model=schemas.RecipeOut)
def update_recipe(
    data: schemas.RecipeUpdate,
    recipe=Depends(get_recipe_or_404),
    db: Session = Depends(get_db),
):
    return crud.update_recipe(db, recipe, data)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe=Depends(get_recipe_or_404), db: Session = Depends(get_db)):
    crud.delete_recipe(db, recipe)
