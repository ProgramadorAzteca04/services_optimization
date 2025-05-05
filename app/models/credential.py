"""

Modulo de modelo credenciales
Este modullo define la clase [Credentials] que representa una credencial de la base de datos.

"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from base import Base


class Credential(Base):
    """ "
    Clase que representa una credencial de acceso en la base de datos.
    Atributos:
    - id (int): ID de la credencial.
    -user (String): Nombre de usuario de la credencial.
    -password (String): Contraseña de la credencial.
    campaign_id (int): ID de la campaña ForeignKey("campaigns.id").
    indexing_id (int): ID de la indexacion ForeignKey("indexing.id").
    last_reset (Datetime): Fecha del ultimo reinicio del contador de indexaciones.

    Relaciones:
    - campaign (Campaign): Campaña asociada a la credencial.
    - indexing (Indexing): Indexacion asociada a la credencial.
    Métodos:
    __init__(self, user, password, campaign_id, last_reset): Inicializa una nueva instancia de la clase Credentials.
    """

    __tablename__ = "credentials"

    # Atributos:
    id = Column(Integer, primary_key=True)
    user = Column(String(), nullable=False)
    password = Column(String(), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    indexing_id = Column(Integer, ForeignKey("indexing.id"))
    last_reset = Column(DateTime, nullable=False)

    # Relaciones:
    campaign = relationship("Campaign", back_populates="credentials")
    indexing = relationship("Indexing", back_populates="credentials")

    def __init__(self, user, password, campaign_id, indexing_id, last_reset):
        """
        Constructor de la clase.

        Args:
            user (String): Usuario.
            password (String): Contraseña.
            campaign_id (Integer): ID de la campaña asociada.
            indexing_today (Integer): Cantidad de indexaciones realizadas hoy.
            last_reset (DateTime): Último reinicio del contador.
        """
        self.user = user
        self.password = password
        self.campaign_id = campaign_id
        self.indexing_id = indexing_id
        self.last_reset = last_reset
