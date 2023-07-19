import decimal
from typing import Union


def return_discount_price(discount_percentage: int, price):
    """
    utilize the decimal library to correctly round decimals to the proper place for monetary purposes.
    :param discount_percentage:
    :param price:
    :return:
    """
    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
    discount = price * discount_percentage / 100
    rounded_discount_amount = float(round(decimal.Decimal(str(discount)), 2))
    discounted_price = price - rounded_discount_amount
    return discounted_price


def is_list(argument: list) -> bool:
    """
    return True or False depending on whether the argument passed to the function is a list or not
    :param argument:
    :return:
    """
    if type(argument) is list:
        return True
    return False


def is_input_in_inventory(store_inventory: dict, user_input: int) -> bool:
    """
    iterates through the keys to a store_inventory dictionary and returns True if user input matches an active item
    number in store_inventory keys
    :param store_inventory:
    :param user_input:
    :return:
    """
    store_inventory_numbers = [item_number for item_number in store_inventory]
    if user_input in store_inventory_numbers:
        return True
    return False


def is_user_order_valid(store_inventory: dict, user_order: str) -> bool:
    """
    Check if user_order_in_inventory is True. If it is, and if not, return False
    :param store_inventory:
    :param user_order:
    :return:
    """
    if user_order.isnumeric():
        user_order_in_inventory = is_input_in_inventory(store_inventory, int(user_order))
        if user_order_in_inventory:
            return True
    return False



