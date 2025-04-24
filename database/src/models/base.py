"""Base model for MongoDB documents."""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class BaseDocument(BaseModel):
    """Base document model with common fields."""
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return self.model_dump(by_alias=True)

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        arbitrary_types_allowed = True
