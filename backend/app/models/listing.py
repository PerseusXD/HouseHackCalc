from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class HOA(BaseModel):
    fee: float

class Agent(BaseModel):
    name: str
    phone: str
    email: str
    website: str

class Office(BaseModel):
    name: str
    phone: str
    email: str
    website: str

class HistoryEvent(BaseModel):
    event: str
    price: float
    listingType: str
    listedDate: datetime
    removedDate: Optional[datetime] = None
    daysOnMarket: int

class Listing(BaseModel):
    id: str
    formattedAddress: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: str
    zipCode: str
    county: str
    latitude: float
    longitude: float
    propertyType: str
    bedrooms: int
    bathrooms: float
    squareFootage: int
    lotSize: int
    yearBuilt: int
    hoa: Optional[HOA] = None
    status: str
    price: float
    listingType: str
    listedDate: datetime
    removedDate: Optional[datetime] = None
    createdDate: datetime
    lastSeenDate: datetime
    daysOnMarket: int
    mlsName: str
    mlsNumber: str
    listingAgent: Agent
    listingOffice: Office
    history: Dict[str, HistoryEvent] 