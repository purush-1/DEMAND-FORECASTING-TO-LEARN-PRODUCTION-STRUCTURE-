# Demand Forecasting: Learning Production Structure

A small project for learning how to take a forecasting model out of a notebook and put it into a production-style layout: a reusable package for features and training, a FastAPI service for serving, tests, and a Docker image.

The model is an **XGBoost regressor** that predicts the **next day's order quantity** from same-day sales figures, lagged quantities, a 7-day moving average and calendar features.

> **Status:** work in progress. This is a learning repo, and a few known rough edges are listed under [Known issues](#known-issues).

## Project structure

```
.
├── src/demand_forecasting/       # Installable package (ML code)
│   ├── datapipeline.py           # Aggregation, lag, rolling and calendar features
│   ├── create_model.py           # XGBRegressor configuration
│   ├── train.py                  # Training script, saves the model to models/
│   └── predict.py                # Batch prediction helper
├── app/                          # FastAPI service
│   ├── api.py                    # App setup, routers, timing middleware
│   ├── config.py                 # Settings (model file name and path)
│   ├── dependencies.py           # Loads the model once at startup
│   ├── load_model.py             # XGBoost model loading
│   ├── schemas.py                # Pydantic request/response models
│   ├── routes/
│   │   ├── health.py             # GET /health
│   │   ├── model_check.py        # GET /model
│   │   └── predict.py            # POST predict endpoint
│   └── test_api.py               # API tests
├── test_features/features_test.py  # Feature engineering tests
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```

`data/` and `models/` are git-ignored, so the dataset and the trained model are not in the repo and must be created locally (see below).

## How it works

### Features (`datapipeline.py`)

| Step | Function | What it does |
|---|---|---|
| 1 | `aggeragate` | Groups raw orders by `Date`, summing revenue, cost, profit, quantity, unit cost and unit price into `Sales`, `Cost`, `Profit`, `Quantity`, `Unit_Cost`, `Unit_Price` |
| 2 | `rolling_features` | `MA_7`, the 7-day moving average of `Quantity` (shifted by 1 day to avoid leakage) |
| 3 | `lag_features` | `Lag_1`, `Lag_7`, `Lag_30` of `Quantity` |
| 4 | `time_features` | `Month`, `Year`, `Quarter`, `Dayofweek`, `Dayofyear` from `Date` |
| – | `get_dummies` | One-hot encodes a `Product` column (used only in `predict.py`) |

### Training (`train.py`)

1. Reads `data/sales_data.csv` (expects columns `Date`, `Revenue`, `Cost`, `Profit`, `Order_Quantity`, `Unit_Cost`, `Unit_Price`).
2. Builds the features above and sets `Target = Quantity.shift(-1)`, the next day's quantity.
3. Trains `XGBRegressor(n_estimators=2500, learning_rate=0.005, max_depth=5)` on all rows.
4. Saves the model to `models/demand_forecasting_model.json`.

### Serving (`app/`)

The API loads the saved model once at startup and exposes:

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness check, returns `{"health": "ok"}` |
| GET | `/model` | Confirms the model is loaded |
| POST | `/api v1/ predict/Predict` | Returns a forecast for one input row |

Requests are validated with Pydantic. Every field is a non-negative integer, and `Month` (1–12), `Quarter` (1–4), `Dayofweek` (0–6) and `Dayofyear` (1–365) have range checks. A timing middleware logs how long each request takes.

**Example request body**

```json
{
  "Sales": 1430, "Cost": 34, "Profit": 452, "Quantity": 41,
  "Unit_Cost": 540, "Unit_Price": 133, "MA_7": 3248,
  "Lag_1": 343, "Lag_7": 234, "Lag_30": 343,
  "Month": 2, "Year": 2000, "Quarter": 1, "Dayofweek": 5, "Dayofyear": 37
}
```

**Response**

```json
{ "Forecast": 100.0 }
```

## Getting started

Requires Python 3.12.

```bash
# 1. Install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

# 2. Add your data at data/sales_data.csv, then train
python -m demand_forecasting.train

# 3. Run the API
uvicorn app.api:app --reload
```

Interactive docs are served at `http://localhost:8000/docs`.

### Docker

Train the model first so `models/` exists, then:

```bash
docker build -t demand-forecasting .
docker run -p 8000:8000 demand-forecasting
```

The image copies in `app/` and `models/`.

## Tests

```bash
pip install pytest httpx
pytest
```

- `app/test_api.py` covers the health check, a valid prediction (with a fake model), input validation (422), a model failure (500) and the timing middleware.
- `test_features/features_test.py` checks the lag and rolling-average features against known values.

## Tech stack

Python 3.12 · XGBoost · pandas · scikit-learn · FastAPI · Pydantic · Uvicorn · Docker · pytest

## Known issues

Things I noticed while documenting the repo, worth fixing next:

- **Route paths.** The predict router is mounted at `/api v1/ predict` (with spaces), and the tests call `/Predict` and `/Health`, which don't match the routes as written (`/health`, `/api v1/ predict/Predict`). Using `/api/v1/predict` and updating the tests would line them up.
- **`Quarter` feature.** `time_features` sets `Quarter` from `dt.year`; it should be `dt.quarter`.
- **`predict.py` is incomplete.** It imports `target_lag_features`, which doesn't exist, and `XGBRegressor` isn't imported. `load_model` also returns `None` because `load_model()` on the model returns nothing.
- **Preprocessing at serving time.** The API sends the raw row straight to the model and doesn't use the feature pipeline, so callers must supply `MA_7` and the lag values themselves.
- **Duplicated config.** `pyproject.toml` has two `[project]` tables, and `app/routes/middleware.py` duplicates the middleware in `api.py` and isn't used.
- **No evaluation.** `train.py` fits on all data with no train/validation split or metrics.

## License

No license has been added yet.
