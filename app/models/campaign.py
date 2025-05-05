"""
Modulo de modelo campaña
Este modullo define la clase [Campaign] que representa una campaña de la base de datos.
"""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Campaign(Base):
      """Clase que representa una campaña en la base de datos.
       Atributos:
      - id (int): ID de la campaña.
      - name (String): Nombre de la campaña.
      -state (String): Estado de la campaña.

      Relaciones:
      - design_elements (DesignElement): Elementos de diseño asociados a la campaña.
      - domains (Domain): Dominios asociados a la campaña.
      - sheduled (Scheduled): Programaciones asociadas a la campaña.
      Métodos:
      __init__(self, name, state): Inicializa una nueva instancia de la clase Campaign.
      """

      #Attributes:
      __tablename__ = "campaigns"

      id - Column(Integer, primary_key=True)
      name = Column(String(), nullable=False)
      state = Column(Boolean, nullable=False)

      design_elements = relationship("DesignElement", back_populates="campaign")
      domains = relationship("Domain", back_populates="campaign")
      scheduled = relationship("Scheduled", back_populates="campaign")
      indexing = relationship("Indexing", back_populates="campaign")
      credentials = relationship("Credentials", back_populates="campaign")
      campaign_services = relationship("ServicesCampaign", back_populates="campaign")

      def __init__(self, name, state):
              self.name = name
              self.state = state
      """
      Contructor de la clase:

      Args:
          name (str): Nombre de la campaña.
          state (str): Estado de la campaña.
      
      """