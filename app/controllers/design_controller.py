from app.config import local_session
from app.models import DesignElement
import json
from app.controllers.services_controller import get_services_by_campaign
from urllib.parse import urlparse



def get_designs() -> list[DesignElement] | list:
    """
    Obtiene todos los elementos de diseño disponibles en la base de datos.

    Realiza una consulta para recuperar todos los registros de elementos de diseño (DesignElement).
    En caso de error, retorna una lista vacía.

    Returns:
        list[DesignElement] | list: Lista de objetos DesignElement si la consulta es exitosa,
        lista vacía si ocurre algún error.

    Raises:
        Exception: Error genérico durante la consulta a la base de datos (manejado internamente)
    """
    try:
        with local_session() as session:
            return session.query(DesignElement).all()
    except Exception as e:
        print(f"Error al obtener los elementos de diseño: {e}")
        return []



def get_design(
    campaign_id: int,
    title_seo: str,
    meta_description: str,
    key_phrase: str,
    url: str,
    reviews: int,
    blocks: list,
) -> str:
    try:
        # 🟡 1. Extraemos el slug desde la URL
        parsed_url = urlparse(url)
        slug = parsed_url.path.strip("/").split("/")[-1]

        # 🟡 2. Obtenemos los servicios de esa campaña
        service_response = get_services_by_campaign(campaign_id)

        # 🟡 3. Filtramos por slug
        service = None
        if service_response["success"]:
            for s in service_response["data"]:
                if s["services_slug"] == slug:
                    service = s
                    break

        if not service:
            print("⚠️ No se encontró un servicio con slug:", slug)
            return json.dumps({"error": f"Service con slug '{slug}' no encontrado en campaña {campaign_id}"})

        with local_session() as session:
            design = session.query(DesignElement).filter_by(campaign_id=campaign_id).first()

        if not design:
            return json.dumps({"error": "DesignElement no encontrado"})

        # 🟢 4. Usamos el servicio correcto
        design_data = {
            "campaign_id": design.campaign_id,
            "service": {
                "services_name": service["services_name"],
                "services_slug": service["services_slug"],
            },
            "number": design.number,
            "language": design.language,
            "layout": design.layout,
            "address": design.address,
            "country": design.country,
            "url": url,
            "reviews": reviews,
            "blocks": blocks,
            "title_seo": title_seo,
            "meta_description": meta_description,
            "key_phrase": key_phrase,
            "alt_name": design.alt_name,
            "local_city": design.local_city,
            "local_state": design.local_state,
            "postal_code": design.postal_code,
            "wizard": design.wizard,
            "meta": design.meta,
            "channel_id": design.channel_id,
        }

        print("✅ Servicio detectado:", service)
        print("✅ Elemento de diseño obtenido:", design_data)
        return json.dumps(design_data)

    except Exception as e:
        print(f"Error al obtener el elemento de diseño: {e}")
        return json.dumps({"error": f"Error interno: {str(e)}"})

