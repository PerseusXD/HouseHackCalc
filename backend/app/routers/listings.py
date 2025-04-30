from fastapi import APIRouter, HTTPException
import logging
from ..services.listings_service import ListingService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/listings", tags=["listings"])



@router.get("/{zip_code}")
async def get_listings(zip_code: str):
    try:
        logger.info(f"Received request for zip code: {zip_code}")
        result = await ListingService.get_listings(zip_code)
        return result
    except ValueError as e:
        logger.error(f"Invalid zip code: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 