# Amazon Order Flow Automation

## Project Overview
This project automates an Amazon shopping flow using **Playwright with Python** and the **Page Object Model (POM)** design pattern.

The main happy-path test:
1. Opens the Amazon home page.
2. Searches for a wireless product.
3. Opens the first search result.
4. Adds the product to the cart.
5. Verifies the cart item and subtotal.
6. Proceeds to checkout and stops. **No order is placed.**

The suite also includes negative and edge-case scenarios.

## Tech Stack
- Python
- Playwright (Python)
- Pytest
- Page Object Model (POM)
- Pytest HTML report

## Project Structure
```text
amazon-playwright-pom/
├── pages/                 # Page Object classes
├── tests/                 # Automated test cases
├── config.py              # Test configuration
├── conftest.py            # Shared pytest fixtures
├── pytest.ini             # Pytest configuration and markers
├── requirements.txt       # Python dependencies
├── report.html            # HTML execution report (if included)
└── README.md
```

## Setup
1. Install Python 3.12 or a compatible Python version.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:

```bash
playwright install chromium
```

## Running the Tests

Run the complete suite:

```bash
pytest -v
```

Run with the browser visible:

```bash
pytest --headed
```

Run a specific group:

```bash
pytest -m happy_path -v
pytest -m negative -v
pytest -m edge -v
```

Run all three groups together:

```bash
pytest -m "happy_path or negative or edge" -v
```

## Automated Scenarios

- Happy path: product search through checkout entry, without placing an order.
- Negative: search with text expected to return no matching results.
- Negative: submit an empty search.
- Negative: verify an empty guest cart.
- Negative: verify guest checkout requires sign-in.
- Edge: remove the only cart item.
- Edge: search using special characters.
- Edge: search using a long input string.

See `Test_Cases.xlsx` for the scenario-level test case list.

## AI Tools & Usage

- Claude AI was used as an AI-assisted development tool to explore
  automation approaches, review code structure, troubleshoot issues,
  and refine test scenarios.
- AI-generated suggestions were reviewed, modified where necessary,
  and validated through test execution.
- Test implementation and execution results were verified against
  the actual application behaviour.

## Latest Execution Summary

| Metric | Result |
|---|---:|
| Browser | Chromium |
| Tests collected | 8 |
| Passed | 8 |
| Failed | 0 |
| Warnings | 1 |
| Execution time | 160.31 seconds |

The warning observed in this run was a Pytest deprecation warning concerning a session-scoped fixture defined as an instance method. It did not cause a test failure.

## Notes and Limitations
- Amazon is a live third-party website. Page content, search results, availability, loading time, CAPTCHA challenges, and session behaviour may change.
- A successful run demonstrates the result for that execution; it does not guarantee identical results on every future run.
- The checkout test intentionally stops before order placement. No purchase is made by this test.
- Do not include personal credentials, browser cookies, authentication state files, or local virtual-environment folders when sharing the project.
