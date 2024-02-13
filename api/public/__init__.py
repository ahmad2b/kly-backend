from fastapi import APIRouter, Depends
from api.public.url import views as url

api = APIRouter()

api.include_router(
    url.router,
    prefix="/api/v2/url",
    tags=["URL"],
    # dependencies=[Depends(authent)],
)
