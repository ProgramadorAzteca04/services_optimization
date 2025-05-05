"""
Módulo de modelos de dominios

Este módulo define la clase [Domain] que representa un dominio en la base de datos.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Domain(Base):
    """
    Clase que representa un dominio en la base de datos.

    Atributos:
        id (Integer): Identificador único del dominio.
        domain (String): Nombre del dominio.
        admin (String): Administrador del dominio.
        password (String): Contraseña del dominio.
        campaign_id (Integer): Identificador de la campaña asociada.

    Relaciones:
        campaign (Campaign): Campaña asociada al dominio.

    Métodos:
        __init__(domain, admin, password, campaign_id): Constructor de la clase.
    """

    __tablename__ = "domains"

    # Atributos
    id = Column(Integer, primary_key=True)
    domain = Column(String(255), nullable=False)
    admin = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)

    # Relaciones
    campaign = relationship("Campaign", back_populates="domains")

    def __init__(self, domain, admin, password, campaign_id):
        """
        Constructor de la clase.

        Args:
            domain (String): Nombre del dominio.
            admin (String): Administrador del dominio.
            password (String): Contraseña del dominio.
            campaign_id (Integer): Identificador de la campaña asociada.
        """
        self.domain = domain
        self.admin = admin
        self.password = password
        self.campaign_id = campaign_id
