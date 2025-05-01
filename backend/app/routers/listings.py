from fastapi import APIRouter, HTTPException
from typing import Dict, List
import logging
from ..services.listings_service import ListingService
from ..database import State, ZipCode, get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/state/{state}")
async def get_listings_by_state(state: str) -> Dict[str, List[Dict]]:
    """
    Get all listings for a state, organized by zip code.
    Returns a dictionary where keys are zip codes and values are lists of listings.
    """
    try:
        logger.info(f"Fetching listings for state: {state}")
        listings = await ListingService.get_listings_by_state(state)
        return listings
    except ValueError as e:
        logger.error(f"Invalid state code: {state}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching listings for state {state}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cache-info")
async def get_cache_info() -> Dict:
    """
    Get information about cached data in the database.
    Returns a dictionary containing information about states and their zip codes.
    """
    try:
        logger.info("Fetching cache information")
        db = next(get_db())
        try:
            states = db.query(State).all()
            cache_info = {
                "total_states": len(states),
                "states": []
            }
            
            for state in states:
                state_info = {
                    "state_code": state.state_code,
                    "last_updated": state.last_updated.isoformat(),
                    "total_zip_codes": len(state.zip_codes),
                    "zip_codes": []
                }
                
                for zip_code in state.zip_codes:
                    zip_info = {
                        "zip_code": zip_code.zip_code,
                        "total_listings": len(zip_code.listings),
                        "sample_listing": zip_code.listings[0] if zip_code.listings else None
                    }
                    state_info["zip_codes"].append(zip_info)
                
                cache_info["states"].append(state_info)
            
            return cache_info
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error fetching cache information: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cache-info/state/{state}")
async def get_state_cache_info(state: str) -> Dict:
    """
    Get detailed information about cached data for a specific state.
    Returns information about the state and its zip codes.
    """
    try:
        logger.info(f"Fetching cache information for state: {state}")
        db = next(get_db())
        try:
            state_data = db.query(State).filter(State.state_code == state.upper()).first()
            if not state_data:
                raise HTTPException(status_code=404, detail=f"No cached data found for state {state}")
            
            state_info = {
                "state_code": state_data.state_code,
                "last_updated": state_data.last_updated.isoformat(),
                "total_zip_codes": len(state_data.zip_codes),
                "zip_codes": []
            }
            
            for zip_code in state_data.zip_codes:
                zip_info = {
                    "zip_code": zip_code.zip_code,
                    "total_listings": len(zip_code.listings),
                    "sample_listing": zip_code.listings[0] if zip_code.listings else None
                }
                state_info["zip_codes"].append(zip_info)
            
            return state_info
        finally:
            db.close()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching cache information for state {state}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 