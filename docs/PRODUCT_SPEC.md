# MATCHLAB — Product specification

## Vision

MATCHLAB is a football match intelligence workspace. It combines deterministic statistical analysis, explainable AI commentary, and transparent evaluation of historical forecasts.

The product is an analytical tool, not a betting-advice service. It must never imply guaranteed outcomes or fabricate data.

## Product principles

1. **Data before language models.** All probabilities come from explicit statistical code and identified input data. The language model may explain outputs, but may not invent or alter them.
2. **Traceability.** Every analysis records its input data, model version, calculation timestamp, and assumptions.
3. **Honest uncertainty.** Missing data is shown as missing. Confidence is not a substitute for calibrated probability.
4. **Measurable quality.** Forecasts are stored before kickoff and evaluated against final results.
5. **Security by default.** Secrets live only in server-side environment variables. No API key may be shipped in browser JavaScript or committed to Git.

## MVP scope

### 1. Match Radar
- Upcoming fixtures with competition, kickoff time, and team names.
- Filters by date and competition.
- Match detail view with home/away comparison.
- Clear indication of data freshness and missing fields.

### 2. Statistical Engine
- Independent Poisson goal model as the initial baseline.
- 1X2, over/under, and both-teams-to-score probabilities derived from the same score matrix.
- Explicit model assumptions and configurable goal-rate inputs.
- Unit tests for probability normalization and edge cases.

### 3. Analyst
- Converts structured model output into concise explanations.
- Must cite only facts supplied in the analysis payload.
- Must distinguish measured data, model estimates, and qualitative interpretation.
- Must not produce unsupported confidence scores.

### 4. Performance Lab
- Persist immutable pre-match forecasts.
- Record final scores after matches finish.
- Report sample size, log loss, Brier score, and calibration by probability bucket.
- ROI, if later added, is explicitly simulated and never presented as a guaranteed return.

## Initial architecture

- **Frontend:** evolve the existing `index.html` interface in this repository.
- **Backend:** Python API, reusing and refactoring the statistical logic from `gaybaldes-art/football-analyst`.
- **Domain layer:** typed match, team-statistics, forecast, and result schemas.
- **Persistence:** SQLite for local MVP; keep repository interfaces portable to PostgreSQL.
- **AI layer:** optional server-side explanation provider behind an interface; no provider key in client code.
- **Testing:** deterministic unit tests for calculations and API contract tests.

## Delivery milestones

### Milestone 1 — Safe foundation
- Remove browser-exposed credentials and route provider calls through a backend.
- Define data contracts and environment configuration.
- Add a reproducible local development setup.

### Milestone 2 — Statistical core
- Extract pure probability functions from the existing Python application.
- Add tests for score matrices, 1X2, totals, and BTTS.
- Return a structured forecast payload.

### Milestone 3 — Product interface
- Connect the dashboard to the backend.
- Add match detail, model explanation, and data-quality indicators.

### Milestone 4 — Evaluation
- Persist forecasts and results.
- Add historical metrics and calibration reporting.

## Security action required

The current frontend source has previously been identified as containing a provider credential in client-side JavaScript. Treat that credential as compromised: revoke/rotate it in the provider console, remove it from the frontend source, and store the replacement only in server-side environment configuration. Removing it from the latest commit does not erase it from Git history.

## Non-goals for the first release

- Automated betting or account execution.
- Claims of guaranteed profit.
- Predictions generated solely by an LLM.
- Complex model training before a reliable baseline and historical evaluation exist.

## Definition of done for the MVP

A user can select a fixture, inspect its data, obtain reproducible probabilities from the statistical engine, read an explanation grounded in those outputs, and later see how the forecast performed.
