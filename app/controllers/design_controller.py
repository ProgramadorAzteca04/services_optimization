from app.config import local_session
from app.models import DesignElement
import json
from sqlalchemy.exc import NoResultFound

# =======================================
# Controlador de Diseño
# - Consultar todos los elementos
# - Consultar un diseño específico por campaña
# =======================================

def get_designs() -> list[DesignElement] | list:
    """
    Retrieves all available design elements from the database.

    Queries the database for all DesignElement records. If the query fails or an
    exception occurs, returns an empty list.

    Returns:
        list[DesignElement] | list: A list of DesignElement objects if successful,
        or an empty list in case of failure.
    """
    try:
        # Get all design elements from the database
        with local_session() as session:
            return session.query(DesignElement).all()
    except Exception as e:
        print(f"Error al obtener los elementos de diseño: {e}")
        return []


def get_design(
    campaign_id: int,
    local_city: str,
    title_seo: str,
    meta_description: str,
    local_state: str,
    campaign: str,
    key_phrase: str,
    url: str,
    reviews: int,
    blocks: dict,
) -> str:
    """
    Retrieves a design element by campaign_id and returns a combined JSON.

    Combines data from the database (design_elements table) with additional
    context provided externally (like SEO metadata, reviews, and layout blocks).

    Args:
        campaign_id (int): ID of the associated campaign.
        local_city (str): Target city (external).
        title_seo (str): SEO title for the page (external).
        meta_description (str): SEO meta description (external).
        local_state (str): Target state (external).
        campaign (str): Campaign name (external).
        key_phrase (str): Main keyword (external).
        url (str): Final URL for the landing page (external).
        reviews (int): Number of reviews (external).
        blocks (dict): JSON of layout components (external).

    Returns:
        str: A JSON string combining DB data with provided context.
    """
    try:
        with local_session() as session:
            design = session.query(DesignElement).filter_by(campaign_id=campaign_id).first()

            if design:
                design_data = {
                    # Campos directos desde la base de datos
                    "id": design.id,
                    "campaign_id": design.campaign_id,
                    "service": design.service,
                    "number": design.number,
                    "language": design.language,
                    "layout": design.layout,
                    "address": design.address,
                    "country": design.country,
                    "alt_name": design.alt_name,
                    "local_city": design.local_city,
                    "local_state": design.local_state,
                    "postal_code": design.postal_code,
                    "wizard": design.wizard,
                    "meta": design.meta,
                    "channel_id": design.channel_id,
                    "url": design.url,  # Desde la BD, puedes sobrescribir si prefieres el externo

                    #  Campos externos que hacen parte de la Base de Datos
                    "reviews": reviews,
                    "blocks": blocks,
                    "campaign": campaign,
                    "title_seo": title_seo,
                    "meta_description": meta_description,
                    "key_phrase": key_phrase
                }
                return json.dumps(design_data)
            else:
                return json.dumps([]), 404

    except NoResultFound:
        print("No se encontró el diseño con la campaña indicada.")
        return json.dumps([]), 404

    except Exception as e:
        print(f"Error al obtener el diseño: {e}")
        return json.dumps([]), 500