# HouseHackCalc

A real estate investment calculator that helps you analyze potential properties and calculate returns.

## Features

- Fetch real estate listings from RentCast API
- Cache listings data to optimize API usage
- Calculate potential returns on properties
- Compare different investment scenarios

## API Endpoints

### Listings

#### Get Listings by State
```bash
GET /state/{state}
```
Fetches all listings for a state and caches them by zip code.

**Response Format:**
```json
{
  "22003": [
    {
      "formattedAddress": "123 Main St",
      "city": "Annandale",
      "state": "VA",
      "zipCode": "22003",
      "price": 500000
    },
    // ... more listings
  ],
  "22042": [
    // ... listings for this zip code
  ]
}
```

#### View Cache Information
```bash
GET /cache-info
```
Shows information about all cached states and their zip codes.

**Response Format:**
```json
{
  "total_states": 2,
  "states": [
    {
      "state_code": "VA",
      "last_updated": "2024-03-20T10:30:00Z",
      "total_zip_codes": 3,
      "zip_codes": [
        {
          "zip_code": "22003",
          "total_listings": 25,
          "sample_listing": {
            "formattedAddress": "123 Main St",
            "city": "Annandale",
            "state": "VA",
            "zipCode": "22003",
            "price": 500000
          }
        }
        // ... other zip codes
      ]
    }
    // ... other states
  ]
}
```

#### View State Cache Information
```bash
GET /cache-info/state/{state}
```
Shows detailed information about a specific state's cached data.

**Response Format:**
```json
{
  "state_code": "VA",
  "last_updated": "2024-03-20T10:30:00Z",
  "total_zip_codes": 3,
  "zip_codes": [
    {
      "zip_code": "22003",
      "total_listings": 25,
      "sample_listing": {
        "formattedAddress": "123 Main St",
        "city": "Annandale",
        "state": "VA",
        "zipCode": "22003",
        "price": 500000
      }
    }
    // ... other zip codes
  ]
}
```

## Data Caching

The application implements a caching system to optimize API usage:

- Data is cached at the state level
- Cache expires after 30 days
- Listings are organized by zip code within each state
- Cache information can be viewed through the `/cache-info` endpoints

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 400: Invalid input (e.g., invalid state code)
- 404: Resource not found (e.g., no cached data for state)
- 500: Server error

## Development

### Prerequisites

- Python 3.8+
- Poetry for dependency management

### Setup

1. Install dependencies:
```bash
poetry install
```

2. Run the development server:
```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

### Database Management

To clear the database and start fresh:
```bash
poetry run python clear_db.py 