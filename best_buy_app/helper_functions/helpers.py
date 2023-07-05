def is_list(argument):
    if type(argument) is list:
        return True
    return False


def return_total_price(self, quantity):
    return f'Purchase total is {self.price * quantity}'


def is_input_in_inventory(store_inventory, user_input):
    store_inventory_numbers = [item_number for item_number in store_inventory]
    if user_input in store_inventory_numbers:
        return True
    return False



