# Need_Analysis

AI-assisted job description extraction via Streamlit.

## Requirements

- Python 3.10+
- Packages from `requirements.txt`

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
streamlit run app.py
```

The UI now features `images/sthree.png` as the logo and a 50% transparent
background from `images/AdobeStock_506577005.jpeg` with matching accent colours.

### Environment variables

Optional settings used in `utils/openai_client.py`:

- `OPENAI_API_KEY`
- `OPENAI_ORG_ID`

Define them in your shell or inside `.streamlit/secrets.toml`.

## Project structure

```
app.py          # entry point
agents/         # OpenAI agent helpers
functions/      # extraction and search logic
utils/          # shared helpers
```

## Roadmap

Functions from [06_05_25_gpt_slim](https://github.com/KleinerBaum/06_05_25_gpt_slim)
will be integrated under `functions/` to extend job field extraction.

## Development

Run linting and typing checks:

```bash
ruff check .
black .
mypy .
```

Run tests (once they exist):

```bash
pytest
```

## Changelog

- Enhanced file extraction to reset pointers for DOCX and TXT files
- Improved Boolean search generation without city input
- Wizard navigation now uses Next/Back buttons and two-column layout for large steps
- Replaced deprecated `st.experimental_rerun()` with `st.rerun()` for Streamlit 1.45+
- Default start date to today's date when none stored


## Contributing

- Use feature branches named `feat/<description>` and open PRs against `dev`.
- Write Conventional Commit messages (`feat:`, `fix:`, etc.).

