# Backend API Service

A FastAPI-based backend service that provides real estate listing data through integration with the RentCast API.

## Features

- Real-time property listings by zip code
- Integration with RentCast API
- RESTful API endpoints
- Async request handling
- Error handling and validation

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Run the development server:
```bash
poetry run uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Get Listings by Zip Code
```
GET /listings/{zip_code}
```

Parameters:
- `zip_code`: 5-digit US zip code

Response:
Returns the raw response from the RentCast API, which includes an array of listing objects with the following structure:
```json
[
  {
    "id": "string",
    "formattedAddress": "string",
    "addressLine1": "string",
    "addressLine2": "string",
    "city": "string",
    "state": "string",
    "zipCode": "string",
    "county": "string",
    "latitude": "number",
    "longitude": "number",
    "propertyType": "string",
    "bedrooms": "number",
    "bathrooms": "number",
    "squareFootage": "number",
    "lotSize": "number",
    "yearBuilt": "number",
    "hoa": {
      "fee": "number"
    },
    "status": "string",
    "price": "number",
    "listingType": "string",
    "listedDate": "string",
    "removedDate": "string",
    "createdDate": "string",
    "lastSeenDate": "string",
    "daysOnMarket": "number",
    "mlsName": "string",
    "mlsNumber": "string",
    "listingAgent": {
      "name": "string",
      "phone": "string",
      "email": "string",
      "website": "string"
    },
    "listingOffice": {
      "name": "string",
      "phone": "string",
      "email": "string",
      "website": "string"
    },
    "history": {
      "date": {
        "event": "string",
        "price": "number",
        "listingType": "string",
        "listedDate": "string",
        "removedDate": "string",
        "daysOnMarket": "number"
      }
    }
  }
]
```

## Development

- Python 3.12+
- FastAPI
- Poetry for dependency management
- aiohttp for async HTTP requests

## Environment Variables

The following environment variables are used:
- `RENTCAST_API_KEY`: Your RentCast API key

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 400: Invalid zip code format
- 500: Internal server error or API integration error 