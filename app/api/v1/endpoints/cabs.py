from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.cab import Cab
from app.models.driver import Driver
from app.schemas.cab import CabCreate, CabUpdate, CabResponse
from app.core.exceptions import ResourceNotFoundException

router = APIRouter()

@router.post("/", response_model=CabResponse)
async def create_cab(
    cab_create: CabCreate,
    current_user: Driver = Depends(deps.get_current_driver),
    db: Session = Depends(deps.get_db)
):
    """Create a new cab"""
    # Check if driver already has a cab
    existing_cab = db.query(Cab).filter(Cab.driver_id == current_user.id).first()
    if existing_cab:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Driver already has a registered cab"
        )
    
    cab = Cab(**cab_create.dict(), driver_id=current_user.id)
    db.add(cab)
    db.commit()
    db.refresh(cab)
    return cab

@router.get("/me", response_model=CabResponse)
async def get_my_cab(
    current_user: Driver = Depends(deps.get_current_driver),
    db: Session = Depends(deps.get_db)
):
    """Get driver's cab details"""
    cab = db.query(Cab).filter(Cab.driver_id == current_user.id).first()
    if not cab:
        raise ResourceNotFoundException("No cab registered for this driver")
    return cab

@router.put("/me", response_model=CabResponse)
async def update_my_cab(
    cab_update: CabUpdate,
    current_user: Driver = Depends(deps.get_current_driver),
    db: Session = Depends(deps.get_db)
):
    """Update driver's cab details"""
    cab = db.query(Cab).filter(Cab.driver_id == current_user.id).first()
    if not cab:
        raise ResourceNotFoundException("No cab registered for this driver")
    
    for field, value in cab_update.dict(exclude_unset=True).items():
        setattr(cab, field, value)
    
    db.commit()
    db.refresh(cab)
    return cab

@router.delete("/me")
async def delete_my_cab(
    current_user: Driver = Depends(deps.get_current_driver),
    db: Session = Depends(deps.get_db)
):
    """Delete driver's cab registration"""
    cab = db.query(Cab).filter(Cab.driver_id == current_user.id).first()
    if not cab:
        raise ResourceNotFoundException("No cab registered for this driver")
    
    db.delete(cab)
    db.commit()
    return {"message": "Cab registration deleted successfully"}

@router.get("/{cab_id}", response_model=CabResponse)
async def get_cab(
    cab_id: int,
    current_user: Driver = Depends(deps.get_current_driver),
    db: Session = Depends(deps.get_db)
):
    """Get cab by ID"""
    cab = db.query(Cab).filter(Cab.id == cab_id).first()
    if not cab:
        raise ResourceNotFoundException(f"Cab with ID {cab_id} not found")
    return cab

@router.get("/", response_model=List[CabResponse])
async def get_cabs(
    skip: int = 0,
    limit: int = 100,
    current_user: Driver = Depends(deps.get_current_driver),
    db: Session = Depends(deps.get_db)
):
    """Get all cabs"""
    cabs = db.query(Cab).offset(skip).limit(limit).all()
    return cabs

@router.get("/me/bookings", response_model=List[dict])
async def get_cab_bookings(
    current_user: Driver = Depends(deps.get_current_driver),
    db: Session = Depends(deps.get_db)
):
    """Get bookings for driver's cab"""
    cab = db.query(Cab).filter(Cab.driver_id == current_user.id).first()
    if not cab:
        raise ResourceNotFoundException("No cab registered for this driver")
    return cab.bookings 