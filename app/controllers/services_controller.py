# app/controllers/service_controller.py

from app.models.services import Services
from app.config.database_config import local_session

# Obtener todos los servicios
def get_all_services():
    session = local_session()
    try:
        services = session.query(Services).all()
        return {
            "success": True,
            "data": [s.to_dict() for s in services]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        session.close()

# Obtener servicios por campaña
def get_services_by_campaign(campaign_id : int):
    session = local_session()
    try:
        services = session.query(Services).filter(Services.campaign_id == campaign_id).all()
        return {
            "success": True,
            "data": [s.to_dict() for s in services]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        session.close()

# Crear nuevo servicio
def create_service(data):
    session = local_session()
    try:
        new_service = Services(
            name=data.get("name"),
            campaign_id=data.get("campaign_id")
        )
        session.add(new_service)
        session.commit()
        return {
            "success": True,
            "message": "✅ Servicio creado exitosamente",
            "service": new_service.to_dict()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        session.close()

# Eliminar un servicio
def delete_service(service_id):
    session = local_session()
    try:
        service = session.query(Services).get(service_id)
        if service:
            session.delete(service)
            session.commit()
            return {
                "success": True,
                "message": f"🗑️ Servicio con ID {service_id} eliminado exitosamente"
            }
        return {
            "success": False,
            "message": f"⚠️ Servicio con ID {service_id} no encontrado"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
    finally:
        session.close()

print(get_services_by_campaign(1))
