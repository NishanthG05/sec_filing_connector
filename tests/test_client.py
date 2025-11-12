import pytest
import json
from pathlib import Path
from sec_connector.client import SECClient
from sec_connector.models import Company
from datetime import date
from sec_connector.models import FilingFilter



@pytest.fixture
def companies_data():
    """Load test company data."""
    fixture_path = Path(__file__).parent / "fixtures" / "company_tickers.json"
    with open(fixture_path) as f:
        return json.load(f)


@pytest.fixture
def client(companies_data):
    """Create SECClient with test data."""
    return SECClient(companies_data)


class TestCompanyLookup:
    """Tests for company lookup functionality."""
    
    def test_lookup_valid_ticker(self, client):
        """Test looking up a valid ticker returns Company."""
        company = client.lookup_company("AAPL")
        
        assert isinstance(company, Company)
        assert company.ticker == "AAPL"
        assert company.cik == "0000320193"  # Zero-padded to 10 digits
        assert company.name == "Apple Inc."
    
    def test_lookup_case_insensitive(self, client):
        """Test ticker lookup is case-insensitive."""
        company_lower = client.lookup_company("aapl")
        company_upper = client.lookup_company("AAPL")
        
        assert company_lower.ticker == company_upper.ticker
        assert company_lower.cik == company_upper.cik
    
    def test_lookup_invalid_ticker_raises_error(self, client):
        """Test that invalid ticker raises ValueError."""
        with pytest.raises(ValueError, match="Ticker 'INVALID' not found"):
            client.lookup_company("INVALID")
    
    def test_cik_zero_padding(self, client):
        """Test that CIK is zero-padded to 10 digits."""
        company = client.lookup_company("AAPL")
        
        assert len(company.cik) == 10
        assert company.cik.startswith("0")

class TestListFilings:
    """Tests for filing list and filter functionality."""
    
    def test_list_all_filings(self, client):
        """Test listing all filings without filters."""
        filters = FilingFilter(limit=10)
        filings = client.list_filings("0000320193", filters)
        
        assert len(filings) == 4  # We have 4 filings in our test data
        assert all(f.cik == "0000320193" for f in filings)
    
    def test_filter_by_form_type(self, client):
        """Test filtering by form type (only 10-K)."""
        filters = FilingFilter(form_types=["10-K"], limit=10)
        filings = client.list_filings("0000320193", filters)
        
        assert len(filings) == 2
        assert all(f.form_type == "10-K" for f in filings)
    
    def test_filter_by_date_range(self, client):
        """Test filtering by date range."""
        filters = FilingFilter(
            date_from=date(2024, 1, 1),
            date_to=date(2024, 12, 31),
            limit=10
        )
        filings = client.list_filings("0000320193", filters)
        
        assert len(filings) == 2  # Only 2024 filings
        assert all(f.filing_date.year == 2024 for f in filings)
    
    def test_filings_sorted_by_date_descending(self, client):
        """Test that filings are sorted newest first."""
        filters = FilingFilter(limit=10)
        filings = client.list_filings("0000320193", filters)
        
        dates = [f.filing_date for f in filings]
        assert dates == sorted(dates, reverse=True)
    
    def test_limit_respected(self, client):
        """Test that limit parameter is respected."""
        filters = FilingFilter(limit=2)
        filings = client.list_filings("0000320193", filters)
        
        assert len(filings) == 2