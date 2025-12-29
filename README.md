````md
# ML-LLM-FastAPI-PSQL

A FastAPI project that serves:
- Classical Machine Learning models (Iris classification, Advertising sales prediction)
- An LLM-powered Product Review analyzer (LangChain + Google Gemini)

All requests and predictions are persisted to a PostgreSQL database via SQLModel.

---

## Important: Train the ML Models First (Required)

This repository expects pre-trained `.pkl` files to exist under `saved_models/`.  
Before you run the API, you **must** train the models so the application can load the `.pkl` artifacts at startup/runtime.

Training scripts:
- `train_iris_model.py`
- `train_advertising_model.py`

Generated artifacts:
- `saved_models/01.knn_with_iris_dataset.pkl`
- `saved_models/02.iris_label_encoder.pkl`
- `saved_models/03.randomforest_with_advertising.pkl`

---

## Screenshots

### Swagger UI
![Swagger UI](assets/8000.png)

### Advertising predictions stored in PostgreSQL
![Advertising table](assets/advertising.png)

### Iris predictions stored in PostgreSQL
![Iris table](assets/iris.png)

### Product review analysis stored in PostgreSQL
![Product review table](assets/review.png)

---

## Features

### 1) Product Review LLM (GenAI)
Analyzes a free-text review and returns structured output such as:
- rating (1–5)
- sentiment (positive/negative)
- key points (short bullet-like phrases)

Also stores the request + result into PostgreSQL.

### 2) Iris Prediction (ML)
KNN-based classifier that predicts Iris species from:
- sepal length/width
- petal length/width

Also logs inputs + prediction into PostgreSQL.

### 3) Advertising Prediction (ML)
Random Forest regression model predicting sales based on:
- TV, Radio, Newspaper spend

Also logs inputs + prediction into PostgreSQL.

---

## Tech Stack

- **API:** FastAPI, Uvicorn
- **Database:** PostgreSQL, SQLModel
- **ML:** scikit-learn, pandas, joblib
- **LLM:** LangChain, Google GenAI (Gemini)
- **DB runtime:** Docker (recommended for local PostgreSQL)

---

## Repository Structure

```text
.
├── assets/
│   ├── 8000.png
│   ├── advertising.png
│   ├── iris.png
│   └── review.png
├── routers/
│   ├── advertising.py
│   ├── iris.py
│   └── product_review_llm.py
├── saved_models/
│   ├── 01.knn_with_iris_dataset.pkl
│   ├── 02.iris_label_encoder.pkl
│   └── 03.randomforest_with_advertising.pkl
├── database.py
├── llm_app.py
├── main.py
├── models.py
├── requirements.txt
├── train_advertising_model.py
└── train_iris_model.py
````

---

## Prerequisites

* Python 3.10+ (recommended: 3.12, as your project uses `cpython-312` caches)
* Docker (for PostgreSQL)
* A Google GenAI API key (only required for the Product Review LLM endpoint)

---

## Setup and Run (Local)

### 1) Clone the repository

```bash
git clone https://github.com/oguztoy8/ML-LLM-FastAPI-PSQL.git
cd ML-LLM-FastAPI-PSQL
```

### 2) Create and activate a virtual environment

```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Start PostgreSQL with Docker

Example command (adjust credentials if you want):

```bash
docker run --rm -d \
  --name postgresql \
  -e POSTGRES_USER=train \
  -e POSTGRES_PASSWORD=sifre123 \
  -e POSTGRES_DB=traindb \
  -p 5432:5432 \
  postgres:15
```

### 5) Create a `.env` file

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY="your_google_api_key_here"
SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://train:sifre123@localhost:5432/traindb
```

Notes:

* `GOOGLE_API_KEY` is required for Product Review LLM requests.
* `SQLALCHEMY_DATABASE_URL` must match your PostgreSQL credentials/host/port.

### 6) Train the ML models (Required)

This step creates the `.pkl` files under `saved_models/`.

```bash
python train_iris_model.py
python train_advertising_model.py
```

### 7) Run the API

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open Swagger UI:

* [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Endpoints

### Product Review LLM

* **POST** `/product-review-llm/chat`

Example request:

```bash
curl -X POST "http://localhost:8000/product-review-llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": "john_doe",
    "product": "Wireless Headphones XYZ",
    "review": "Amazing product! Quick delivery and great quality, but quite pricey."
  }'
```

### Iris Prediction

* **POST** `/iris/prediction/iris`

Example request:

```bash
curl -X POST "http://localhost:8000/iris/prediction/iris" \
  -H "Content-Type: application/json" \
  -d '{
    "sepallengthcm": 5.1,
    "sepalwidthcm": 3.5,
    "petallengthcm": 1.4,
    "petalwidthcm": 0.2
  }'
```

### Advertising Prediction

* **POST** `/advertising/prediction/advertising`

Example request:

```bash
curl -X POST "http://localhost:8000/advertising/prediction/advertising" \
  -H "Content-Type: application/json" \
  -d '{
    "tv": 150.5,
    "radio": 45.2,
    "newspaper": 12.8
  }'
```

---

## Database Persistence

The application creates tables automatically on startup (if configured that way in `main.py/database.py`).

Typical tables in this project:

* `iris`
  Stores Iris feature inputs, predicted label, prediction timestamp, and client IP.
* `advertising`
  Stores TV/Radio/Newspaper inputs, predicted sales, prediction timestamp, and client IP.
* `products_review_rates`
  Stores user info, product, original review, extracted rating/sentiment/key points, and created timestamp.

---

## Common Issues / Troubleshooting

### 1) “File not found” for `.pkl`

Cause: Models were not trained yet.
Fix:

```bash
python train_iris_model.py
python train_advertising_model.py
```

### 2) LLM endpoint fails with authentication error

Cause: Missing or invalid `GOOGLE_API_KEY`.
Fix: Set the key in `.env` and restart the server.

### 3) Database connection errors

Cause: PostgreSQL not running or wrong `SQLALCHEMY_DATABASE_URL`.
Fix:

* Ensure Docker container is running:

  ```bash
  docker ps
  ```
* Verify `.env` connection string matches your credentials/port.

---

## Notes

* Do not commit your `.env` file.
* If you change model filenames or paths, update the loading logic accordingly (where the `.pkl` files are read).

---




