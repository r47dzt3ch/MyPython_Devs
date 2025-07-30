from fastapi import APIRouter, Depends, HTTPException
from app.internal.dolphin_api.api import DolphinAPI
from app.core.config import settings

router = APIRouter()

def get_dolphin_api():
    return DolphinAPI(api_token=settings.DOLPHIN_API_TOKEN)

@router.get("/profiles")
async def list_profiles(dolphin_api: DolphinAPI = Depends(get_dolphin_api)):
    profiles = dolphin_api.get_profiles()
    if profiles:
        return profiles
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch profiles")