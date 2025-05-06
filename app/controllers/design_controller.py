from app.config import local_session
from app.models import DesignElement
import json
from sqlalchemy.exc import NoResultFound


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
    city: str,
    title_seo: str,
    meta_description: str,
    state: str,
    campaign: str,
    key_phrase: str,
    url: str,
    reviews: int,
    blocks: dict,
) -> str:
    try:
        with local_session() as session:
            design = (
                session.query(DesignElement).filter_by(campaign_id=campaign_id).first()
            )
            if design:
                design_data = {
                    "id": design.id,
                    "service": design.service,
                    "number": design.number,
                    "language": design.language,
                    "layout": design.layout,
                    "address": design.address,
                    "country": design.country,
                    "url": url,
                    "reviews": reviews,
                    "blocks": blocks,
                    "campaign": campaign,
                    "city": city,
                    "title_seo": title_seo,
                    "meta_description": meta_description,
                    "state": state,
                    "key_phrase": key_phrase,
                    "alt_name": design.alt_name,
                    "local_city": design.local_city,
                    "local_state": design.local_state,
                    "postal_code": design.postal_code,
                    "wizard": design.wizard,
                    "meta": design.meta,
                    "channel_id": design.channel_id,
                }
                return json.dumps(design_data)
            else:
                return json.dumps([]), 404
    except NoResultFound:
        print("Error al obtener el elemento de diseño")
        return json.dumps([]), 404
    except Exception as e:
        print(f"Error al obtener el elemento de diseño: {e}")
        return json.dumps([]), 500
