class Product:
    def __init__(self, sku, name, description, price, stock_quantity, is_active=True, id=None):
        self.sku = sku
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.is_active = is_active
        self.id = id

    def to_dict(self):
        data = {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock_quantity": self.stock_quantity,
            "is_active": self.is_active
        }
        # Remove id if None for backward compatibility
        if self.id is None:
            data.pop("id")
        return data
