import os
import sys
# Appending the root directory of this project to the sys.path so that it can call
# sibling packages
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from best_buy_store.best_buy_app.helper_functions import helpers


class Product:
    def __init__(self, name, price, quantity):
        if not any([price, quantity, name]):
            raise ValueError('Please remember to initialize all values')
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
        self.is_active = False

    def get_quantity(self) -> float:
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity

    def activate_product(self):
        self.is_active = True

    def deactivate_product(self):
        self.is_active = False

    def show_self(self) -> str:
        return f'{self.name}, price: {self.price}, quantity: {self.quantity}'

    def check_if_active(self) -> bool:
        return self.is_active

    def buy(self, quantity):
        if quantity <= self.quantity and self.check_if_active():
            self.quantity -= quantity
            return helpers.return_total_price(self, quantity)
        else:
            print(f'\nYOU ARE TRYING TO BUY MORE THAN WE HAVE IN STOCK. PLEASE BUY AN AMOUNT LESS THAN OR EQUAL TO {self.quantity}')
            return False


class Store:
    def __init__(self, products):
        self.products = products

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        total_quantity = 0
        for product in self.products:
            total_quantity += product.get_quantity()
        return total_quantity

    def list_active_product_info(self):
        """must call .show method on all objects within self.products value
        :return:
        """
        product_info_list = []
        for product in self.products:
            if product.check_if_active():
                product_info_list.append(product.show_self())
        if len(product_info_list) == 0:
            return 'Store currently has no active products. Please activate products or add products to store'
        return product_info_list

    def list_active_product_objects(self):
        """must call .show method on all objects within self.products value
        :return:
        """
        active_product_list = []
        for product in self.products:
            active_product_list.append(product)
        return active_product_list

    def order(self, shopping_list):
        # Buys the products and returns the total price of the order.
        total_price = 0
        for product, order_quantity in shopping_list:
            returned_order = product.buy(order_quantity)
            if not returned_order:
                return 'not able to go through'
            total_price += product.price * order_quantity
        return total_price

    def create_store_inventory(self):
        inventory_dictionary = {}
        product_number = 0
        for inventory_object in self.products:
            inventory_dictionary[product_number] = inventory_object
            product_number += 1
        return inventory_dictionary

    def print_store_inventory(self, store_inventory):
        for product_number, product_object in store_inventory.items():
            print(f'\n{product_number}: {product_object.show_self()}')
