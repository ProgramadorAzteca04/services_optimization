import json


#Abrir y cargar el archivo JSON

def json_to_dict(jsonFile):
      try:
            with open(jsonFile, 'r') as archivo:
                  json_local = json.load(archivo)

                  return json_local
      except FileExistsError:
            print(f"El archivo '{jsonFile}' no fue encontrado")
      except json.JSONDecodeError:
            print(f"El archivo '{jsonFile}' no es un archivo JSON")

#Guardar el archivo JSON:

def save_json_file(jsonFile, jsonLocal, nameCampaign):
      try:
            with open(jsonFile, 'w') as archivo:
                  json.dump(jsonLocal, archivo, indent=4)
                  print(f"Componente {nameCampaign} guardado con exitosamente")
      except FileExistsError:
                  print(f"El archivo '{jsonFile}' no fue encontrado")
      except json.JSONDecodeError as e:
                  print(f"El archivo '{jsonFile}' no es un archivo JSON. Detalles: {str(e)}")

      except Exception as e:
            print(f"Error inesperado al guardar el archivo '{jsonFile}': {str(e)}")

def findElementById(jsonLocal, elementId):
    if isinstance(jsonLocal, dict):
        if "id" in jsonLocal and jsonLocal["id"] == elementId:
            return jsonLocal
        for key, value in jsonLocal.items():
            result = findElementById(value, elementId)
            if result is not None:
                return result
    elif isinstance(jsonLocal, list):
        for item in jsonLocal:
            result = findElementById(item, elementId)
            if result is not None:
                return result
    return None

def find_element(json_local: dict, widget_type: str, position: int = 0) -> dict | None:
    # Buscamos todos los elementos del tipo widgetType
    count = 0
    for section in json_local["content"]:
        for element in section["elements"]:
            if element.get("widgetType") == widget_type:
                if count == position:
                    return element
                count += 1
    return None