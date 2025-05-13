import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


from .report_utilities import export_report

load_dotenv()

template_path = os.getenv("TEMPLATE_PATH")
print(template_path)


def page_title(page: Page, title: str):
    try:
        page.wait_for_selector("xpath=//input[@name='post_title']")
        page.fill("//input[@name='post_title']", title)
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


# ... (todo el principio idéntico)


def insert_wordpress_data(
    page: Page, key_phrase: str, meta_description: str, title: str, reviews: int
):
    error_report = []

    def write_error_and_exit(step: str, error: Exception):
        error_report.append(
            {
                "step": step,
                "status": "error",
                "message": str(error),
                "timestamp": datetime.now().isoformat(),
            }
        )

        excel_report = export_report(error_report)
        return {
            "status": "error",
            "url": None,
            "report": error_report,
            "file": excel_report,
            "code": 500,
        }

    try:
        page.wait_for_timeout(1000)
        print("Insertando titulo de la pagina...")
        page_title(page, key_phrase.title())
        error_report.append(
            {"step": "Insertando titulo de la pagina", "status": "ok", "message": ""}
        )
    except Exception as e:
        return write_error_and_exit("Insertando titulo de la pagina", e)

    try:
        print("Insertando titulo SEO...")
        seo_title(page, title.title())
        error_report.append(
            {"paso": "insertar_titulo_seo", "status": "ok", "message": ""}
        )
    except Exception as e:
        return write_error_and_exit("insertar_titulo_seo", e)

    try:
        print("Insertando frase clave...")
        page.wait_for_selector("#focus-keyword-input-metabox")
        page.fill("#focus-keyword-input-metabox", key_phrase.title())
        error_report.append(
            {"paso": "insertar_frase_clave", "status": "ok", "message": ""}
        )
    except Exception as e:
        return write_error_and_exit("insertar_frase_clave", e)

    try:
        print("Insertando meta descripción...")
        page.wait_for_selector("#yoast-google-preview-description-metabox")
        page.fill("#yoast-google-preview-description-metabox", meta_description)
        error_report.append(
            {"paso": "insertar_meta_descripción", "status": "ok", "message": ""}
        )
    except Exception as e:
        return write_error_and_exit("insertar_meta_descripción", e)

    page.wait_for_timeout(1000)

    try:
        print("Click en cornerstone...")
        corner = page.wait_for_selector(
            "//button[@id='yoast-cornerstone-collapsible-metabox']//*[name()='svg']",
            timeout=5000,
        )
        corner.scroll_into_view_if_needed()
        corner.click()

        checkbox = page.locator("//div[@role='checkbox']")
        checkbox.click()
        error_report.append(
            {"paso": "activar_cornerstone", "status": "ok", "message": ""}
        )
    except Exception as e:
        return write_error_and_exit("activar_cornerstone", e)

    try:
        print("Insertando descripción...")
        description = page.locator(
            "//label[contains(text(), 'Descrip')]/following::input[1]"
        )

        description.clear()
        description.fill(meta_description)
        error_report.append(
            {"paso": "insertar_descripción", "status": "ok", "message": ""}
        )
    except Exception as e:
        return write_error_and_exit("insertar_descripción", e)

    try:
        print("Insertando reviews...")
        number_of_reviews = page.locator(
            "//label[contains(text(), 'Descrip')]/following::input[2]"
        )
        number_of_reviews.clear()
        number_of_reviews.fill(str(reviews))
        error_report.append({"paso": "insertar_reviews", "status": "ok", "message": ""})
    except Exception as e:
        return write_error_and_exit("insertar_reviews", e)

    try:
        print("Publicando datos iniciales...")
        publish = page.locator("//input[@id='save-post']")
        publish.scroll_into_view_if_needed()
        publish.click()
        error_report.append(
            {"paso": "publicar_borrador", "status": "ok", "message": ""}
        )
    except Exception as e:
        return write_error_and_exit("publicar_borrador", e)

    page.wait_for_timeout(10000)

    try:
        print("Yendo a elementor...")
        page.wait_for_selector("#elementor-switch-mode-button")
        page.click("#elementor-switch-mode-button")
        error_report.append({"paso": "entrar_elementor", "status": "ok", "message": ""})
    except Exception as e:
        return write_error_and_exit("entrar_elementor", e)

    page.wait_for_timeout(10000)

    try:
        print("Cambiar a iframe...")
        iframe_element = page.wait_for_selector("iframe")
        frame = iframe_element.content_frame()
        frame.click(".elementor-add-section-area-button.elementor-add-template-button")

        print("Click en plantillas...")
        page.wait_for_selector(
            "//*[@id='elementor-template-library-header-menu']/div[3]"
        )
        page.click("//*[@id='elementor-template-library-header-menu']/div[3]")

        page.wait_for_timeout(5000)

        page.wait_for_selector(
            "//*[@id='elementor-template-library-header-menu']/div[1]"
        )
        page.click("//*[@id='elementor-template-library-header-menu']/div[1]")

        page.wait_for_timeout(5000)

        page.wait_for_selector(
            "//*[@id='elementor-template-library-header-menu']/div[3]"
        )
        page.click("//*[@id='elementor-template-library-header-menu']/div[3]")

        page.wait_for_timeout(5000)
        container = page.wait_for_selector(
            "//div[@id='elementor-template-library-templates-container']", timeout=10000
        )
        elements = container.query_selector_all(".elementor-template-library-template")

        # Insertar plantilla
        encontrada = False
        for element in elements:
            name = element.query_selector(".elementor-template-library-template-name")
            if name and "base servicios" in name.inner_text().lower():
                insert_button = element.query_selector(
                    ".elementor-template-library-template-insert"
                )
                insert_button.click()
                encontrada = True
                break

        if not encontrada:
            raise Exception("Plantilla 'base servicios' no encontrada")

        try:
            apply_button = page.wait_for_selector(
                "//button[normalize-space()='Apply' or normalize-space()='Aplicar']",
                timeout=5000,
            )
            apply_button.click()
        except:  # noqa: E722
            print("No hay botón aplicar, se continúa")

        error_report.append(
            {"paso": "insertar_plantilla_elementor", "status": "ok", "message": ""}
        )
    except Exception as e:
        return write_error_and_exit("insertar_plantilla_elementor", e)

    page.wait_for_timeout(60000)

    try:
        print("Publicando...")

        page.keyboard.press("Control+S")
        page.wait_for_timeout(90000)
        error_report.append(
            {"paso": "publicar_elementor", "status": "ok", "message": ""}
        )
    except Exception as e:
        return write_error_and_exit("publicar_elementor", e)

    page.wait_for_timeout(5000)

    try:
        page.go_back()
        page.wait_for_timeout(3000)
        page.click(
            "//a[contains(text(),'Set featured') or contains(text(),'Establecer la imagen destacada')]"
        )
        page.wait_for_timeout(3000)

        image = page.wait_for_selector(
            "//div[@id='__wp-uploader-id-2']//li[1]", timeout=5000
        )
        image.click()
        page.click(
            "//button[contains(text(),'Set featured image') or contains(text(),'Establecer la imagen destacada')]"
        )
        error_report.append({"paso": "imagen_destacada", "status": "ok", "message": ""})
    except Exception as e:
        return write_error_and_exit("imagen_destacada", e)

    try:
        page.wait_for_timeout(3000)
        page.locator(
            "(//input[contains(@id, 'publi')])[3]"
        ).scroll_into_view_if_needed()
        page.click("(//input[contains(@id, 'publi')])[3]")
        error_report.append({"paso": "actualizar_final", "status": "ok", "message": ""})
    except Exception as e:
        return write_error_and_exit("actualizar_final", e)

    page.wait_for_timeout(3000)
    new_page = page.url

    return {"status": "ok", "url": new_page, "reporte": error_report, "code": 200}


def delete_template(page: Page):
    try:
        filas = page.locator("//tbody[@id='the-list']/tr")
        count = filas.count()
        print("Número de filas encontradas:", count)

        for i in range(count):
            fila = filas.nth(i)

            try:
                # Localiza título por XPath con locator
                titulo = fila.locator(
                    "xpath=.//td[@data-colname='Título' or @data-colname='Title']//a[contains(text(), 'Base servicios')]"
                )

                if titulo.count() > 0:
                    print(titulo.first.inner_text())  # sync

                    try:
                        checkbox = fila.locator("xpath=.//th//input[@type='checkbox']")
                        if checkbox.count() > 0:
                            checkbox.first.click()
                            page.wait_for_timeout(2000)
                            print("Checkbox encontrado y clickeado.")
                    except Exception as e:
                        print(f"Error al marcar el checkbox: {e}")
                else:
                    print("No se encontró el título 'Base servicios' en esta fila.")

            except PlaywrightTimeoutError:
                print("Timeout esperando el título en esta fila, se omite.")
                continue
            except Exception as e:
                print(f"Error al buscar el título: {e}")

    except Exception as e:
        print(f"Error al buscar las filas: {e}")

    # Acción masiva para enviar a papelera
    try:
        print("Ejecutando acción masiva para mover a papelera...")
        page.select_option("#bulk-action-selector-top", value="trash")
        page.click("#doaction")
        print("Acción masiva ejecutada.")
    except Exception as e:
        print(f"Error al ejecutar acción masiva: {e}")


def save_template(
    page: Page,
    template_file: str,
    domain: str,
    url: str,
    init_layout,
    design_data: dict,
):

    template_url = (
          f"{domain.rstrip('/')}/wp-admin/edit.php?post_type=elementor_library&tabs_group=library"
    )
    page.goto(template_url)

    page.wait_for_selector("#the-list", timeout=10000)
    delete_template(page)
    get_template(page, url, design_data)
    page.goto(template_url)
    delete_template(page)

    response = init_layout.init()
    print(response)

    page.click("#elementor-import-template-trigger")
    page.wait_for_timeout(2000)

    input_archivo_xpath = (
        "//*[@id='elementor-import-template-form-inputs']/input[@name='file']"
    )
    input_archivo = page.wait_for_selector(input_archivo_xpath, timeout=5000)

    base_directory = (
        Path(__file__).resolve().parent.parent.parent
    )  # Desde utilities/ hasta app/
    layout_path = base_directory / template_file

    print(f"Ruta de la plantilla esperada: {layout_path}")

    if not layout_path.exists():
        print(f"Plantilla no encontrada: {layout_path}")
        return

    for file in (base_directory / "layouts").glob("*"):
        print(f"- {file.name}")

    input_archivo.set_input_files(str(layout_path))
    page.wait_for_timeout(5000)

    page.click("#e-import-template-action")
    page.wait_for_timeout(5000)


def get_template(page: Page, link: str, design_data: dict):
    print("Obteniendo plantilla")
    page.goto(link)
    page.wait_for_timeout(5000)
    print("Recargando")
    page.reload()
    page.wait_for_timeout(5000)
    print("Recargado")

    try:
        page.wait_for_timeout(5000)
        print("Yendo a Elementor...")
        page.click(
            "//span[normalize-space()='Edit with Elementor' or normalize-space()='Editar con Elementor']"
        )
        page.wait_for_timeout(60000)
    except Exception as e:
        print(f"Error al ir a Elementor: {e}")

    page.wait_for_timeout(6000)

    try:
        print("Desplegando menu de plantillas")
        page.wait_for_timeout(30000)

        button_locator = page.locator(
            "//button[(@aria-label='Guardar opciones' or @aria-label='Save Options') and @type='button']"
        )
        button_locator.wait_for(state="visible")

        button_locator.click()

    except Exception as e:
        print(f"Error al desplegar el menu de plantillas: {e}")

    page.wait_for_timeout(5000)

    print("Esperando el contenedor de plantillas")
    page.wait_for_timeout(5000)
    templates = page.wait_for_selector("(//div[@role='menuitem'])[2]")
    templates.click()
    page.wait_for_timeout(5000)

    try:
        print("Nombrando plantilla como Base servicios")
        page.fill(
            "//input[@id='elementor-template-library-save-template-name']",
            "Base servicios",
        )
        page.wait_for_timeout(5000)
    except Exception as e:
        print(f"Error al nombrar la plantilla: {e}")

    page.wait_for_timeout(5000)

    try:
        print("Guardando plantilla")
        page.click("//button[@id='elementor-template-library-save-template-submit']")
        page.wait_for_timeout(5000)
    except Exception as e:
        print(f"Error al guardar la plantilla: {e}")

    page.wait_for_timeout(5000)

    try:
        print("Esperando el contenedor de plantillas")
        page.wait_for_timeout(5000)
        container = page.wait_for_selector(
            "//div[@id='elementor-template-library-templates' and @data-template-source='local']/div[@id='elementor-template-library-templates-container']",
            timeout=10000,
        )

        print("Buscando plantillas...")
        page.wait_for_timeout(5000)
        elements = container.query_selector_all(
            ".elementor-template-library-template.elementor-template-library-template-local.elementor-template-library-pro-template"
        )

        print(len(elements))

    except Exception as e:
        print(e)

    file_name = design_data.get("alt_name").replace(" ", "_").lower() + ".json"
    complete_path = Path(template_path) / file_name
    print(complete_path)
    

    if complete_path.exists():
        print(f"La plantilla ya existe Eliminando {complete_path}")
        complete_path.unlink()

    print("Exportando plantilla...")
    i = 0
    for element in elements:
        i += 1
        name = element.query_selector(".elementor-template-library-template-name")
        text_name = name.inner_text() if name else ""

        if "base servicios" in text_name.lower():
            try:
                selector = (
                    "(//div[@class='elementor-template-library-template-more-toggle'])"
                )
                more_actions = element.query_selector(f"{selector}[{i}]")
                if more_actions:
                    more_actions.click()
            except Exception as e:
                print(e)
            with page.expect_download() as download_info:
                # Espera a que el selector sea visible
                export_button = element.query_selector(
                    f"(//span[contains(text(),'port')])[{i + 1}]"
                )

                # Verifica si el elemento es visible antes de hacer clic
                if export_button.is_visible():
                    export_button.click()
                else:
                    print("El botón no es visible.")

            download = download_info.value

            download.save_as(str(complete_path))
            print(f"Plantilla exportada a {complete_path}")
