import json
from sqlalchemy.exc import NoResultFound

from app.config import local_session
from app.models import Campaign

# =======================================
# Controlador de Campañas
# - Consultar todas las campañas
# - Consultar una campaña individual por ID
# =======================================

def get_campaigns() -> str:
    """
    Retrieves all campaigns from the database and returns them as a JSON string.

    Queries the database for all Campaign records, extracts the relevant fields
    (id, name, state), and formats them as a JSON array. Returns an empty array
    if any error occurs during the process.

    Returns:
        str: A JSON-formatted string containing a list of campaigns with their
             id, name, and state. Returns an empty JSON array on failure.
    """
    try:
        # Open a session and retrieve all campaign records
        with local_session() as session:
            campaigns = session.query(Campaign).all()
            campaign_list = []
            
            # Convert each Campaign object into a dict
            for campaign in campaigns:
                campaign_data = {
                    "id": campaign.id,
                    "name": campaign.name,
                    "state": campaign.state,
                }
                campaign_list.append(campaign_data)

            # Return JSON string of campaigns
            return json.dumps(campaign_list)

    except Exception as e:
        # Log error and return empty list
        print("Error al obtener las campañas:", e)
        return json.dumps([])


def get_campaign(id: int) -> Campaign | None:
    """
    Retrieves a specific campaign from the database by its ID.

    Attempts to find a Campaign record using the provided ID. If found, returns
    the Campaign object. If not found or an error occurs, returns None.

    Args:
        id (int): The unique identifier of the campaign to retrieve.

    Returns:
        Campaign | None: The Campaign object if found, otherwise None.
    """
    try:
        # Attempt to retrieve campaign by primary key
        with local_session() as session:
            return session.get(Campaign, id)

    except NoResultFound:
        # Handle specific case where no campaign was found
        print(f"No se encontró la campaña con el id: {id}")
        return None

    except Exception as e:
        # General error handling
        print(f"Error al obtener la campaña con el id: {id}", e)
        return None
