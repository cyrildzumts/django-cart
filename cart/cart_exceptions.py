
class QuantityError(Exception):
    def __init__(self, available, value):
        self.message = "Quantity Error.\n\
            Quantity Available = %d\n\
            Quantity Requested %d\n" % (available, value)

    def __str__(self):
        return self.message


class ProductNotAvailableError(Exception):
    def __init__(self, product_name):
        self.message = "The product %s is not available" % (product_name)

    def __str__(self):
        return self.message
