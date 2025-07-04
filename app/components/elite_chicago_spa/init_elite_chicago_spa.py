from app.components.elite_chicago_spa.botox_chicago import BotoxChicago
from app.components.elite_chicago_spa.coolsculpting_in_chicago import CoolsculptingChicago
from app.components.elite_chicago_spa.facials_chicago import FacialsChicago
from app.components.elite_chicago_spa.laser_hair_removal_in_chicago import LaserHairRemovalChicago

class EliteChicagoSpa:
    def __init__(self, options: dict):
        self.options = options
        self.service = options.get("service", {}).get("services_slug", "")


    def run(self):
        service = {
            "botox-chicago": BotoxChicago,
            "facials-chicago": FacialsChicago,
            "coolsculpting-in-chicago": CoolsculptingChicago,
            "laser-hair-removal-in-chicago": LaserHairRemovalChicago, 
        }

        print(f"[DEBUG] slug recibido: {self.service}")
        print(f"[DEBUG] servicios disponibles: {list(service.keys())}")

        service_class = service.get(self.service)
        if not service_class:
            raise Exception(f"Servicio '{self.service}' no está registrado en EliteChicagoSpa")

        service_instance = service_class(self.options)
        for block in self.options["blocks"]:
            method = getattr(service_instance, block)
            method()
        return f"Servicio {self.service} ejecutado con éxito"

