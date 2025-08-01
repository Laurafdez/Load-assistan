from fastapi import APIRouter
from app.business.healthcheck import HealthcheckManager
from fastapi import Depends

router = APIRouter()


@router.get("/", tags=["Healthcheck"])
def health(manager: HealthcheckManager = Depends()):
    return manager.status()
