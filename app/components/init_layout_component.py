from fastapi import HTTPException
import json
from app.components.elite_chicago_spa.init_elite_chicago_spa import EliteChicagoSpa

class InitLayout:
    def __init__(self, options: dict):
        self.options = options

        if isinstance(options, (str, dict)):    
            if isinstance(options, str):
             self.options = json.loads(options)
        else:
            self.options = options
    
    def init(self):
        try:
            switch = {
                15: EliteChicagoSpa, 
            }

            layout_id = int(self.options["layout"])
            selected_class = switch.get(layout_id)

            if selected_class:
                return selected_class(self.options).run()
            else:
                raise ValueError(f"No se encontró la campaña para layout {layout_id}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
