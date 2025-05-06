"""
Módulo de modelos de campaña

Este módulo define la clase [Campaign] que representa una campaña en la base de datos.
"""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Campaign(Base):
    """
    Clase que representa una campaña en la base de datos.

    Atributos:
        id (Integer): Identificador único de la campaña.
        name (String): Nombre de la campaña.
        state (Boolean): Estado de la campaña.

    Relaciones:
        design_elements (DesignElement): Elementos de diseño asociados a la campaña.
        domains (Domain): Dominios asociados a la campaña.
        scheduled (Scheduled): Programación asociada a la campaña.

    Métodos:
        __init__(name, state): Constructor de la clase.
    """

    __tablename__ = "campaigns"

    # Attributes
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    state = Column(Boolean, nullable=False)

    # Relationships
    design_elements = relationship("DesignElement", back_populates="campaign")
    domains = relationship("Domain", back_populates="campaign")
    scheduled = relationship("Scheduled", back_populates="campaign")
    indexings = relationship("Indexing", back_populates="campaign")
    credentials = relationship("Credential", back_populates="campaign")
    services = relationship("Services", back_populates="campaign")


    def __init__(self, name, state):
        """
        Constructor de la clase.

        Args:
            name (String): Nombre de la campaña.
            state (Boolean): Estado de la campaña.
        """
        self.name = name
        self.state = state
