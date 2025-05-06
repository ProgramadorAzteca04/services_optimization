"""
Modulo de modelo servicio de campaña
Este modullo define la clase [Campaign_services] que representa una campaña de la base de datos.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Services(Base):
      """Clase que representa una servicios por campaña en la base de datos.
       Atributos:
       -id (int): ID del servicio.
       -campaign_id (int): ID de la campaña ForeignKey("campaigns.id").
       -services_name (String): Nombre del servicio.
      -services_slug (String): Nombre del servicio en formato slug.      
       Relaciones:
       - campaign (Campaign): Elementos de diseño asociados a la campaña.
       Métodos:
       __init__(self, name, state): Inicializa una nueva instancia de la clase Campaign.
       """
      
      __tablename__ = "services"
      id = Column(Integer, primary_key=True)
      campaign_id = Column(Integer, ForeignKey("campaigns.id"))
      services_name = Column(String(), nullable=False)
      services_slug = Column(String(), nullable=False)

      campaign = relationship("Campaign", back_populates="services")
      def __init__(self, campaign_id, services_name, services_slug):
              self.campaign_id = campaign_id
              self.services_name = services_name
              self.services_slug = services_slug
      