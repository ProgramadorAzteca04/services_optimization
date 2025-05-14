import json
from playwright.sync_api import sync_playwright
from fastapi import HTTPException
 
from app.controllers.design_controller import get_design
from app.components.init_layout_component import InitLayout
from app.utilities.wordpress_utilities import save_template, go_to_page_section
 
 
def get_website_info(
    campaign_id: int,
    title_seo: str,
    meta_description: str,
    key_phrase: str,
    url: str,
    reviews: int,
    blocks: list,
):
    return get_design(
        campaign_id,
        title_seo,
        meta_description,
        key_phrase,
        url,
        reviews,
        blocks,
    ) 
 
 
def create_page(
    campaign_id: int,
    title_seo: str,
    meta_description: str,
    key_phrase: str,
    reviews: int,
    blocks: list,
    url: str,
):
    # 1. Obtener diseño
    website_info = get_website_info(
        campaign_id,
        title_seo,
        meta_description,
        key_phrase,
        url,
        reviews,
        blocks,
    )
    try:
        design_data = json.loads(website_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSON inválido: {e}")
    if "error" in design_data:
        raise HTTPException(status_code=500, detail=design_data["error"])
 
    design_data["campaign"] = campaign_id
    init_layout = InitLayout(design_data)
 
    try:
        # 2. Iniciar Playwright
        playwright = sync_playwright().start()
        try:
            browser = playwright.chromium.launch(
                headless=False,
                args=["--window-size=1524,968",
                      "--force-device-scale-factor=0.64"],
            )
            page = browser.new_page()
            page.set_viewport_size({"width": 1524, "height": 968})
 
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
            campaign = str(
                design_data["alt_name"]).lower().replace(" ", "_")
            service = design_data["service"]
            template = service.get("services_slug")
            template_file = f"app/layouts/{campaign}/{template}.json"
            save_template(
            page,
            template_file,
            domain,        
            url,           
            init_layout,  
            design_data
            )

 
            # 6. Navegar a la sección de edición
            go_to_page_section(page, url)
 
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
        finally:
            playwright.stop()
    except Exception as e:
        return {"status": "error", "message": str(e)}
 
    return {"status": "ok", "message": "Página creada exitosamente"}
 
 