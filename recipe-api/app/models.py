"""Database tables, written as Python classes (ORM models)."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instructions: Mapped[str] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    prep_time_minutes: Mapped[int] = mapped_column(Integer, default=0)
    cook_time_minutes: Mapped[int] = mapped_column(Integer, default=0)
    servings: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # One recipe has many ingredients.
    # cascade="all, delete-orphan" -> deleting a recipe also deletes its ingredients.
    ingredients: Mapped[List["Ingredient"]] = relationship(
        back_populates="recipe", cascade="all, delete-orphan"
    )


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(150))
    quantity: Mapped[str] = mapped_column(String(100))  # e.g. "2 cups", "1 tsp"

    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")
