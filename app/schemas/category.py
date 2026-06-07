from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    pattern: str | None = None


class CategoryRead(BaseModel):
    category_id: int
    name: str
    pattern: str | None
    user_id: int

    model_config = {"from_attributes": True}


class CategoryUpdate(BaseModel):
    name: str | None = None
    pattern: str | None = None


class CategoryBulkItem(BaseModel):
    category_id: int | None = None
    name: str
    pattern: str | None = None


class CategoryBulkRequest(BaseModel):
    categories: list[CategoryBulkItem]
