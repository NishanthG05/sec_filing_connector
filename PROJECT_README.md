# SEC Filing Connector

A Python module for fetching and filtering SEC EDGAR filings.

## Installation
```bash
# Clone the repository onto machine
git clone https://github.com/YOUR_USERNAME/sec_filing_connector.git
cd sec_filing_connector

# Create virtual environment
python -m venv venv
source venv\Scripts\activate

# Install package e
pip install -e .
```
## Running the Tests
```bash
pytest tests/ -v
```

## Usage

### CLI Examples
```bash
# List all filings for a certain company
python -m sec_connector.cli AAPL

# Filter by form type specifically
python -m sec_connector.cli AAPL --form 10-K

# Filter by specified date range
python -m sec_connector.cli AAPL --date-from 2024-01-01 --date-to 2024-12-31

# Limit the results
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
│   ├── models.py
│   ├── client.py
│   └── cli.py
├── tests/
│   ├── fixtures/
│   └── test_client.py
├── pyproject.toml
└── README.md
```