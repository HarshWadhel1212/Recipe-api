"""Pydantic schemas: they define and validate the data going IN and OUT of the API."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class IngredientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150, examples=["Flour"])
    quantity: str = Field(min_length=1, max_length=100, examples=["2 cups"])


class IngredientOut(IngredientCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RecipeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200, examples=["Pancakes"])
    description: Optional[str] = None
    instructions: str = Field(min_length=1)
    category: Optional[str] = Field(default=None, max_length=100, examples=["Breakfast"])
    prep_time_minutes: int = Field(default=0, ge=0)
    cook_time_minutes: int = Field(default=0, ge=0)
    servings: int = Field(default=1, ge=1)
    ingredients: List[IngredientCreate] = []


class RecipeUpdate(BaseModel):
    """Every field is optional, so the client can send only what it wants to change."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    instructions: Optional[str] = Field(default=None, min_length=1)
    category: Optional[str] = Field(default=None, max_length=100)
    prep_time_minutes: Optional[int] = Field(default=None, ge=0)
    cook_time_minutes: Optional[int] = Field(default=None, ge=0)
    servings: Optional[int] = Field(default=None, ge=1)
    ingredients: Optional[List[IngredientCreate]] = None


class RecipeOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    instructions: str
    category: Optional[str]
    prep_time_minutes: int
    cook_time_minutes: int
    servings: int
    created_at: datetime
    updated_at: datetime
    ingredients: List[IngredientOut]

    model_config = ConfigDict(from_attributes=True)
