from fastapi import APIRouter, HTTPException, UploadFile, Request
import json
from pydantic import BaseModel
from typing import List

from app.controllers.campaign_controller import get_campaigns
from app.controllers.scheduled_controller import (
    get_scheduled_campaigns,
    deleted_scheduled_campaign,
    create_scheduled
)
from app.controllers import create_page
from app.utilities import process_excel, massive_creation
from app.utilities.utils import programming_hour, change_hour

router = APIRouter()


#  Modelo con 'services' incluido
class CampaignData(BaseModel):
    id: int
    city: str
    services: str  # nuevo campo
    title_seo: str
    meta_description: str
    state: str
    key_phrase: str
    url: str
    review: int
    blocks: List[str]


# Obtener campañas
@router.get("/campaigns")
async def campaigns():
    campaigns = get_campaigns()
    campaign_list = json.loads(campaigns)
    return campaign_list


#  Crear nueva campaña con campo 'services'
@router.post("/new_campaign")
def new_campaign(data: CampaignData):
    try:
        create_page(
            data.id,
            data.city,
            data.services,  # incluido aquí
            data.title_seo,
            data.meta_description,
            data.state,
            data.key_phrase,
            int(data.review),
            data.blocks,
            data.url,
        )
        return {"message": "Página creada"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener programaciones
@router.get("/scheduled")
async def scheduled():
    scheduled = get_scheduled_campaigns()
    scheduled_list = json.loads(scheduled)
    return scheduled_list


# Eliminar una programación
@router.delete("/delete_scheduled/{scheduled_id}")
async def delete_scheduled(scheduled_id: int):
    try:
        result = deleted_scheduled_campaign(scheduled_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#  Subir archivo Excel que ya incluye 'services'
@router.post("/upload_excel")
async def upload_json(file: UploadFile):
    try:
        data = process_excel(file)
        success_ids = massive_creation(data, create_scheduled)

        return {
            "success": "success",
            "processed": f"Registros creados exitosamente: {len(success_ids)}",
            "error_log": "static/error_log.txt"
            if len(success_ids) != len(data)
            else None,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}",
        )


# Consultar hora programada actual
@router.get("/get_programmed_hour")
async def get_programmed_hour():
    try:
        return programming_hour
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}",
        )


# Cambiar hora programada
@router.post("/program_hour")
async def program_hour(request: Request):
    try:
        body = await request.json()
        new_hour = body["programming_hour"]
        change_hour(new_hour)
        return {"message": "Hora programada"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}",
        )
