from dotenv import load_dotenv
import os
from playwright.sync_api import Page
from app.utilities.wordpress_utilities import insert_wordpress_data, delete_template
from app.controllers.form_controller import perform_login
from app.components import InitLayout
# from app.api import GPT
#from app.controllers.indexing_controller import indexing_controller

load_dotenv()

API_URL = os.getenv("API_URL")
META_FOLDER = os.getenv("META_FOLDER")

class WordpressComponent:
    def __init__(self, page: Page, design_data: dict, service: dict = None):
        self.page = page
        self.design_data = design_data
        self.service = service
        # self.gpt = GPT(design_data)

    def dates_wordpress(
        self,
        reviews: int,
        url: str,
        init_layout: InitLayout,
        meta_description: str,
        id: int,
    ):
        print(f" Iniciando flujo para servicio: {self.service.get('name', 'Genérico') if self.service else 'Sin servicio'}")

        perform_login(
            self.page,
            self.design_data["campaign"],
            self.design_data["layout"],
            url,
            init_layout,
            self.design_data,
        )

        frase_clave = self.design_data["key_phrase"].replace(",", "")

        # Generar título SEO
        # title_seo = self.gpt.title_seo()
        title_seo = (
            f"{self.service['name']}"
            if self.service else
            self.design_data["campaign"]
        )

        insert_wordpress_data(
            self.page,
            frase_clave,
            meta_description,
            title_seo,
            reviews,
            service=self.service
        )

        # Borrar plantilla si hay service (slug), si no, pasa vacío
        delete_template(self.page, filtro=self.service.get("slug", "") if self.service else "")

        # Optional indexación (solo si lo necesitas)
        # indexing_controller(id, url)
