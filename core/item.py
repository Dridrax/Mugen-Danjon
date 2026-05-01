from core.data.items import ITEMS

class Item:
    def __init__(self, item_id):
        data = ITEMS[item_id]

        self.id = item_id
        self.nombre = data["nombre"]
        self.tipo = data["tipo"]

        # Opcionales
        self.efecto = data.get("efecto", {})
        self.stats = data.get("stats", {})
        self.valor = data.get("valor", 0)