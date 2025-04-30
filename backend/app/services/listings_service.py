from typing import Dict, List
import aiohttp
import logging
import certifi
import ssl
from ..models.base import Message
from ..models.listing import Listing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListingService:
    
    api_key = "bba1a028708c4b5db83118c519386e4f"
    rent_cast_base_url = "https://api.rentcast.io/v1"

    @staticmethod
    async def get_listings(zip_code: str) -> Dict:
        # Validate zip code
        if not zip_code.isdigit() or len(zip_code) != 5:
            raise ValueError("Zip code must be a 5-digit number")
        
        headers = {
            'Accept': 'application/json',
            'X-Api-Key': ListingService.api_key
        }
        
        url = f"{ListingService.rent_cast_base_url}/listings/sale?zipCode={zip_code}"
        logger.info(f"Making request to RentCast API: {url}")
        
        # Create SSL context with certifi certificates
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        try:
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=connector) as session:
                logger.info("Created aiohttp session")
                async with session.get(url, headers=headers) as response:
                    logger.info(f"Received response with status: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Successfully retrieved {len(data) if isinstance(data, list) else 0} listings")
                        return data
                    elif response.status == 401:
                        logger.error("Invalid API key")
                        raise Exception("Invalid API key. Please check your RentCast API key.")
                    elif response.status == 403:
                        logger.error("Access forbidden")
                        raise Exception("Access forbidden. Please check your API key permissions.")
                    elif response.status == 404:
                        logger.error(f"No listings found for zip code {zip_code}")
                        raise Exception(f"No listings found for zip code {zip_code}")
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