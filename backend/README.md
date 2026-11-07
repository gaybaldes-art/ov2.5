# MATCHLAB API

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API docs.

## Test

```bash
cd backend
pytest
```

## Forecast endpoint

`POST /api/v1/forecast`

```json
{
  "home_xg": 1.45,
  "away_xg": 1.10,
  "max_goals": 10
}
```

Important: this first version expects xG inputs from a trusted data source or an analyst. It deliberately does not fabricate fixtures, team form, injuries, or xG values.
