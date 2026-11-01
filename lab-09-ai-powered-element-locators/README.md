# Lab 9: AI-Powered Techniques for Locating Elements

## Objectives
- Explore natural-language element location with SeleniumBase AI methods.
- Compare AI-assisted login with traditional CSS selectors.
- Search and save result titles and URLs as JSON.
- Exercise contextual and semantic AI examples.

## Requirements
Python 3.10+, Chrome/Chromium, network access, SeleniumBase, and an OpenAI API key for AI locator calls. AI calls may incur API usage costs. Keep the key private and never commit it.

## Setup

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r lab-09-ai-powered-element-locators/requirements.txt
    seleniumbase install chromedriver

Set the key in your shell: export OPENAI_API_KEY="your-api-key". PowerShell: $env:OPENAI_API_KEY="your-api-key". Do not place the key in source files or GitHub.

## Run
From the lab directory:

    pytest -v -s lab9_ai_locators.py
    pytest -v -s google_search_ai.py
    pytest -v -s ai_comparison_analysis.py
    pytest -v -s advanced_ai_examples.py
    python results_summary.py

## Scripts and outputs
- lab9_ai_locators.py: AI and traditional login flows.
- google_search_ai.py: natural-language search field interaction and result extraction.
- ai_comparison_analysis.py: captures success, duration, and errors for login approaches.
- advanced_ai_examples.py: contextual, semantic, and dynamic control examples.
- results_summary.py: summarizes generated artifacts.
- Runtime outputs include ai_vs_traditional.log, ai_comparison_results.json, and google_search_results.json.

## Important notes
AI locators may require external model access, network connectivity, and extra latency. AI-only tests are skipped if OPENAI_API_KEY is absent; the traditional CSS login test remains runnable. Google markup, consent screens, and automated access restrictions can change, so the script records results actually observed rather than promising five results.

## Troubleshooting
- Missing key: set OPENAI_API_KEY in the current shell.
- API error: verify key and account access; never expose the key in a commit.
- Driver error: run seleniumbase install chromedriver and verify Chrome.
- Locator timeout: confirm page load and use a clearer natural-language description.
- Google extraction empty: inspect current page markup and retry later.
- Missing JSON: inspect test output and ensure the corresponding test completed.

## Security and cost
Use public demo pages and test accounts only. AI requests can send page context to an external service and may be billable. Do not use private customer data unless organizational policy explicitly allows it.

## Completion checklist
- [ ] SeleniumBase installed.
- [ ] Traditional login executed.
- [ ] AI login executed or intentionally skipped without a key.
- [ ] Search extraction attempted.
- [ ] Comparison JSON reviewed.
- [ ] Advanced examples reviewed.
