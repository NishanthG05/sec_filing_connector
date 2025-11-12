# SEC Filing Connector

A Python module for fetching and filtering SEC EDGAR filings.

## Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/sec_filing_connector.git
cd sec_filing_connector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .
```

## Running Tests
```bash
pytest tests/ -v
```

All tests should pass.

## Usage

### CLI Examples
```bash
# List all filings for a company
python -m sec_connector.cli AAPL

# Filter by form type
python -m sec_connector.cli AAPL --form 10-K

# Filter by date range
python -m sec_connector.cli AAPL --date-from 2024-01-01 --date-to 2024-12-31

# Limit results
python -m sec_connector.cli AAPL --limit 5

# JSON output
python -m sec_connector.cli AAPL --json
```

### Python API
```python
from sec_connector.client import SECClient
from sec_connector.models import FilingFilter
from datetime import date

# Load company data and create client
companies_data = {...}  # Load from fixtures or API
client = SECClient(companies_data)

# Look up company
company = client.lookup_company("AAPL")
print(f"{company.name} - CIK: {company.cik}")

# Get filtered filings
filters = FilingFilter(
    form_types=["10-K"],
    date_from=date(2024, 1, 1),
    limit=5
)
filings = client.list_filings(company.cik, filters)

for filing in filings:
    print(f"{filing.form_type} - {filing.filing_date}")
```

## Project Structure
```
sec_filing_connector/
├── sec_connector/
│   ├── __init__.py
│   ├── models.py      # Pydantic data models
│   ├── client.py      # Core SEC client logic
│   └── cli.py         # Command-line interface
├── tests/
│   ├── fixtures/      # Test data
│   └── test_client.py # Unit tests
├── pyproject.toml
└── README.md
```

## Features

- ✅ Company lookup by ticker
- ✅ Filing filtering by form type
- ✅ Date range filtering
- ✅ Result limiting
- ✅ Type-safe with Pydantic models
- ✅ Comprehensive test coverage
- ✅ CLI and Python API

## Time Spent

Approximately 2-3 hours as specified in the assessment.