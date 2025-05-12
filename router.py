import json
import os
from typing import List
from app.controllers import create_page
from fastapi import APIRouter, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse
from app import CampaignData 
from pydantic import BaseModel


from app.controllers.campaign_controller import get_campaigns
from app.controllers.services_controller import get_services_by_campaign
from app.controllers.scheduled_controller import (
    create_scheduled,
    delete_scheduled_campaign,
    get_scheduled_campaigns,
)
from typing import List
from app.utilities import massive_creation, process_excel
from app.utilities.utils import change_hour, programming_hour

router = APIRouter()


class BotExecutionData(BaseModel):
    campaign_id: int
    title_seo: str
    meta_description: str
    key_phrase: str
    url: str
    review: int
    blocks: List[str]


### CAMPAÑAS ###
@router.get("/{campaign_id}")
async def campaigns():
    campaigns = get_campaigns()
    campaign_list = json.loads(campaigns)
    return campaign_list


@router.post("/services/")
def run_bot(data: BotExecutionData):
    try:
        from app.controllers.page_controller import create_page

        result =  create_page(
            data.campaign_id,
            data.title_seo,
            data.meta_description,
            data.key_phrase,
            data.review,
            data.blocks,
            data.url,
        )

        return {
            "status": "ok",
            "message": f"Bot ejecutado correctamente para campaña {data.campaign_id}",
            "result": result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar el bot: {str(e)}")

### PROGRAMACIONES ###
@router.get("/scheduled")
async def scheduled():
    scheduled = get_scheduled_campaigns()
    scheduled_list = json.loads(scheduled)
    return scheduled_list


@router.delete("/delete_scheduled/{scheduled_id}")
async def delete_scheduled(scheduled_id: int):
    try:
        result = delete_scheduled_campaign(scheduled_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@router.get("/get_programmed_hour")
async def get_programmed_hour():
    try:
        return programming_hour
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}",
        )


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


@router.get("/download_report/")
async def download_report():
    ruta = os.path.join("static", "report.xlsx")
    return FileResponse(ruta, filename="report.xlsx")


@router.post("/services")
def new_campaign(data: CampaignData):
    try:
        print("📥 Datos recibidos:", data)

        result = create_page(
            data.id,
            data.campaign_id,
            data.title_seo,
            data.meta_description,
            data.key_phrase,
            int(data.review),
            data.blocks,
            data.url,
        )
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}",
        )
