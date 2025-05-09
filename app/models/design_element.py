"""
Modelo de modelos de elementos de diseño
Este modullo define la clase [DesignElement] que representa un elemento de diseño de la base de datos.
"""

from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class DesignElement(Base):
      """
        Clase que representa un elemento de diseño en la base de datos.

    Atributos:
        id (Integer): Identificador único del elemento de diseño.
        campaign_id (Integer): Identificador de la campaña asociada.
        service (String): Servicio asociado al elemento de diseño.
        number (String): Número asociado al elemento de diseño.
        language (String): Idioma asociado al elemento de diseño.
        layout (String): Diseño asociado al elemento de diseño.
        address (String): Dirección asociada al elemento de diseño.
        country (String): País asociado al elemento de diseño.
        url (String): URL asociada al elemento de diseño.
        alt_name (String): Nombre alternativo asociado al elemento de diseño.
        local_city (String): Ciudad local asociada al elemento de diseño.
        local_state (String): Estado local asociado al elemento de diseño.
        postal_code (String): Código postal asociado al elemento de diseño.
        wizard (String): Asistente asociado al elemento de diseño.
        meta (String): Metadatos asociados al elemento de diseño.
        channel_id (String): Identificador del canal asociado.

    Relaciones:
        campaign (Campaign): Campaña asociada al elemento de diseño.

    Métodos:
        __init__(campaign_id, service, number, language, layout, address, country, url, alt_name, local_city, local_state, postal_code, wizard, meta, channel_id): Constructor de la clase.
      """

      __tablename__ = "design_elements"

      # Atributos:
      id = Column(Integer, primary_key=True, index=True)
      campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
      name = Column(String(), nullable=False)
      service = Column(String(), nullable=False)
      number = Column(String(), nullable=False)
      language = Column(String(), nullable=False)
      layout = Column(String(), nullable=False)
      address = Column(String(), nullable=False)
      country = Column(String(), nullable=False)
      url = Column(String(), nullable=False)
      alt_name = Column(String(), nullable=False)
      local_city = Column(String(), nullable=False)
      local_state = Column(String(), nullable=False)
      postal_code = Column(String(), nullable=False)
      wizard = Column(String(), nullable=False)
      meta = Column(String(), nullable=False)
      channel_id = Column(String(), nullable=False)

      # Relaciones:
      campaign = relationship("Campaign", back_populates="design_elements")

      def __init__(self, campaign_id, service, number, language, layout, address, country, url, alt_name, local_city, local_state, postal_code, wizard, meta, channel_id):
            self.campaign_id = campaign_id
            self.service = service
            self.number = number
            self.language = language
            self.layout = layout
            self.address = address
            self.country = country
            self.url = url
            self.alt_name = alt_name
            self.local_city = local_city
            self.local_state = local_state
            self.postal_code = postal_code
            self.wizard = wizard
            self.meta = meta
            self.channel_id = channel_id
