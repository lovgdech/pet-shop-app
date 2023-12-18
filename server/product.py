import json


class Product:
    def __init__(
        self,
        id,
        productId,
        productGroupId,
        name,
        title,
        desciption,
        image,
        price,
        quanlity,
        enable,
        note,
    ):
        self.id = id
        self.productId = productId
        self.productGroupId = productGroupId
        self.name = name
        self.title = title
        self.desciption = desciption
        self.image = image
        self.price = price
        self.quanlity = quanlity
        self.enable = enable
        self.note = note


class ProductEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Product):
            return obj.__dict__
        return super().default(obj)


def convertCustoms(arr):
    productsList = []
    for e in arr:
        newProduct = Product(
            e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8], e[9], e[10]
        )

        product_json = json.dumps(newProduct, cls=ProductEncoder)

        productsList.append(product_json)

    return productsList
