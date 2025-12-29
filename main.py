# imports
from fastapi import FastAPI
from routers import product_review_llm, iris, advertising
from dotenv import load_dotenv
from database import create_db_and_tables

load_dotenv()

# FastAPI app and routes
app = FastAPI(title="ML and LLM Application")

create_db_and_tables()

app.include_router(product_review_llm.router, prefix="/product-review", tags=["Product Review LLM"])
app.include_router(iris.router, prefix="/iris", tags=["Iris Prediction"])
app.include_router(advertising.router, prefix="/advertising", tags=["Advertising Prediction"])  


# Endpoints
@app.get("/")
def root():
    return {"message": "Welcome to the ML and LLM Application"}