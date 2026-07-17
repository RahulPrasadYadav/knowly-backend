from typing import Optional

from pydantic import BaseModel


class CategoryRead(BaseModel):
    """API representation of a category.

    Database tables belong in ``app.models``.  Keeping this as a Pydantic
    schema prevents it from being included in Alembic's metadata.
    """

    id: int
    name: Optional[str] = None

    model_config = {"from_attributes": True}
