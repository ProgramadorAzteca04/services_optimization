from playwright.sync_api import sync_playwright
from .campaign_controller import get_campaigns
from .design_controller import get_design
from app.components import WordpressComponent
from app.components import InitLayout
import json


def get_website_info(
    id: int,
    service: dict,
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

    return get_design(
        id,
        service,
        title_seo,
        meta_description,
        name,
        key_phrase,
        url,
        reviews,
        blocks,
    )


def create_page(
    id: int,
    service: dict,
    title_seo: str,
    meta_description: str,
    key_phrase: str,
    reviews: int,
    blocks: list,
    url: str,
    result = None,


    
):
    try:
        website_info = get_website_info(
            id,
            service,
            title_seo,
            meta_description,
            key_phrase,
            url,
            reviews,
            blocks,
        )
        design_data = json.loads(website_info)
        init_layout = InitLayout(design_data)

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
                    reviews, url, init_layout, design_data, meta_description, id
                )

                if result["status"] == "ok":
                    page.evaluate("alert('Pagina creada')")
                else:
                    page.evaluate("alert('Error al crear la pagina')")

                browser.close()

        except Exception as e:
            print(f"Error al crear la pagina: {e}")

    except Exception as e:
        print(f"Error al obtener la información de la pagina: {e}")

    return result
