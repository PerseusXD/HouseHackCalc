from typing import Dict, List
import aiohttp
import logging
import certifi
import ssl
import json
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from ..models.base import Message
from ..models.listing import Listing as ListingModel
from ..database import State, ZipCode, get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListingService:
    
    api_key = "bba1a028708c4b5db83118c519386e4f"
    rent_cast_base_url = "https://api.rentcast.io/v1"
    CACHE_EXPIRATION = timedelta(days=30)  # Cache for 30 days since we have monthly quota

    @staticmethod
    def _is_cache_valid(last_updated: datetime) -> bool:
        """Check if the cached data is still valid."""
        # Ensure last_updated is timezone-aware
        if last_updated.tzinfo is None:
            last_updated = last_updated.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) - last_updated < ListingService.CACHE_EXPIRATION

    @staticmethod
    def _filter_listing_data(listing: Dict) -> Dict:
        """Extract only the required fields from a listing."""
        return {
            "formattedAddress": listing.get("formattedAddress"),
            "city": listing.get("city"),
            "state": listing.get("state"),
            "zipCode": listing.get("zipCode"),
            "price": listing.get("price"),
            "bedrooms": listing.get("bedrooms"),
            "bathrooms": listing.get("bathrooms"),
            "squareFootage": listing.get("squareFootage")
        }

    @staticmethod
    def _organize_listings_by_zip(listings: List[Dict]) -> Dict[str, List[Dict]]:
        """Organize listings by zip code."""
        zip_listings = {}
        for listing in listings:
            zip_code = listing.get("zipCode")
            if zip_code:
                if zip_code not in zip_listings:
                    zip_listings[zip_code] = []
                zip_listings[zip_code].append(listing)
        return zip_listings

    @staticmethod
    async def get_listings_by_state(state: str) -> Dict[str, List[Dict]]:
        """Fetch all listings for a state and cache them by zip code."""
        state = state.upper()
        
        # Get database session
        db = next(get_db())
        
        try:
            # Check if we have valid cached data for the state
            state_data = db.query(State).filter(
                State.state_code == state
            ).first()
            
            if state_data and ListingService._is_cache_valid(state_data.last_updated):
                logger.info(f"Returning cached data for state {state}")
                # Return all listings organized by zip code
                return {
                    zip_data.zip_code: zip_data.listings
                    for zip_data in state_data.zip_codes
                }
            
            # If no valid cache, make API call
            headers = {
                'Accept': 'application/json',
                'X-Api-Key': ListingService.api_key
            }
            
            url = f"{ListingService.rent_cast_base_url}/listings/sale?state={state}&limit=500"
            logger.info(f"Making request to RentCast API: {url}")
            
            # Create SSL context with certifi certificates
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=connector) as session:
                logger.info("Created aiohttp session")
                async with session.get(url, headers=headers) as response:
                    logger.info(f"Received response with status: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Successfully retrieved {len(data) if isinstance(data, list) else 0} listings")
                        
                        # Filter and transform the data
                        filtered_listings = [
                            ListingService._filter_listing_data(listing)
                            for listing in data
                        ]
                        
                        # Organize listings by zip code
                        zip_listings = ListingService._organize_listings_by_zip(filtered_listings)
                        
                        # Store in database
                        if state_data:
                            # Clear existing zip codes
                            state_data.zip_codes = []
                        else:
                            state_data = State(
                                state_code=state,
                                last_updated=datetime.now(timezone.utc)
                            )
                            db.add(state_data)
                        
                        # Add zip code data
                        for zip_code, listings in zip_listings.items():
                            zip_data = ZipCode(
                                zip_code=zip_code,
                                listings=listings,
                                state=state_data
                            )
                            db.add(zip_data)
                        
                        # Commit changes to database
                        db.commit()
                        return zip_listings
                        
                    elif response.status == 401:
                        logger.error("Invalid API key")
                        raise Exception("Invalid API key. Please check your RentCast API key.")
                    elif response.status == 403:
                        logger.error("Access forbidden")
                        raise Exception("Access forbidden. Please check your API key permissions.")
                    elif response.status == 404:
                        logger.error(f"No listings found for state {state}")
                        raise Exception(f"No listings found for state {state}")
                    elif response.status == 429:
                        logger.error("Rate limit exceeded")
                        raise Exception("Rate limit exceeded. Please try again later.")
                    else:
                        error_text = await response.text()
                        logger.error(f"API error: Status {response.status}, Response: {error_text}")
                        raise Exception(f"RentCast API error (Status {response.status}): {error_text}")
        except aiohttp.ClientError as e:
            logger.error(f"Network error: {str(e)}")
            raise Exception(f"Network error while connecting to RentCast API: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise Exception(f"Unexpected error: {str(e)}")
        finally:
            db.close() 