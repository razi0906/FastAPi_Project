# importing modules
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, Float, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from geopy.distance import geodesic

# setting database
DATABASE_URL = "sqlite:///./test.db"

# creating sqlAlchemy model
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#creating pydantic model for validation
class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    description = Column(String)

# creating tables in database
Base.metadata.create_all(bind=engine)

# creating FASTAPI instance
app = FastAPI()

class AddressCreate(BaseModel):
    latitude: float
    longitude: float
    description: str

class AddressResponse(AddressCreate):
    id: int

#API route to create an address
@app.post("/addresses/", response_model=AddressResponse)
def create_address(address: AddressCreate):
    db_address = Address(**address.dict())
    db = SessionLocal()
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    db.close()
    return db_address


#API route to update an address
@app.put("/addresses/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, address: AddressCreate):
    db = SessionLocal()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address:
        for key, value in address.dict().items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    else:
        raise HTTPException(status_code=404, detail="Address not found")
    db.close()
    return db_address



#API route to delete address
@app.delete("/addresses/{address_id}", response_model=AddressResponse)
def delete_address(address_id: int):
    db = SessionLocal()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Address not found")
    db.close()
    return db_address

#API route to fetch address
@app.get("/addresses/", response_model=List[AddressResponse])
def get_addresses(
    latitude: float = Query(..., description="Latitude of the center point"),
    longitude: float = Query(..., description="Longitude of the center point"),
    distance: Optional[float] = Query(10, description="Search radius in kilometers"),
):
    db = SessionLocal()
    center_point = (latitude, longitude)
    addresses = db.query(Address).all()
    db.close()

    #function to find nearest address to a coordinate
    def within_distance(address):
        point = (address.latitude, address.longitude)
        return geodesic(center_point, point).kilometers <= distance

    return [address for address in addresses if within_distance(address)]
