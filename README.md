# Need_Analysis

AI-assisted job description extraction via Streamlit.

## Requirements

- Python 3.10+
- Packages from `requirements.txt`
- Plotly for salary visualisation

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

## License

This project is licensed under the [MIT License](LICENSE).

app.py
