from fastapi import APIRouter, Depends, HTTPException, status

from api.ai_model.models import UrlRequest

router = APIRouter()
