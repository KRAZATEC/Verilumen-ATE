from fastapi import APIRouter, HTTPException
from backend.app.ml.predict import PredictionRequest, PredictionResponse, predict_record
from backend.app.core.logging import logger

router = APIRouter(prefix="", tags=["Prediction"])


@router.post("/predict", response_model=PredictionResponse)
def run_prediction(req: PredictionRequest):
    try:
        response = predict_record(req)
        return response
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
