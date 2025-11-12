from pydantic import BaseModel, Field, field_validator
from datetime import date


class Company(BaseModel):
    """Represents a company with SEC identifiers."""
    ticker: str = Field(..., min_length=1, description="Stock ticker symbol")
    cik: str = Field(..., pattern=r'^\d{10}$', description="10-digit CIK number")
    name: str = Field(..., min_length=1, description="Company name")
    
    @field_validator('ticker')
    @classmethod
    def ticker_must_be_uppercase(cls, v: str) -> str:
        """Ensure ticker is uppercase."""
        return v.upper().strip()


class Filing(BaseModel):
    """Represents an SEC filing."""
    cik: str = Field(..., pattern=r'^\d{10}$')
    company_name: str = Field(..., min_length=1)
    form_type: str = Field(..., min_length=1)
    filing_date: date
    accession_number: str = Field(..., min_length=1)


class FilingFilter(BaseModel):
    """Filter criteria for SEC filings search."""
    form_types: list[str] | None = Field(None, description="List of form types to filter by")
    date_from: date | None = Field(None, description="Start date for filtering")
    date_to: date | None = Field(None, description="End date for filtering")
    limit: int = Field(10, gt=0, le=100, description="Maximum number of results (1-100)")
    
    @field_validator('date_to')
    @classmethod
    def date_to_must_be_after_date_from(cls, v: date | None, info) -> date | None:
        """Ensure date_to is after date_from if both are provided."""
        date_from = info.data.get('date_from')
        if v and date_from and v < date_from:
            raise ValueError('date_to must be after date_from')
        return v