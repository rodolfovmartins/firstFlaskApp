from datetime import datetime
from model.Product import Product

class ProductController():

    def __init__(self):
        self.product_model = Product()

    def save_product(self, obj):
        self.product_model.name = obj['name']
        self.product_model.description = obj['description']
        self.product_model.qtd = obj['qtd']
        self.product_model.price = obj['price']
        self.product_model.date_created = datetime.now()
        self.product_model.last_updated = datetime.now()
        self.product_model.status = True
        self.product_model.category = obj['category']
        self.product_model.user_created = obj['user_created']

        self.product_model.save()