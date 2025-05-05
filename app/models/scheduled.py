"""
Módulo de modelos de programaciones actualizado
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, String, JSON, Text
from sqlalchemy.orm import relationship
from .base import Base


class Scheduled(Base):
    """
    Clase actualizada que representa una programación en la base de datos.

    Nuevos campos:
        title_seo (str): Título SEO para la página
        meta_description (str): Descripción para motores de búsqueda
        url (str): URL completa del recurso
        blocks (list): Lista de bloques activos (almacenados como JSON)
    """

    __tablename__ = "scheduled"

    # Atributos
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    city = Column(String)
    title_seo = Column(String)
    meta_description = Column(Text)
    state = Column(String)
    key_phrase = Column(String)
    url = Column(String(512))
    date = Column(Date)
    total_reviews = Column(Integer)
    blocks = Column(JSON)

    # Relaciones
    campaign = relationship("Campaign", back_populates="scheduled")

    def __init__(
        self,
        campaign_id: int,
        city: str,
        title_seo: str,
        meta_description: str,
        state: str,
        key_phrase: str,
        url: str,
        date: str,
        total_reviews: int,
        blocks: list[str],
    ):
        """
        Constructor actualizado con nuevos campos.
        """
        self.campaign_id = campaign_id
        self.city = city
        self.title_seo = title_seo
        self.meta_description = meta_description
        self.state = state
        self.key_phrase = key_phrase
        self.url = url
        self.date = date
        self.total_reviews = total_reviews
        self.blocks = blocks
