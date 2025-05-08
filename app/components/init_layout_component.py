from fastapi import HTTPException
from concurrent.futures import ThreadPoolExecutor

# Importar clases de cada servicio - ELITE CHICAGO SPA
from app.components.elite_chicago_spa.botox_chicago import BotoxChicago
from app.components.elite_chicago_spa.coolsculpting_in_chicago import CoolsculptingChicago
from app.components.elite_chicago_spa.facials_chicago import FacialsChicago
from app.components.elite_chicago_spa.laser_hair_removal_in_chicago import LaserHairRemovalChicago

# ELITE CHICAGO SPA
def init_botox_chicago(options: dict):
    try:
        json_component = BotoxChicago(options)
        blocks = options["blocks"]
        steps = [getattr(json_component, block) for block in blocks]

        def execute_steps(step): step()

        with ThreadPoolExecutor() as executor:
            executor.map(execute_steps, steps)

        return "Servicio Botox Chicago optimizado exitosamente"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def init_facials_chicago(options: dict):
    try:
        json_component = FacialsChicago(options)
        blocks = options["blocks"]
        steps = [getattr(json_component, block) for block in blocks]

        def execute_steps(step): step()

        with ThreadPoolExecutor() as executor:
            executor.map(execute_steps, steps)

        return "Servicio Facials Chicago optimizado exitosamente"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def init_coolsculpting_chicago(options: dict):
    try:
        json_component = CoolsculptingChicago(options)
        blocks = options["blocks"]
        steps = [getattr(json_component, block) for block in blocks]

        def execute_steps(step): step()

        with ThreadPoolExecutor() as executor:
            executor.map(execute_steps, steps)

        return "Servicio Coolsculpting Chicago optimizado exitosamente"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def init_laser_hair_removal_chicago(options: dict):
    try:
        json_component = LaserHairRemovalChicago(options)
        blocks = options["blocks"]
        steps = [getattr(json_component, block) for block in blocks]

        def execute_steps(step): step()

        with ThreadPoolExecutor() as executor:
            executor.map(execute_steps, steps)

        return "Servicio Laser Hair Removal Chicago optimizado exitosamente"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Clase despachadora
class InitEliteChicagoSpaService:
    def __init__(self, options: dict):
        self.options = options

    def init(self):
        try:
            switch = {
                "botox": init_botox_chicago,
                "facials": init_facials_chicago,
                "coolsculpting": init_coolsculpting_chicago,
                "laser": init_laser_hair_removal_chicago,
            }

            service = self.options["service"]
            selected_function = switch.get(service)

            if selected_function:
                return selected_function(self.options)
            else:
                raise ValueError(f"Servicio '{service}' no está registrado en Elite Chicago Spa.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
