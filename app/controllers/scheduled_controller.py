import json
import logging
from datetime import datetime
from typing import List


from app.config import local_session
from app.models import Scheduled


def create_scheduled(
    campaign_id: int,
    city: str,
    title_seo: str,
    meta_description: str,
    state: str,
    key_phrase: str,
    url: str,
    total_reviews: int,
    blocks: List[str],
    date: str,
) -> bool:
    """
    Crea un Scheduled en la base de datos.

    Args:
        campaign_id: ID de la campaña asociada
        city: Ciudad objetivo
        title_seo: Título SEO para la página
        meta_description: Descripción para motores de búsqueda
        state: Estado/Provincia objetivo
        key_phrase: Frase clave programada
        url: URL completa del recurso
        total_reviews: Total de reseñas programadas
        date: Espera formato "YYYY-MM-DD" (como se procesa en process_data)
        blocks: Lista de strings con sufijo "_block" (ej: ["map_block", "faq_block"])
        session: Sesión de SQLAlchemy inyectada

    Returns:
        bool: True si éxito, False si falla (para manejo en massive_creation)
    """
    try:
        with local_session() as session:
            try:
                parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                logging.error(f"Formato de fecha inválido: {date}")
                return False

            # Crear registro
            new_scheduled = Scheduled(
                campaign_id=campaign_id,
                city=city,
                title_seo=title_seo,
                meta_description=meta_description,
                state=state,
                key_phrase=key_phrase,
                url=url,
                total_reviews=int(total_reviews),
                blocks=blocks,
                date=parsed_date,
            )

            session.add(new_scheduled)
            session.commit()
            return True

    except Exception as e:
        logging.error(f"Error al crear scheduled (ID {campaign_id}): {str(e)}")
        return False


def get_scheduled_campaigns() -> str:
    """
    Obtiene todas las campañas programadas de la base de datos en formato JSON.

    Consulta todos los registros de la tabla Scheduled y los retorna como una cadena JSON
    que contiene una lista de diccionarios con los datos de cada programación.

    Returns:
        str: Cadena JSON con la lista de programaciones. Cada elemento contiene:
            - id (int): Identificador único de la programación
            - campaign_id (int): ID de la campaña asociada
            - city (str): Ciudad objetivo
            - state (str): Estado/Provincia objetivo
            - key_phrase (str): Frase clave programada
            - date (str): Fecha de programación
            - total_reviews (int): Total de reseñas programadas
        Retorna una lista vacía (como JSON) en caso de error.

    Raises:
        Exception: Error durante la consulta a la base de datos (manejado internamente).
                  Se imprime el error en consola.
    """
    try:
        with local_session() as session:
            scheduled_objects = session.query(Scheduled).all()
            scheduled_list = []
            for schedule in scheduled_objects:
                scheduled_dict = {
                    "id": schedule.id,
                    "url": schedule.url,
                    "title_seo": schedule.title_seo,
                    "meta_description": schedule.meta_description,
                    "campaign_id": schedule.campaign_id,
                    "city": schedule.city,
                    "state": schedule.state,
                    "key_phrase": schedule.key_phrase,
                    "date": schedule.date.isoformat(),
                    "total_reviews": schedule.total_reviews,
                    "blocks": schedule.blocks,
                }
                scheduled_list.append(scheduled_dict)

            return json.dumps(scheduled_list)

    except Exception as e:
        print(f"Error al obtener las programaciones. Error: {e}")
        return json.dumps([])


def delete_scheduled_campaign(scheduled_id: int) -> dict:
    """
    Elimina una campaña programada de la base de datos según su ID.

    Busca y elimina un registro específico de la tabla Scheduled. Retorna un diccionario
    con mensajes sobre el resultado de la operación y códigos de estado HTTP.

    Args:
        scheduled_id (int): ID de la programación a eliminar

    Returns:
        dict: Diccionario con mensaje de resultado y código de estado:
            - {"message": str, "status": int}

    Raises:
        Exception: Error durante la operación de base de datos (manejado internamente).
                  Se imprime el error en consola.
    """
    try:
        with local_session() as session:
            scheduled = (
                session.query(Scheduled).filter(Scheduled.id == scheduled_id).first()
            )

            if scheduled is None:
                return {"message": "La programación no existe", "status": 404}

            session.delete(scheduled)
            session.commit()
            return {"message": "Programación eliminada correctamente", "status": 200}
    except Exception as e:
        print(f"Error al eliminar la programación. Error: {e}")
        return {"message": "Error al eliminar la programación", "status": 500}
