from fastapi import Request, Depends
from sqlmodel import Session
from fastapi.routing import APIRouter
from models import Advertising, RequestAdvertising
from database import get_db
import joblib

router = APIRouter()

advertising_estimator_loaded = joblib.load("saved_models/03.randomforest_with_advertising.pkl")


def make_advertising_prediction(estimator, input_data):
    data = [[
        input_data["tv"],
        input_data["radio"],
        input_data["newspaper"]
    ]]
    prediction = estimator.predict(data)
    return  prediction[0].item()


# save prediction to database function to be implemented
def insert_advertising(request, prediction, client_ip, db):
    new_advertising = Advertising(
        tv=request["tv"],
        radio=request['radio'],
        newspaper=request['newspaper'],
        prediction=prediction,
        client_ip=client_ip
    )

    with db as session:
        session.add(new_advertising)
        session.commit()
        session.refresh(new_advertising)

    return new_advertising

@router.post("/prediction/advertising")
def predict_advertising(request: RequestAdvertising, fastapi_req: Request,  db: Session = Depends(get_db)):
    prediction = make_advertising_prediction(advertising_estimator_loaded, request.dict())
    #save prediction to database 
    db_insert_record = insert_advertising(request.dict(), prediction, fastapi_req.client.host, db)
    return {"prediction": prediction, "db_record": db_insert_record}