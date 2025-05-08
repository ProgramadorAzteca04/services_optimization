from fastapi import HTTPException

class InitLayout:
    def __init__(self, options: dict):
        self.options = options

    def init(self):
        try:
            switch = {
            
            }

            value = int(self.options["layout"])

            selected_function = switch.get(value)

            if selected_function:
                response = selected_function(self.options)
                return response
            else:
                raise ValueError(f"No se encontró la función para el layout {value}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))