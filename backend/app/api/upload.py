from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.services.pipeline import process_dataset
from backend.app.core.logging import logger

router = APIRouter(prefix="", tags=["Upload"])


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    try:
        content = await file.read()
        res = process_dataset(content, filename=file.filename)
        return {"status": "success", "message": "File processed successfully", "data": res}
    except Exception as e:
        logger.error(f"Upload processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process CSV file: {str(e)}")


@router.post("/process-demo")
def process_demo_dataset():
    """Loads and processes the pre-generated synthetic dataset automatically."""
    from backend.app.core.config import settings
    demo_file = settings.DATA_DIR / "demo_ate_data.csv"
    if not demo_file.exists():
        raise HTTPException(status_code=404, detail="Demo file demo_ate_data.csv not found.")
    
    try:
        res = process_dataset(str(demo_file), filename="demo_ate_data.csv")
        return {"status": "success", "message": "Demo dataset processed", "data": res}
    except Exception as e:
        logger.error(f"Demo processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process demo dataset: {str(e)}")
