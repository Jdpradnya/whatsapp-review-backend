from pydantic import BaseModel
from datetime import datetime

class ReviewBase(BaseModel):
    contact_number: str
    user_name: str
    product_name: str
    product_review: str

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
