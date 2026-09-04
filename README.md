# QA Testing Portfolio

QA Engineer with hands-on experience in manual testing, API testing, and test automation. This repo covers the full testing lifecycle: test case design, bug reporting, API testing, and automated end-to-end test suites.

**Applications under test:** [Sauce Demo](https://www.saucedemo.com/) (sample e-commerce site) and [the-internet](https://the-internet.herokuapp.com/) (QA practice site).

## What's in here

### `manual-testing/`
A 34-case manual test suite for Sauce Demo covering login, product listing, cart, and checkout flows. Applies equivalence partitioning and boundary value analysis. Includes the functional defects found during execution.

### `bug-reports/`
Formal bug reports tracked in Jira with repro steps, severity/priority, and screenshot evidence:
- **KAN-1 — Empty-cart checkout completion:** Sauce Demo allows a full order to be placed with 0 items in the cart, including an order confirmation and receipt
- **KAN-3 — Missing zip code validation:** the checkout form accepts a 20-character postal code with no validation error, and the invalid value carries through to the order receipt

### `api-testing/`
A Postman collection testing the [ReqRes](https://reqres.in/) REST API: authenticated requests, scripted assertions, cross-request variable chaining, and response type validation.

**To run:** import both JSON files into Postman, get a free API key from [app.reqres.in/api-keys](https://app.reqres.in/api-keys), and set it as the `apiKey` environment variable.

### `automation/`
Selenium + pytest automation suites.

```
automation/
├── requirements.txt
├── saucedemo/
│   └── test_saucedemo_e2e.py      # valid/invalid login + full checkout, parametrized across products
├── the-internet/
│   └── test_checkboxes.py         # checkbox default state and toggle behaviour
└── exploratory-practice/
    └── YT_search_and_play_full_video_automation.py
```

Built with pytest fixtures for setup/teardown, explicit waits (`WebDriverWait` + expected conditions), and `@pytest.mark.parametrize` for data-driven tests.

The `exploratory-practice/` script is a browser automation exercise rather than a test suite — it searches YouTube, plays the first result, and handles dynamically generated class names, pre-roll ad detection, and custom wait conditions.

**To run the test suites:**
```
pip install -r automation/requirements.txt
pytest automation/ -v
```

## Skills demonstrated
Manual testing, test case design (EP/BVA), bug lifecycle management, Jira, API testing, Postman, Selenium WebDriver, pytest, Python

---
[LinkedIn](https://www.linkedin.com/in/heidialhadad/)
