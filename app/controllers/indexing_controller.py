import os
from app.config import local_session
from dotenv import load_dotenv
from app.models import Indexing, Credential

# Cargar .env y crear conexión
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def indexing_controller(campaign_id: int, link_page: str):
    try:
        with local_session() as session:
            cred = session.query(Credential).filter_by(campaign_id=campaign_id).first()

            if not cred:
                print(f" No se encontró credential_id para campaign_id {campaign_id}")
                return

            print(f" Se encontró credential_id: {cred.id}")

            exists = session.query(Indexing).filter_by(
                campaign_id=campaign_id,
                credential_id=cred.id,
                link_page=link_page
            ).first()

            if exists:
                print(f" Ya existe un registro en indexing para esta URL con campaña {campaign_id} y credencial {cred.id}")
                return

            new_index = Indexing(
                campaign_id=campaign_id,
                credential_id=cred.id,
                link_page=link_page
            )

            session.add(new_index)
            session.commit()
            print(f" Registro insertado en indexing para campaña {campaign_id}")

    except Exception as e:
        print(f" Error en indexing_controller: {e}")
        session.rollback()

