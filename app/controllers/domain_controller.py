from app.config import local_session
from app.models import Campaign, Domain

# =======================================
# Controlador de Dominio
# - Consultar el dominio asociado a una campaña (por nombre)
# =======================================

def get_domain(campaign_name: str) -> str | None:
    """
    Retrieves the domain associated with a specific campaign name.

    This function looks up the campaign by its name in the database, then fetches
    the domain record linked to its campaign_id. Returns the domain as a string
    if found, otherwise returns None.

    Args:
        campaign_name (str): The name of the campaign to search.

    Returns:
        str | None: The domain string if found, or None if not found or error.

    Raises:
        Exception: Caught and logged internally if database access fails.
    """
    try:
        with local_session() as session:
            # Buscar la campaña por su nombre
            campaign = session.query(Campaign).filter_by(name=campaign_name).first()
            if campaign:
                # Buscar el dominio asociado al ID de la campaña
                domain_info = session.query(Domain).filter_by(campaign_id=campaign.id).first()
                if domain_info:
                    return domain_info.domain
                else:
                    print(f"No se encontró dominio asociado a la campaña: {campaign_name}")
            else:
                print(f"No se encontró la campaña con nombre: {campaign_name}")
        return None
    except Exception as e:
        print(f"Error al obtener el dominio de la campaña '{campaign_name}': {e}")
        return None
