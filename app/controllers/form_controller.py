import os
import shutil

from playwright.sync_api import Page
from app.utilities.wordpress_utilities import go_to_page_section, login, save_template
from app.components.init_layout_component import InitLayout
from app.config import local_session
from app.models.campaign import Campaign
from app.models.domain import Domain



# Perform login function
def perform_login(
    page: Page,
    campaign_id: int,
    url: str,
    design_data: dict,
) -> str:
    """
    1) Recupera el dominio desde BD
    2) Navega a la pantalla de login de WP
    3) Rellena credenciales y espera a que el dashboard cargue
    4) Devuelve el dominio para seguir el flujo
    """
    with local_session() as session:
        campaign = session.query(Campaign).filter_by(id=campaign_id).first()
        if not campaign:
            raise Exception(f"Campaña {campaign_id} no encontrada")
        domain_info = session.query(Domain).filter_by(campaign_id=campaign.id).first()
        if not domain_info:
            raise Exception(f"Dominio para campaña {campaign_id} no configurado")

        # --- 1) Preparar dominio y URL de login ---
        domain = domain_info.domain.rstrip("/")
        login_url = f"{domain}/wp-login.php"

        # --- 2) Ir a la página de login y esperar al formulario ---
        page.goto(login_url)
        page.wait_for_selector("#user_login", timeout=15000)

        # --- 3) Rellenar credenciales y enviar ---
        page.fill("#user_login", domain_info.admin)
        page.fill("#user_pass", domain_info.password)
        page.click("#wp-submit")

        # --- 4) Esperar a que cargue el Panel de Control ---
        # Por ejemplo, que aparezca el menú lateral de WP Admin
        page.wait_for_selector("#adminmenu", timeout=15000)

        print(f" Login realizado exitosamente en {domain}")
        return domain



# Obtener información del sitio web


# Obtener y guardar la plantilla desde Elementor
def get_template(page: Page, link: str, file_name: str):
    DOWNLOAD_PATH = "app/layouts/"
    print("Obteniendo plantilla")
    page.goto(link)
    page.wait_for_timeout(10000)
    print("Recargando")
    page.reload()
    page.wait_for_timeout(10000)
    print("Recargado")
    page.wait_for_timeout(60000)
    try:
        print("Yendo a Elementor...")
        page.wait_for_selector(
            "//span[normalize-space()='Edit with Elementor' | normalize-space()='Editar con Elementor']",
            timeout=10000,
        )
        page.click(
            "//span[normalize-space()='Edit with Elementor' | normalize-space()='Editar con Elementor']"
        )
    except Exception as e:
        print(f"Error al ir a Elementor: {e}")
    page.wait_for_selector(
        "//span[normalize-space()='Editar con Elementor']",
        timeout=10000,
    )
    page.click("//span[normalize-space()='Editar con Elementor']")

    page.wait_for_timeout(10000)

    try:
        print("Desplegando menú de plantillas")
        page.click("(//div[@role='menuitem'])[2]")
    except Exception as e:
        print(f"Error al desplegar el menú de plantillas: {e}")

    page.wait_for_timeout(15000)

    try:
        print("Nombrando plantilla como Base Servicios")
        page.fill(
            "//input[@id='elementor-template-library-save-template-name']",
            "Base Servicios",
        )
    except Exception as e:
        print(f"Error al nombrar la plantilla: {e}")

    page.wait_for_timeout(5000)

    try:
        print("Guardando plantilla")
        page.click("//button[@id='elementor-template-library-save-template-submit']")
    except Exception as e:
        print(f"Error al guardar la plantilla: {e}")

    page.wait_for_timeout(5000)

    try:
        print("Esperando contenedor de plantillas")
        container = page.wait_for_selector(
            "//div[@id='elementor-template-library-templates' and @data-template-source='local']/div[@id='elementor-template-library-templates-container']",
            timeout=10000,
        )
        print("Buscando plantillas...")
        elements = container.query_selector_all(
            ".elementor-template-library-template.elementor-template-library-template-local.elementor-template-library-pro-template"
        )
    except Exception as e:
        print(f"Error al buscar plantillas: {e}")
        return

    print("Aplicando plantilla...")
    for element in elements:
        try:
            name = element.query_selector(".elementor-template-library-template-name")
            if not name:
                print(" Elemento sin nombre detectado, se omite.")
                continue
            text_name = name.inner_text()
        except Exception as e:
            print(" Error al obtener el nombre del template:", e)
            continue

        if str(text_name).lower() == "base servicios":
            try:
                more_actions = element.query_selector(
                    "//div[span[text()='More actions']] or //div[span[text()='Más acciones']]"
                )
                if more_actions:
                    more_actions.click()
                    page.wait_for_timeout(1000)
            except Exception as e:
                print("Error al abrir acciones:", e)

            try:
                # Construimos la ruta completa
                path_final = os.path.join(DOWNLOAD_PATH, file_name)

                # Eliminamos si ya existe
                if os.path.exists(path_final):
                    print(f"Eliminando archivo existente: {path_final}")
                    os.remove(path_final)

                with page.expect_download() as download_info:
                    export_button = page.wait_for_selector(
                        "//span[text()='Export']/parent::a",
                        timeout=5000,
                    )
                    export_button.click()

                download = download_info.value
                downloaded_path = download.path()

                shutil.move(downloaded_path, path_final)

                print(f"Archivo exportado y guardado en: {path_final}")

            except Exception as e:
                print("Error en la descarga o movimiento del archivo:", e)

            break


def delete_old_template(page: Page, ulr: str):
    page.goto(ulr)
    page.wait_for_timeout(6000)
    try:
        print("Redirigiendo a editar la pagina")
        page.wait_for_selector("//a[contains(normalize-space(text()), 'Edit')]")
        page.click("//a[contains(normalize-space(text()), 'Edit')]")
        page.wait_for_timeout(5000)
        print("Obteniendo slug")
        slug = page.input_value("//input[@id='yoast-google-preview-slug-metabox']")

        try:
            print("Eliminando la plantilla antigua")
            page.wait_for_selector(
                "//a[normalize-space()='Move to Trash' or normalize-space()='Mover a la papelera']"
            )
            page.click(
                "//a[normalize-space()='Move to Trash' or normalize-space()='Mover a la papelera']"
            )
            page.wait_for_timeout(5000)
            print("Plantilla eliminada")

            try:
                print("Redirigiendo a la pagina optimizada")
                page.go_back()
                page.wait_for_timeout(5000)
                page.go_back()
                page.wait_for_timeout(10000)
                try:
                    page.wait_for_selector(
                        "//a[contains(normalize-space(text()), 'Edit')]"
                    )
                    page.click("//a[contains(normalize-space(text()), 'Edit')]")
                    page.wait_for_timeout(2000)
                    print("Sustituyendo el slug de pagina")
                    page.wait_for_selector(
                        "//input[@id='yoast-google-preview-slug-metabox']"
                    )
                    page.click("//input[@id='yoast-google-preview-slug-metabox']")
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    page.fill(
                        "//input[@id='yoast-google-preview-slug-metabox']",
                        slug,
                    )
                    print("Slug eliminado")
                    try:
                        print("Actualizando Pagina")
                        page.wait_for_selector("//input[@id='publish']")
                        page.click("//input[@id='publish']")
                        page.wait_for_load_state("networkidle")
                        print("Pagina actualizada")
                        page.wait_for_timeout(5000)
                    except Exception as e:
                        print(f"Error al actualizar la pagina: {e}")
                except Exception as e:
                    print(f"Error al modificar el slug de pagina: {e}")
            except Exception as e:
                print(f"Error al devolver a la pagina optimizada: {e}")

        except Exception as e:
            print(f"Error al eliminar la plantilla antigua: {e}")

    except Exception as e:
        print(f"Error al eliminar la plantilla {e}")