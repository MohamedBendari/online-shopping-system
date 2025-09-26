class Item:
    def __init__(self, name, price, brand, model_year):
        self.name = name
        self.price = price
        self.brand = brand
        self.model_year = model_year

    def to_dict(self):
        return {"name": self.name, "price": self.price, "brand": self.brand, "model_year": self.model_year}