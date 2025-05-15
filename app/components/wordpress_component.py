# app/components/wordpress_component.py

from dotenv import load_dotenv
import os
from playwright.sync_api import Page
from app.utilities.wordpress_utilities import insert_wordpress_data, delete_template
from app.components.init_layout_component import InitLayout
from app.api.gpt_api import GPT

load_dotenv()

API_URL = os.getenv("API_URL")
META_FOLDER = os.getenv("META_FOLDER")

class WordpressComponent:
    def __init__(self, page: Page, design_data: dict):
        self.page = page
        self.design_data = design_data
        self.service = design_data.get("service")
        self.gpt = GPT(design_data)

    def dates_wordpress(
        self,
        reviews: int,
        url: str,
        init_layout: InitLayout,
        meta_description: str,
        _id: int,
    ):
        print("🟢 Iniciando flujo para servicio:", self.service.get("services_name", "Sin servicio"))


        # Import local para romper import circular
        from app.controllers.form_controller import perform_login

        try:
            self.page.wait_for_selector("#adminmenu", timeout=5000)
            print("🟢 Ya estoy logueado en WP")
        except Exception:
            # 1. Login en WP
            perform_login(
                self.page,
                self.design_data["campaign_id"],  # campaign_id (int)
                url,                            # URL pública de la página
                self.design_data               # todo el dict de diseño
            )

        # 2. Preparar datos para insertar
        frase_clave = self.design_data["key_phrase"].replace(",", "")
        title_seo = self.service.get("services_name", f"Campaña {self.design_data['campaign_id']}") #Se cambia para tomar el nombre del servicio en vez de la campaña


        # 3. Insertar contenido en WP
        insert_wordpress_data(
            self.page,
            frase_clave,
            meta_description,
            title_seo,
            reviews
        )

        # 4. Borrar plantilla antigua si corresponde
        filtro_slug = self.service.get("slug", "") if self.service else ""
        delete_template(self.page, filtro=filtro_slug)

        # (Opcional) indexación...
        # from app.controllers.indexing_controller import indexing_controller
        # indexing_controller(_id, url)
