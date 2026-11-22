"""CRUD = Create, Read, Update, Delete.

All database work lives here, so the routes stay short and clean.
"""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def create_recipe(db: Session, data: schemas.RecipeCreate) -> models.Recipe:
    values = data.model_dump(exclude={"ingredients"})
    recipe = models.Recipe(**values)
    recipe.ingredients = [models.Ingredient(**i.model_dump()) for i in data.ingredients]
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


def get_recipe(db: Session, recipe_id: int) -> Optional[models.Recipe]:
    return db.get(models.Recipe, recipe_id)


def list_recipes(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    category: Optional[str] = None,
) -> List[models.Recipe]:
    query = select(models.Recipe)
    if search:
        query = query.where(models.Recipe.title.ilike(f"%{search}%"))
    if category:
        query = query.where(models.Recipe.category.ilike(category))
    query = query.order_by(models.Recipe.id).offset(skip).limit(limit)
    return list(db.scalars(query).all())


def update_recipe(
    db: Session, recipe: models.Recipe, data: schemas.RecipeUpdate
) -> models.Recipe:
    changes = data.model_dump(exclude_unset=True)  # only fields the client sent
    new_ingredients = changes.pop("ingredients", None)

    for field, value in changes.items():
        setattr(recipe, field, value)

    if new_ingredients is not None:  # replace the full ingredient list
        recipe.ingredients = [models.Ingredient(**i) for i in new_ingredients]

    db.commit()
    db.refresh(recipe)
    return recipe


def delete_recipe(db: Session, recipe: models.Recipe) -> None:
    db.delete(recipe)
    db.commit()
