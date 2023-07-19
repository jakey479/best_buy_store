from abc import ABC, abstractmethod
import decimal

import os
import sys

# Appending the root directory of this project to the sys.path so that it can call
# sibling packages
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from best_buy_store.helper_functions import helpers


class Promotion(ABC):
    """
    set up default methods for promotion cubclass
    """
    def __init__(self, promotion_type):
        self.promotion_type = promotion_type

    @abstractmethod
    def apply_promotion(self, product, quantity):
        pass


class PercentageOffPromo(Promotion):

    def __init__(self, promotion_type, discount_percentage):
        super().__init__(promotion_type)
        self.discount_percentage = discount_percentage

    def apply_promotion(self, product, quantity):
        discounted_price = helpers.return_discount_price(self.discount_percentage, product.price)
        return float(discounted_price * quantity)


class Buy2Get1FreePromo(Promotion):
    def apply_promotion(self, product, quantity):
        price_with_discount = 0
        if quantity >= 2:
            last_number_in_range = list(range(1, quantity + 1))[-1]
            for count in range(1, quantity + 1):
                if count % 2 == 0:
                    price_with_discount += product.price
            if last_number_in_range % 2 == 1:
                price_with_discount += product.price
            return price_with_discount
        price_with_discount += product.price
        return price_with_discount


class HalfOffSecondItemPromo(Promotion):

    def apply_promotion(self, product, quantity):
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        price_with_discount = 0
        if quantity >= 2:
            for count in range(1, quantity + 1):
                if count % 2 == 1:
                    price_with_discount += product.price
                    price_with_discount = float(round(decimal.Decimal(str(price_with_discount)), 2))
                if count % 2 == 0:
                    price_with_discount += helpers.return_discount_price(50, product.price)
            return price_with_discount
        price_with_discount += product.price
        return price_with_discount


class Product:
    def __init__(self, name, price, quantity):
        if not name:
            raise ValueError('Please remember to initialize a valid name')
        elif quantity < 0 or price < 0:
            raise ValueError('Please don\'t initialize with negative numbers')
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
        self.is_active = False
        self.promotion = None

    def set_promotion(self, promotion):
        self.promotion = promotion

    def get_promotion(self):
        return self.promotion

    def get_quantity(self) -> float:
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity

    def activate_product(self):
        self.is_active = True

    def deactivate_product(self):
        self.is_active = False

    def show_self(self) -> str:
        if self.promotion:
            return f'{self.name}, price: {self.price}, quantity: {self.quantity}, promotion: {self.promotion.promotion_type}'
        return f'{self.name}, price: {self.price}, quantity: {self.quantity}'

    def check_if_active(self) -> bool:
        return self.is_active

    def return_total_price(self, quantity):
        return self.price * quantity

    def buy(self, quantity):
        if quantity <= self.get_quantity() and self.check_if_active():
            self.quantity -= quantity
            if self.quantity == 0:
                self.is_active = False
            if self.promotion:
                return self.promotion.apply_promotion(self, quantity)
            return Product.return_total_price(self, quantity)
        elif quantity > self.get_quantity():
            print(f'\nYOU ARE TRYING TO BUY MORE THAN WE HAVE IN STOCK. PLEASE BUY AN AMOUNT LESS THAN OR EQUAL TO {self.quantity}')
            return
        print('Please tell the store to activate this product first')
        return


class NonPhysicalProduct(Product):
    def __init__(self, name, price, quantity=0):
        super().__init__(name, price, quantity)

    def show_self(self) -> str:
        return f'{self.name}, price: {self.price}, quantity: Unlimited!'

    def buy(self, quantity):
        return Product.return_total_price(self, quantity)


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, max_per_order):
        super().__init__(name, price, quantity)
        self.max_per_order = max_per_order

    def show_self(self) -> str:
        if self.max_per_order == 0:
            return f'{self.name}, price: {self.price}, quantity: {self.quantity},' \
               f' Max order limit reached'

        return f'{self.name}, price: {self.price}, quantity: {self.quantity},' \
               f' Only {self.max_per_order} available per order'

    def buy(self, quantity):
        if quantity <= self.max_per_order and self.check_if_active():
            self.quantity -= quantity
            self.max_per_order -= quantity
            if self.max_per_order == 0:
                self.is_active = False
            return Product.return_total_price(self, quantity)
        elif quantity > self.max_per_order:
            print(f'\nIneligible to add to order')
            return
        print('Please tell the store to activate this product first')
        return


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
                return
            total_price += returned_order
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
