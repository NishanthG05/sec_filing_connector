import argparse
import json
from pathlib import Path
from datetime import date
from sec_connector.client import SECClient
from sec_connector.models import FilingFilter


def load_companies_data():
    """Load company tickers data from fixtures."""
    fixture_path = Path(__file__).parent.parent / "tests" / "fixtures" / "company_tickers.json"
    with open(fixture_path) as f:
        return json.load(f)


def main():
    """
    CLI for SEC Filing Connector.
    
    Usage examples:
        python -m sec_connector.cli AAPL
        python -m sec_connector.cli AAPL --form 10-K
        python -m sec_connector.cli AAPL --form 10-K --limit 5
        python -m sec_connector.cli AAPL --date-from 2024-01-01 --date-to 2024-12-31
    """
    parser = argparse.ArgumentParser(
        description="Fetch and filter SEC EDGAR filings",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "ticker",
        type=str,
        help="Stock ticker symbol (e.g., AAPL, MSFT)"
    )
    
    parser.add_argument(
        "--form",
        type=str,
        action="append",
        dest="form_types",
        help="Filter by form type (can be used multiple times, e.g., --form 10-K --form 10-Q)"
    )
    
    parser.add_argument(
        "--date-from",
        type=str,
        help="Filter filings from this date (YYYY-MM-DD)"
    )
    
    parser.add_argument(
        "--date-to",
        type=str,
        help="Filter filings to this date (YYYY-MM-DD)"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of filings to return (default: 10)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    try:
        # Load companies data and create client
        companies_data = load_companies_data()
        client = SECClient(companies_data)
        
        # Lookup company
        print(f"Looking up ticker: {args.ticker}...")
        company = client.lookup_company(args.ticker)
        print(f"Found: {company.name} (CIK: {company.cik})\n")
        
        # Parse dates if provided
        date_from = date.fromisoformat(args.date_from) if args.date_from else None
        date_to = date.fromisoformat(args.date_to) if args.date_to else None
        
        # Create filter
        filters = FilingFilter(
            form_types=args.form_types,
            date_from=date_from,
            date_to=date_to,
            limit=args.limit
        )
        
        # Get filings
        print("Fetching filings...")
        filings = client.list_filings(company.cik, filters)
        
        # Output results
        if args.json:
            output = [
                {
                    "form_type": f.form_type,
                    "filing_date": f.filing_date.isoformat(),
                    "accession_number": f.accession_number
                }
                for f in filings
            ]
            print(json.dumps(output, indent=2))
        else:
            print(f"\nFound {len(filings)} filing(s):\n")
            print(f"{'Form Type':<12} {'Filing Date':<15} {'Accession Number'}")
            print("-" * 60)
            for filing in filings:
                print(f"{filing.form_type:<12} {filing.filing_date} {filing.accession_number}")
    
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())