import json
import logging
from datetime import datetime
from typing import List
from app.config import local_session
from app.models.scheduled import Scheduled

def create_scheduled(
         campaign_id: int,
         services: str,
         city: str,
         title_seo: str,
         meta_description: str,
         state: str,
         key_phrase: str,
         url: str,
         date: str,
         total_reviews: int,
         blocks: List
      
) -> bool:
      
      """
      Crea una programación en la base de datos.

      Args:
          campaign_id (int): ID de la campaña.
          services (str): Servicios asociados a la Campaña.
          city (str): Ciudad asociada a la programación.
          title_seo (str): Título SEO para la página.
          meta_description (str): Descripción para motores de búsqueda.
          state (str): Estado de la programación.
          key_phrase (str): Frase clave asociada a la programación.
          url (str): URL completa del recurso.
          date (str): Fecha y hora de la programación.
          total_reviews (int): Total de resenas asociadas a la programación.

      Returns:
          bool: Indica si la operación fue exitosa. False si ocurre un error.

      """

      try:
            with local_session() as session:
                  try:
                     parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
                  except ValueError:
                     logging.error(f"Formato de fecha incorrecto: {date}")
                     return False

                  #Creat un Regsitro - Servicioo incoporado
                  new_scheduled = Scheduled.Scheduled(
                        campaign_id=campaign_id,
                        services=services,
                        city=city,
                        title_seo=title_seo,
                        meta_description=meta_description,
                        state=state,
                        key_phrase=key_phrase,
                        url=url,
                        date=parsed_date,
                        total_reviews=total_reviews,
                        blocks=blocks
                  )
                  session.add(new_scheduled)
                  session.commit()
                  return True

      except Exception as e:
            logging.error(f"Error al crear la programación: (ID {campaign_id}): {str(e)}")
            return False
      
def update_scheduled_time(scheduled_id: int, new_hour: str) -> dict:
    """
    Actualiza solo la hora de un registro Scheduled, conservando la misma fecha.

    Args:
        scheduled_id (int): ID de la programación a editar
        new_hour (str): Hora nueva en formato "HH:MM" (ej: "14:30")

    Returns:
        dict: {"message": str, "status": int}
    """
    try:
        with local_session() as session:
            scheduled = session.query(Scheduled).filter_by(id=scheduled_id).first()

            if scheduled is None:
                return {"message": "No se encontró la programación", "status": 404}

            # Combinar la fecha actual con la nueva hora
            try:
                hour_obj = datetime.strptime(new_hour, "%H:%M").time()
                updated_datetime = datetime.combine(scheduled.date.date(), hour_obj)
                scheduled.date = updated_datetime
            except ValueError:
                return {"message": "Formato de hora inválido. Usa HH:MM", "status": 400}

            session.commit()
            return {"message": "Hora actualizada correctamente", "status": 200}

    except Exception as e:
        print(f"Error al actualizar hora. Error: {e}")
        return {"message": "Error interno al actualizar", "status": 500}

      
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
               for scheduled_object in scheduled_objects:
                    
                    scheduled_dict = (
                         {
                              "id": scheduled_object.id,
                              "services": scheduled_object.services,
                              "campaign_id": scheduled_object.campaign_id,
                              "city": scheduled_object.city,
                              "state": scheduled_object.state,
                              "key_phrase": scheduled_object.key_phrase,
                              "date": scheduled_object.date,
                              "total_reviews": scheduled_object.total_reviews,
                         }
                    )
                    scheduled_list.append(scheduled_dict)
               return json.dumps(scheduled_list)
          
     except Exception as e:
          logging.error(f"Error al obtener las programaciones: {str(e)}")
          return json.dumps([])
      
def deleted_scheduled_campaign(scheduled_id: int) -> bool:
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
            with local_session as session:
                 scheduled = (
                      session.query(Scheduled).filter(Scheduled.id == scheduled_id).first()
                  )
                 
                 if scheduled is None:
                      return {"message": "Programación no encontrada", "status": 404}

                 session.delete(Scheduled)
                 session.commit()
                 return {"message": "Programación eliminada", "status": 200}
      except Exception as e:
           print(f"Error al eliminar la programacion. Error: {str(e)}")
           return {"message": f"Error al eliminar la programacion. Error: {str(e)}", "status": 500}