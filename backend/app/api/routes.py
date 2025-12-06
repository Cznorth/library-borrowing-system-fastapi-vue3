from fastapi import APIRouter
from .v1 import auth, users, books, admin_users, copies, loans, reservations, fines


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(copies.router, prefix="/copies", tags=["copies"])
api_router.include_router(loans.router, prefix="/loans", tags=["loans"])
api_router.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
api_router.include_router(fines.router, prefix="/fines", tags=["fines"])
api_router.include_router(admin_users.router, prefix="/admin/users", tags=["admin-users"])

