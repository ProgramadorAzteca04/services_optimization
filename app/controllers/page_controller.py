from playwright.sync_api import sync_playwright
from .campaign_controller import get_campaigns
from .design_controller import get_design
from app.components import WordpressComponent
from app.utilities.wordpress_utilities import save_template, go_to_page_section
from app.components import InitLayout
import json


def get_website_info(
    id: int,
    campaign_id: int,
    title_seo: str,
    meta_description: str,
    key_phrase: str,
    url: str,
    reviews: int,
    blocks: list,
):
    campaign_list = json.loads(get_campaigns())

    for campaign in campaign_list:
        if campaign["id"] == id:
            name = campaign["name"]
            break

    return json.dumps(get_design(
          id,
          campaign_id,
          title_seo,
          meta_description,
          key_phrase,
          url,
          reviews,
          blocks,
            ))


def create_page(
    id: int,
    campaign_id: int,
    title_seo: str,
    meta_description: str,
    key_phrase: str,
    reviews: int,
    blocks: list,
    url: str,
):
    result = {"status": "error", "message": "Error desconocido"}
    try:
        website_info = get_website_info(
            id,
            campaign_id,
            title_seo,
            meta_description,
            key_phrase,
            url,
            reviews,
            blocks,
        )
        design_data = json.loads(website_info)
        init_layout = InitLayout(design_data).init()  # ✅ ahora sí ejecuta el método


        result = {"status": "error", "message": "Error desconocido"}

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=False,
                    args=[
                        "--window-size=1524, 968",
                        "--force-device-scale-factor=0.64",
                    ],
                )
                page = browser.new_page()
                page.set_viewport_size({"width": 1524, "height": 968})

                wordpress_component = WordpressComponent(page, design_data)
                result = wordpress_component.dates_wordpress(
                    reviews, url, init_layout, meta_description,campaign_id
                )

                if result["status"] == "ok":
                    page.evaluate("alert('Pagina creada')")
                else:
                    page.evaluate("alert('Error al crear la pagina')")
            # --- Nuevo flujo: primero vamos a la página pública ---
            page.goto(url)

            # 3. Import dinámico para evitar circularidad
            from app.controllers.form_controller import perform_login
            from app.components.wordpress_component import WordpressComponent

            # 4. Hacer login y recuperar dominio
            domain = perform_login(page, campaign_id, url, design_data)
            if not domain:
                raise Exception("No se obtuvo dominio tras login")

            # 5. Guardar plantilla en Elementor
            template_name = str(design_data["campaign"]).lower().replace(" ", "_")
            template_file = f"app/layouts/{template_name}.json"
            save_template(
                page,
                template_file,
                domain,          # dominio correcto
                url,
                init_layout,
                design_data
            )

            # 6. Navegar a la sección de edición
            go_to_page_section(page, domain)

            # 7. Publicar contenido y limpiar
            wp = WordpressComponent(page, design_data)
            wp.dates_wordpress(
                reviews,
                url,
                init_layout,
                meta_description,
                campaign_id
            )

            browser.close()

        except Exception as e:
            print(f"Error al crear la pagina: {e}")

    except Exception as e:
        print(f"Error al obtener la información de la pagina: {e}")

    return result
