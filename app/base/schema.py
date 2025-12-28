from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field, model_serializer

DataT = TypeVar("DataT")


class BaseResponse(BaseModel):
    """Base response schema"""
    success: bool = Field(default=True, description="Request success status")
    message: str = Field(default="Success", description="Response message")

class DataResponse(BaseResponse, Generic[DataT]):
    """Response with data payload"""
    data: DataT = Field(..., description="Response data")

class ListResponse(BaseResponse, Generic[DataT]):
    """Response for list endpoints with pagination"""
    data: List[DataT] = Field(default_factory=list, description="List of items")
    total: int = Field(default=0, description="Total count of items")
    page: int = Field(default=1, ge=1, description="Current page number")
    page_size: int = Field(default=50, ge=1, le=100, description="Items per page")

    @property
    def total_pages(self) -> int:
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size

    @model_serializer(mode='wrap')
    def _serialize(self, serializer, info):
        data = serializer(self)
        
        # Create meta object
        meta = {
            "total": data.pop("total"),
            "page": data.pop("page"),
            "page_size": data.pop("page_size"),
            "total_pages": self.total_pages,
        }
        
        # Add meta to response
        data["meta"] = meta
        
        return data

class ErrorDetail(BaseModel):
    """Error detail schema"""
    field: str
    message: str
    type: str

class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = Field(default=False)
    status_code: int
    message: str
    error_type: str
    errors: Optional[List[ErrorDetail]] = None
    details: Optional[dict] = None
