def is_list(argument):
    if type(argument) is list:
        return True
    return False


def is_input_in_inventory(store_inventory, user_input):
    store_inventory_numbers = [item_number for item_number in store_inventory]
    if user_input in store_inventory_numbers:
        return True
    return False


def validate_user_order_and_quantity(store_inventory, user_order, user_order_quantity):
    if not user_order and not user_order_quantity:
        return False
    if user_order.isnumeric() and user_order_quantity.isnumeric():
        user_order_in_inventory = is_input_in_inventory(store_inventory, int(user_order))
        if user_order_in_inventory:
            product = store_inventory[int(user_order)]
            product_quantity = int(user_order_quantity)
            return product, product_quantity
    return '\n*** PLEASE ENTER A VALID ORDER AND ORDER QUANTITY OR ELSE EXIT ORDER ***'



