
# ML-LLM-FastAPI-PSQL

A FastAPI project that serves:
- Classical Machine Learning models (Iris classification, Advertising sales prediction)
- An LLM-powered Product Review analyzer (LangChain + Google Gemini)

All requests and predictions are persisted to a PostgreSQL database via SQLModel.

---

## Important: Train the ML Models First (Required)

This repository expects pre-trained `.pkl` files to exist under `saved_models/`.  
Before running the API, you **must** train the models so the application can load the `.pkl` artifacts at runtime.

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
- sentiment (positive / negative)
- key points (short extracted phrases)

The request and analysis result are persisted to PostgreSQL.

---

### 2) Iris Prediction (ML)

KNN-based classifier that predicts Iris species using:
- sepal length
- sepal width
- petal length
- petal width

Input features and predictions are logged to PostgreSQL.

---

### 3) Advertising Prediction (ML)

Random Forest regression model that predicts sales based on:
- TV budget
- Radio budget
- Newspaper budget

Predictions are stored in PostgreSQL.

---

## Tech Stack

- **API:** FastAPI, Uvicorn
- **Database:** PostgreSQL, SQLModel
- **Machine Learning:** scikit-learn, pandas, joblib
- **LLM:** LangChain, Google GenAI (Gemini)
- **Database Runtime:** Docker

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

* Python 3.10+ (recommended: Python 3.12)
* Docker (for PostgreSQL)
* Google GenAI API key (required only for Product Review LLM)

---

## Setup and Run (Local)

### 1) Clone the repository

```bash
git clone https://github.com/oguztoy8/ML-LLM-FastAPI-PSQL.git
cd ML-LLM-FastAPI-PSQL
```

---

### 2) Create and activate a virtual environment

```bash
python -m venv venv

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source venv/bin/activate
```

---

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4) Start PostgreSQL with Docker

```bash
docker run --rm -d \
  --name postgresql \
  -e POSTGRES_USER=train \
  -e POSTGRES_PASSWORD=sifre123 \
  -e POSTGRES_DB=traindb \
  -p 5432:5432 \
  postgres:15
```

---

### 5) Create a `.env` file

Create a `.env` file in the project root directory:

```env
GOOGLE_API_KEY=your_google_api_key_here
SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://train:sifre123@localhost:5432/traindb
```

Notes:

* `GOOGLE_API_KEY` is required only for the LLM endpoint
* Database credentials must match the Docker configuration

---

### 6) Train the ML models (Required)

```bash
python train_iris_model.py
python train_advertising_model.py
```

This step generates the `.pkl` files under `saved_models/`.

---

### 7) Run the API

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Swagger UI:

* [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Endpoints

### Product Review LLM

* **POST** `/product-review-llm/chat`

```bash
curl -X POST "http://localhost:8000/product-review-llm/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_info": "john_doe",
    "product": "Wireless Headphones XYZ",
    "review": "Amazing product! Quick delivery and great quality, but quite pricey."
  }'
```

---

### Iris Prediction

* **POST** `/iris/prediction/iris`

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

---

### Advertising Prediction

* **POST** `/advertising/prediction/advertising`

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

Tables are created automatically on application startup.

Typical tables:

* `iris`
* `advertising`
* `products_review_rates`

Each table stores inputs, predictions, timestamps, and client metadata.

---

## Common Issues

### Missing `.pkl` files

```bash
python train_iris_model.py
python train_advertising_model.py
```

---

### LLM authentication error

Ensure `GOOGLE_API_KEY` is set correctly in `.env`.

---

### Database connection error

```bash
docker ps
```

Verify `SQLALCHEMY_DATABASE_URL`.

---

## Notes

* Do not commit the `.env` file
* Update model loading paths if `.pkl` filenames change

```
```
