"""
Módulo de modelos de indexación

Este módulo define la clase [Indexing] que representa un registro de indexación en la base de datos.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Indexing(Base):
    """
    Clase que representa un registro de indexación en la base de datos.

    Atributos:
        id (Integer): Identificador único del registro.
        campaign_id (Integer): ID de la campaña asociada.
        credential_id (Integer): ID de las credenciales utilizadas.
        link_page (String): Enlace de la página indexada.

    Relaciones:
        campaign (Campaign): Relación con la campaña.
        credential (Credential): Relación con la credencial.

    Métodos:
        __init__(campaign_id, credential_id, link_page): Constructor de la clase.
    """

    __tablename__ = "indexing"

    # Atributos
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    credential_id = Column(Integer, ForeignKey("credentials.id"), nullable=False)
    link_page = Column(String, nullable=True)

    # Relaciones
    campaign = relationship("Campaign", back_populates="indexings")
    credential = relationship("Credential", back_populates="indexings")

    def __init__(self, campaign_id, credential_id, link_page):
        """
        Constructor de la clase.

        Args:
            campaign_id (Integer): ID de la campaña asociada.
            credential_id (Integer): ID de la credencial utilizada.
            link_page (String): URL de la página indexada.
        """
        self.campaign_id = campaign_id
        self.credential_id = credential_id
        self.link_page = link_page
