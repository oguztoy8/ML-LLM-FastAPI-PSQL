from fastapi.routing import APIRouter
from fastapi import Request, Depends
from sqlmodel import Session
from database import get_db
from models import Iris, RequestIris
import joblib

router = APIRouter()

iris_classifier_loaded = joblib.load("saved_models/01.knn_with_iris_dataset.pkl")
iris_encoder_loaded = joblib.load("saved_models/02.iris_label_encoder.pkl")

def make_iris_prediction(estimator, encoder, input_data):
    data = [[
        input_data["sepallengthcm"],
        input_data["sepalwidthcm"],
        input_data["petallengthcm"],
        input_data["petalwidthcm"]
    ]]
    prediction_raw = estimator.predict(data)
    prediction_real = encoder.inverse_transform(prediction_raw)
    return  prediction_real[0]

def insert_iris(request, prediction, client_ip, db):
    new_iris = Iris(
        sepallengthcm=request["sepallengthcm"],
        sepalwidthcm=request["sepalwidthcm"],
        petallengthcm=request["petallengthcm"],
        petalwidthcm=request["petalwidthcm"],
        prediction=prediction,
        client_ip=client_ip
    )

    with db as session:
        session.add(new_iris)
        session.commit()
        session.refresh(new_iris)

    return new_iris


@router.post("/prediction/iris")
def predict_iris(request: RequestIris, fastapi_req: Request,  db: Session = Depends(get_db)):
    prediction = make_iris_prediction(iris_classifier_loaded, iris_encoder_loaded, request.dict())
    # save prediction to database
    db_insert_record = insert_iris(request.dict(), prediction, fastapi_req.client.host, db)
    return {"prediction": prediction, "db_record": db_insert_record}
    