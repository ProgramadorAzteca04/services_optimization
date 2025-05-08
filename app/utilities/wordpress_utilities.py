import os
from pathlib import Path
from app.utilities.wordpress_utilities import page_title
from app.utilities.wordpress_utilities import get_template
from dotenv import load_dotenv
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

load_dotenv

template_path = os.getenv("TEMPLATE_PATH")
print(template_path)

def page_title(page: Page, title: str):
    try:
        Page.wait_for_selector("xpath=//input[@name='post_title']")
        Page.fill("//input[@name='post_title']", title)
    except Exception as e:
        print(e)

def seo_title(page: Page, title: str):
    try:
        title_seo = page.wait_for_selector(
            "//div[@id='yoast-google-preview-title-metabox']//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']",
            timeout=5000,
        )
        title_seo.click()
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        title_seo.fill(title)
        print(f"Insertando titulo SEO: {title}")
    except Exception as e:
        print(e)


def login(page: Page, username: str, password: str):
    page.wait_for_timeout(2000)

    page.fill("#user_login", username)
    page.fill("#user_pass", password)
    page.click("#wp-submit")


def go_to_page_section(page: Page, url: str):
    page.goto(f"{url}wp-admin/post-new.php?post_type=page")

    page.wait_for_timeout(6000)

    page.reload()

def insert_wordpress_data(
    page: Page,
    key_phrase: str,
    meta_description: str,
    title: str = "",
    reviews: int = 0,
    service: dict = None,
):
    if service:
        key_phrase = f"{service['name']} in {service['city']}"
        meta_description = f"{service['name']}"
        title = f"{service['name']} in {service['city']} - {service['state']}"

    page.wait_for_timeout(1000)
    page_title(page, key_phrase.title())
    seo_title(page, title.title())
    page.wait_for_selector("#focus-keyword-input-metabox")
    page.fill("#focus-keyword-input-metabox", key_phrase.title())
    page.wait_for_timeout(2000)

    try:
        page.wait_for_selector("#yoast-google-preview-description-metabox")
        page.fill("#yoast-google-preview-description-metabox", meta_description)
    except Exception as e:
        print("No se pudo insertar la meta descripcion", e)

    page.wait_for_timeout(5000)
    corner = page.wait_for_selector(
        "//button[@id='yoast-cornerstone-collapsible-metabox']//*[name()='svg']",
        timeout=5000,
    )
    corner.scroll_into_view_if_needed()
    corner.click()
    page.wait_for_timeout(5000)
    checkbox = page.locator("//div[@role='checkbox']")
    checkbox.click()

    try:
        description = page.locator(
            "//label[contains(text(), 'Descripción') or contains(text(), 'Description')]/following::input[1]"
        )
        description.clear()
        description.fill(meta_description)
    except Exception as e:
        print("Fallo al insertar la descripcion", e)

    page.wait_for_timeout(5000)

    try:
        number_of_reviews = page.locator(
            "//label[contains(text(), 'Descripción') or contains(text(), 'Description')]/following::input[2]"
        )
        number_of_reviews.clear()
        number_of_reviews.fill(str(reviews))
    except Exception as e:
        print("Fallo al insertar las reviews", e)

    page.wait_for_timeout(5000)

    try:
        publish = page.locator("//input[@id='save-post']")
        publish.scroll_into_view_if_needed()
        publish.click()
    except Exception as e:
        print(e)

    page.wait_for_timeout(60000)
    page.wait_for_selector("#elementor-switch-mode-button")
    page.click("#elementor-switch-mode-button")
    page.wait_for_timeout(60000)
    iframe_element = page.wait_for_selector("iframe")
    frame = iframe_element.content_frame()
    frame.click(".elementor-add-section-area-button.elementor-add-template-button")
    page.wait_for_selector("//*[@id='elementor-template-library-header-menu']/div[3]")
    page.click("//*[@id='elementor-template-library-header-menu']/div[3]")

    try:
        page.wait_for_timeout(30000)
        container = page.wait_for_selector(
            "//div[@id='elementor-template-library-templates' and @data-template-source='local']/div[@id='elementor-template-library-templates-container']",
            timeout=10000,
        )
        elements = container.query_selector_all(
            ".elementor-template-library-template.elementor-template-library-template-local.elementor-template-library-pro-template"
        )
        if not container or not elements:
            raise Exception("No se encontraron plantillas. Recargando...")
    except Exception as e:
        print(f"Error al esperar el contenedor de plantillas: {e}")
        page.reload()
        page.wait_for_timeout(5000)
        page.click(".elementor-add-section-area-button.elementor-add-template-button")
        page.click("//*[@id='elementor-template-library-header-menu']/div[3]")
        page.wait_for_timeout(5000)
        container = page.wait_for_selector(
            "//div[@id='elementor-template-library-templates' and @data-template-source='local']/div[@id='elementor-template-library-templates-container']",
            timeout=5000,
        )
        elements = container.query_selector_all(
            ".elementor-template-library-template.elementor-template-library-template-local.elementor-template-library-pro-template"
        )

    for element in elements:
        name = element.query_selector(".elementor-template-library-template-name")
        text_name = name.inner_text() if name else ""
        if "base optimizada" in text_name.lower():
            try:
                insert_button = element.query_selector(
                    ".elementor-template-library-template-action.elementor-template-library-template-insert.elementor-button.e-primary.e-btn-txt"
                )
                if insert_button:
                    insert_button.click()
            except Exception as e:
                print(e)
            page.wait_for_timeout(5000)
            try:
                apply_button = page.wait_for_selector(
                    "//button[normalize-space()='Apply' or normalize-space()='Aplicar']",
                    timeout=5000,
                )
                apply_button.click()
            except Exception as e:
                print("No hay botón de aplicar", e)

    page.wait_for_timeout(60000)
    page.click(
        "//button[contains(@class, 'MuiButton-contained') and (contains(., 'Publicar') or contains(., 'Publish'))]"
    )
    page.wait_for_timeout(5000)
    page.go_back()
    page.wait_for_timeout(5000)
    page.click(
        "//a[contains(text(),'Set featured') or contains(text(),'imagen destacada')]"
    )
    page.wait_for_timeout(5000)

    try:
        image = page.wait_for_selector(
            "//div[@id='__wp-uploader-id-2']//li[1]",
            timeout=5000,
        )
        image.click()
        page.click(
            "//button[contains(text(),'Set featured image') or contains(text(),'Establecer la imagen destacada')]"
        )
    except Exception as e:
        print(f"No se pudo seleccionar la imagen: {e}")

    page.wait_for_timeout(5000)
    page.click(
        "//input[@type='submit' and (contains(@value,'Update') or contains(@value,'Actualizar'))]"
    )
    page.wait_for_timeout(5000)

def delete_template(page: Page, filtro: str = ""):
    try:
        filas = page.locator("//tbody[@id='the-list']/tr")
        count = filas.count()
        print(" Número de filas encontradas:", count)

        seleccionados = 0

        for i in range(count):
            fila = filas.nth(i)

            try:
                # Buscar solo si contiene 'Base optimizada' y el filtro (si hay)
                xpath = f".//td[@data-colname='Título' or @data-colname='Title']//a[contains(text(), 'Base optimizada'){f' and contains(text(), \"{filtro}\")' if filtro else ''}]"
                titulo = fila.locator(f"xpath={xpath}")

                if titulo.count() > 0:
                    print(" Plantilla encontrada:", titulo.first.inner_text())

                    try:
                        checkbox = fila.locator("xpath=.//th//input[@type='checkbox']")
                        if checkbox.count() > 0:
                            checkbox.first.click()
                            page.wait_for_timeout(1000)
                            seleccionados += 1
                            print(" Checkbox clickeado.")
                    except Exception as e:
                        print(f" Error al marcar el checkbox: {e}")
                else:
                    print(" Esta fila no coincide con el filtro.")

            except PlaywrightTimeoutError:
                print(" Timeout esperando el título en esta fila, se reintenta...")
                page.wait_for_timeout(2000)
                continue
            except Exception as e:
                print(f" Error al buscar el título: {e}")

        if seleccionados == 0:
            print(" No se encontraron plantillas que coincidan con el filtro. Acción cancelada.")
            return

    except Exception as e:
        print(f" Error al buscar las filas: {e}")
        return

    try:
        print(" Ejecutando acción masiva para mover a papelera...")
        page.select_option("#bulk-action-selector-top", value="trash")
        page.click("#doaction")
        page.wait_for_timeout(3000)

        try:
            confirmacion = page.wait_for_selector(".updated.notice-success", timeout=5000)
            print(" Plantillas eliminadas exitosamente.")
        except PlaywrightTimeoutError:
            print(" Acción enviada, pero no se recibió confirmación visual.")

    except Exception as e:
        print(f" Error al ejecutar acción masiva: {e}")


        
def save_template(
    page: Page,
    template_file: str,
    domain: str,
    url: str,
  #  init_layout: InitLayout,
    design_data: dict,
    service: dict = None,
):
    filtro = service["slug"] if service and "slug" in service else ""
    service_name = service["name"] if service else ""

    print(f" Guardando plantilla para servicio: {service_name or 'all'}")
    print(f" Plantilla a guardar: {template_file}")
    template_url = f"{domain}wp-admin/edit.php?post_type=elementor_library&tabs_group=library"
    page.goto(template_url)

    page.wait_for_selector("#the-list", timeout=10000)
    delete_template(page, filtro=filtro)

    get_template(page, url, design_data)

    page.goto(template_url)
    delete_template(page, filtro=filtro)

    #response = init_layout.init()
    #print(f" Init layout response: {response}")

    page.click("#elementor-import-template-trigger")
    page.wait_for_timeout(2000)

    input_archivo_xpath = (
        "//*[@id='elementor-import-template-form-inputs']/input[@name='file']"
    )
    input_archivo = page.wait_for_selector(input_archivo_xpath, timeout=5000)

    base_directory = Path(__file__).resolve().parent.parent.parent
    layout_path = base_directory / template_file

    print(f" Ruta de la plantilla esperada: {layout_path}")
    if not layout_path.exists():
        print(f" Plantilla no encontrada: {layout_path}")
        return

    for file in (base_directory / "layouts").glob("*"):
        print(f" Disponible: {file.name}")

    input_archivo.set_input_files(str(layout_path))
    page.wait_for_timeout(5000)
    page.click("#e-import-template-action")
    page.wait_for_timeout(5000)

def save_template(
    page: Page,
    template_file: str,
    domain: str,
    url: str,
    #init_layout: InitLayout,
    design_data: dict,
    service: dict = None,
):
    filtro = service["slug"] if service and "slug" in service else ""
    service_name = service["name"] if service else ""
    slug = service["slug"] if service and "slug" in service else ""

    print(f" Guardando plantilla para servicio: {service_name or 'Genérico'}")

    # Ruta y nombre esperado del archivo exportado
    file_base = design_data.get("campaign", "plantilla").replace(" ", "_").lower()
    file_name = f"{file_base}_{slug}.json" if slug else f"{file_base}.json"
    complete_path = Path(template_path) / file_name

    if complete_path.exists():
        print(f" La plantilla ya fue exportada previamente: {complete_path}")
        return  # Evita el proceso completo si ya está guardada

    template_url = f"{domain}wp-admin/edit.php?post_type=elementor_library&tabs_group=library"
    page.goto(template_url)

    page.wait_for_selector("#the-list", timeout=10000)
    delete_template(page, filtro=filtro)

    get_template(page, url, design_data, service=service)

    page.goto(template_url)
    delete_template(page, filtro=filtro)

    #response = init_layout.init()
    #print(f" Init layout response: {response}")

    page.click("#elementor-import-template-trigger")
    page.wait_for_timeout(2000)

    input_archivo_xpath = (
        "//*[@id='elementor-import-template-form-inputs']/input[@name='file']"
    )
    input_archivo = page.wait_for_selector(input_archivo_xpath, timeout=5000)

    base_directory = Path(__file__).resolve().parent.parent.parent
    layout_path = base_directory / template_file

    print(f" Ruta de la plantilla esperada: {layout_path}")
    if not layout_path.exists():
        print(f" Plantilla no encontrada: {layout_path}")
        return

    for file in (base_directory / "layouts").glob("*"):
        print(f" Disponible: {file.name}")

    input_archivo.set_input_files(str(layout_path))
    page.wait_for_timeout(5000)
    page.click("#e-import-template-action")
    page.wait_for_timeout(5000)
