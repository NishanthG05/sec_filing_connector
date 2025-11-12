from sec_connector.models import Company, Filing, FilingFilter


class SECClient:
    """Client for fetching SEC EDGAR filings."""
    
    def __init__(self, companies_data: dict[str, dict]):
        """
        Initialize with company ticker->info mapping.
        
        Args:
            companies_data: Dictionary mapping indices to company info dicts
        """
        self._companies = companies_data
    
    def lookup_company(self, ticker: str) -> Company:
        """
        Find company by ticker symbol.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            
        Returns:
            Company object with ticker, CIK, and name
            
        Raises:
            ValueError: If ticker is not found
        """
        ticker = ticker.upper()
        
        # Search through companies_data for matching ticker
        for key, company_info in self._companies.items():
            if company_info.get("ticker") == ticker:
                # Zero-pad CIK to 10 digits
                cik = str(company_info["cik_str"]).zfill(10)
                
                return Company(
                    ticker=ticker,
                    cik=cik,
                    name=company_info["title"]
                )
        
        raise ValueError(f"Ticker '{ticker}' not found")
    
    def list_filings(self, cik: str, filters: FilingFilter) -> list[Filing]:
        """
        Get filings for a CIK, applying filters.
        
        Args:
            cik: Company CIK number
            filters: FilingFilter object with optional form_types, date range, and limit
            
        Returns:
            List of Filing objects, sorted by date descending, limited by filters.limit
        """
        # For now, we'll mock this with sample data
        # In a real implementation, this would fetch from SEC EDGAR API
        
        # Mock data - you would fetch this from SEC API in production
        filings_data = self._load_mock_filings(cik)
        
        filings = []
        for i, accession in enumerate(filings_data["accessionNumber"]):
            filing = Filing(
                cik=cik,
                company_name=self._get_company_name(cik),
                form_type=filings_data["form"][i],
                filing_date=filings_data["filingDate"][i],
                accession_number=accession
            )
            filings.append(filing)
        
        # Apply form type filter
        if filters.form_types:
            filings = [f for f in filings if f.form_type in filters.form_types]
        
        # Apply date range filters
        if filters.date_from:
            filings = [f for f in filings if f.filing_date >= filters.date_from]
        
        if filters.date_to:
            filings = [f for f in filings if f.filing_date <= filters.date_to]
        
        # Sort by date descending (newest first)
        filings.sort(key=lambda f: f.filing_date, reverse=True)
        
        # Apply limit
        return filings[:filters.limit]
    
    def _get_company_name(self, cik: str) -> str:
        """Helper to get company name from CIK."""
        for company_info in self._companies.values():
            if str(company_info["cik_str"]).zfill(10) == cik:
                return company_info["title"]
        return "Unknown Company"
    
    def _load_mock_filings(self, cik: str) -> dict:
        """Load mock filing data for testing."""
        from pathlib import Path
        import json
        
        fixture_path = Path(__file__).parent.parent / "tests" / "fixtures" / "filings_sample.json"
        with open(fixture_path) as f:
            data = json.load(f)
        
        return data["filings"]["recent"]