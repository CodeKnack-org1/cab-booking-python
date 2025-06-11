from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, drivers, cabs, bookings, payments, notifications, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(drivers.router, prefix="/drivers", tags=["drivers"])
api_router.include_router(cabs.router, prefix="/cabs", tags=["cabs"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"]) 