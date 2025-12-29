"""
Database models using SQLModel for product reviews.
"""
from datetime import datetime
from typing import Optional, Literal
from sqlmodel import SQLModel, Field

class Advertising(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tv: float
    radio: float
    newspaper: float
    prediction: float
    prediction_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    client_ip: str


class Iris(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sepallengthcm: float
    sepalwidthcm: float
    petallengthcm: float
    petalwidthcm: float
    prediction: str
    prediction_time: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    client_ip: str


class ProductReviewRate(SQLModel, table=True):
    __tablename__ = "products_review_rates"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_info: str = Field(description="User information or identifier")
    review: str = Field(description="The original review text")
    product: str = Field(description="Product name or identifier")
    rate: Optional[int] = Field(default=None, description="Rating 1-5")
    sentiment: Optional[str] = Field(default=None, description="Positive or negative sentiment")
    key_points: Optional[str] = Field(default=None, description="Key points as JSON string")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When the review was processed")


# Product Review Analysis
class ProductReview(SQLModel):
    """Analysis of a product review."""
    # Rating with validation constraints
    rating: int | None = Field(
        description="The rating of the product (1-5)",
        ge=1,  # minimum value = 1
        le=5  # maximum value = 5
    )
    # Sentiment with restricted values
    sentiment: Literal["positive", "negative"] = Field(
        description="The sentiment of the review"
    )
    # List of key points
    key_points: list[str] = Field(
        description="Key points from the review. Lowercase, 1-3 words each."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "rating": 5,
                "sentiment": "positive",
                "key_points": [
                    "great quality",
                    "fast delivery",
                    "easy to use"
                ]
            }
        }


class AnalyzedReview(SQLModel):
    user: str = Field(description="User information or identifier")
    product: str = Field(description="Product name or identifier")
    review: str = Field(description="The original review text")

    class Config:
        json_schema_extra = {
            "example": {
                "user": "john_doe",
                "product": "Wireless Headphones XYZ",
                "review": "Amazing product! 5 stars. Quick delivery and great quality, but quite pricey."
            }
        }


class RequestIris(SQLModel):
    sepallengthcm: float
    sepalwidthcm: float
    petallengthcm: float
    petalwidthcm: float

    class Config:
        json_schema_extra = {
            "example": {
                "sepallengthcm": 5.1,
                "sepalwidthcm": 3.5,
                "petallengthcm": 1.4,
                "petalwidthcm": 0.2,
            }
        }


class RequestAdvertising(SQLModel):
    tv: float
    radio: float
    newspaper: float

    class Config:
        json_schema_extra = {
            "example": {
                "tv": 230.1,
                "radio": 37.8,
                "newspaper": 69.2,
            }
        }
