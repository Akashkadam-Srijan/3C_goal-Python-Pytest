# 3Cgoal-Python-Pytest

A small end-to-end testing framework using Python, Pytest and Selenium (WebDriver).

This repository contains page objects, tests, reusable browser utilities, and test reports. The README documents how to set up, run, and extend the project so team members can get started quickly.

--

## Table of contents
- Overview
- Tech stack & pre-requisites
- Project structure (current)
- Quick setup
- Running tests & reports
- Page Object Model (POM) and utilities
- Example: reusable `BrowserUtils.print_css_properties`
- Fixing `AttributeError: 'ShopPage' object has no attribute 'utils'`
- Fixtures (`conftest.py`) examples
- CI example (GitHub Actions)
- Troubleshooting
- Contributing


## Overview
This repo demonstrates automated UI tests written with:
- Python 3.11+
- Pytest as the test runner
- Selenium WebDriver for browser automation
- Page Object Model (POM) for organizing page interactions

It includes utilities for browser interactions and reports generated after test runs.


## Tech stack & pre-requisites
- Python 3.11 (or compatible 3.8+)
- ChromeDriver / geckodriver (or use webdriver-manager)
- pip

Recommended packages (example):
- selenium
- pytest
- pytest-html
- pytest-xdist (optional)

Example minimal `requirements.txt`:
```
selenium>=4.0
pytest>=7.0
pytest-html
pytest-xdist
webdriver-manager
```


## Project structure (existing)
Your workspace currently contains the following structure (trimmed):

```
Python_Pytest/
  PageObject/
    shop.py
    login.py
    checkout_confirmation.py
  utils/
    browserUtils.py
  conftest.py
  pytest.ini
  test_e2e.py
  reports/
    report.html
```

Notes:
- Page objects live in `PageObject/` and encapsulate locators and page actions.
- Reusable helpers live in `utils/` (for example `browserUtils.py`).
- Tests and fixtures are at project root (e.g., `test_e2e.py`, `conftest.py`).


## Quick setup
1. Create and activate a virtual environment:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. If you don't have a `requirements.txt`, install the essentials:

```
pip install selenium pytest pytest-html webdriver-manager
```

3. Ensure a compatible WebDriver is available (ChromeDriver for Chrome). You can use `webdriver-manager` to avoid manual driver handling.


## Running tests & generating reports
- Run all tests (quiet):

```
pytest -q
```

- Run a single file:

```
pytest Python_Pytest/test_e2e.py -q
```

- Generate an HTML report:

```
pytest --html=report.html
```

- Run tests in parallel (if `pytest-xdist` installed):

```
pytest -n auto
```


## Page Object Model (POM) and utilities
- Keep selectors and actions inside page object classes (`PageObject/*.py`).
- Keep browser helpers in `utils/browserUtils.py` (timeouts, waits, logging, screenshots).

Design contract for a small helper class `BrowserUtils`:
- Inputs: Selenium WebDriver and WebElement(s)
- Outputs: prints/logs or returns computed values
- Error modes: element not attached, stale element, None input

Edge cases to consider:
- Element is stale or detached
- Element is not visible/interactable
- Browser/driver not initialized


## Example: reusable BrowserUtils.print_css_properties
Create a small helper in `utils/browserUtils.py` and reuse it across page objects and tests.

Example implementation (place in `utils/browserUtils.py`):

```
# utils/browserUtils.py
from selenium.common.exceptions import WebDriverException

class BrowserUtils:
    def __init__(self, driver):
        self.driver = driver

    def print_css_properties(self, element):
        """Print common CSS properties for a WebElement.

        Safe to call — handles common WebDriver exceptions and logs values.
        """
        if element is None:
            print("print_css_properties: element is None")
            return

        try:
            print("Background-color:", element.value_of_css_property("background-color"))
            print("Color:", element.value_of_css_property("color"))
            print("Font-size:", element.value_of_css_property("font-size"))
        except WebDriverException as e:
            print("print_css_properties: WebDriverException:", e)
```


## Fixing `AttributeError: 'ShopPage' object has no attribute 'utils'`
You saw this error when calling `self.utils.print_css_properties(checkout_button)` from a page object.

Two recommended patterns to provide `utils` to page objects:

1) Instantiate `BrowserUtils` inside the page object (simple, local):

```
# PageObject/shop.py
from utils.browserUtils import BrowserUtils

class ShopPage:
    def __init__(self, driver):
        self.driver = driver
        # Provide a utils instance so methods can call `self.utils` safely
        self.utils = BrowserUtils(driver)

    def goToCart(self):
        checkout_button = self.driver.find_element(*self.check_out_Button)
        self.utils.print_css_properties(checkout_button)
        # continue with clicking or other interactions
```

2) Provide `BrowserUtils` via a pytest fixture and pass it in from tests (preferred for DI and test control):

```
# conftest.py
import pytest
from utils.browserUtils import BrowserUtils
from selenium import webdriver

@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # or use webdriver-manager to create safely
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def browser_utils(driver):
    return BrowserUtils(driver)
```

Then in your test:

```
# test_e2e.py
from PageObject.shop import ShopPage

def test_shop_to_cart(driver, browser_utils):
    shop = ShopPage(driver)
    # Option A: set utils from test
    shop.utils = browser_utils

    # or Option B: pass utils into the method if you prefer explicit args
    shop.goToCart()
```

If you prefer not to mutate the page object from tests, pass the `browser_utils` instance into the page object at creation time:

```
shop = ShopPage(driver)
shop.utils = browser_utils
```


## Fixtures (`conftest.py`) examples
Recommended fixtures:
- `driver` — returns a WebDriver instance and tears it down after tests
- `browser_utils` — returns a `BrowserUtils` instance
- `config` — optional, loads test config such as base_url or credentials

Example `conftest.py` snippet:

```
import pytest
from selenium import webdriver
from utils.browserUtils import BrowserUtils

@pytest.fixture(scope='session')
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def browser_utils(driver):
    return BrowserUtils(driver)
```


## CI example (GitHub Actions)
A minimal GitHub Actions workflow to run tests:

```
name: Pytest
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt
      - name: Run tests
        run: pytest --maxfail=1 -q --html=report.html
```


## Troubleshooting
- AttributeError: `self.utils` — add `self.utils = BrowserUtils(self.driver)` in the page object or assign the fixture-provided instance from the test.
- StaleElementReferenceException — re-find the element before interacting.
- WebDriver not found — use `webdriver-manager` or ensure chromedriver/geckodriver is on PATH.


## Contributing
- Follow PEP8 and project conventions
- Add tests for new helpers and page object methods
- Keep utilities generic and reusable


## Next steps (suggested)
- Add a `requirements.txt` if missing
- Add a `tests/` folder and split tests from the page objects
- Add a `Makefile` or helper scripts for common commands (run tests, generate report)
- Add a small `README` section for onboarding new contributors with a standard test run


---

If you'd like, I can also:
- Create or update `utils/browserUtils.py` with the example helper (I see a `utils/browserUtils.py` file exists; I can open and update it),
- Add the `conftest.py` fixtures shown above, or
- Run the project's tests locally and share the output.

Tell me which of those you'd like me to do next.
