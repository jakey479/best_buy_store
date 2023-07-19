from create_classes import classes
from helper_functions import helpers
from typing import Optional, Tuple

PRODUCT_LIST = [classes.Product("MacBook Air M2", price=1450, quantity=100),
                classes.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                classes.Product("Google Pixel 7", price=500, quantity=250),
                classes.NonPhysicalProduct("Windows License", price=125),
                classes.LimitedProduct("Shipping", price=10, quantity=250, max_per_order=1)
                ]

thirty_percent = classes.PercentageOffPromo("30% off!", discount_percentage=30)
second_one_free = classes.Buy2Get1FreePromo("Second One Free!")
second_half_price = classes.HalfOffSecondItemPromo("Second Half price!")


PRODUCT_LIST[0].set_promotion(thirty_percent)
PRODUCT_LIST[1].set_promotion(second_one_free)
PRODUCT_LIST[2].set_promotion(second_half_price)


BEST_BUY = classes.Store(PRODUCT_LIST)


def show_interface():
    """
    display user options to the user
    :return:
    """
    print('''
1. List all products in store
2. Show total amount in store
3. Make an order
4. Quit
''')


def return_user_input() -> int:
    """
    listener loop which runs until a valid response is entered by the user
    :return:
    """
    valid_response = False
    while not valid_response:
        user_input = input('Please enter an option: ')
        if user_input not in ['1', '2', '3', '4']:
            continue
        return int(user_input)


def return_user_order_and_quantity() -> Optional[Tuple[classes.Product, int]]:
    """
    return product object and order quantity if user order corresponds to a valid product object identifier.
    Else return None.
    :return:
    """
    store_inventory = BEST_BUY.create_store_inventory()
    valid_input = False
    while not valid_input:
        BEST_BUY.print_active_store_inventory(store_inventory)
        print('\n*** To exit out of order enter, leave order and quantity options empty ***')
        user_order = input('\nWhich item number would you like to order: ')
        user_order_quantity = input('\nHow many would you like to order: ')
        if not user_order and not user_order_quantity:
            return None
        is_valid_order = helpers.is_user_order_valid(store_inventory, user_order)
        if is_valid_order and user_order_quantity.isnumeric():
            return store_inventory[int(user_order)], int(user_order_quantity)
        print('\n*** PLEASE ENTER A VALID ORDER AND ORDER QUANTITY OR ELSE EXIT ORDER ***')
        continue


def run_store():
    store_inventory = BEST_BUY.create_store_inventory()
    valid_response = False
    for product in BEST_BUY.products:
        product.activate_product()
    while not valid_response:
        show_interface()
        user_input = return_user_input()
        if user_input == 1:
            BEST_BUY.print_active_store_inventory(store_inventory)
        elif user_input == 2:
            print(f'\nThere are {BEST_BUY.get_total_quantity()} items in the store!')
        elif user_input == 3:
            exit_order = False
            while not exit_order:
                user_response = return_user_order_and_quantity()
                if not user_response:
                    break
                user_order, user_order_quantity = user_response
                order_response = BEST_BUY.order([(user_order, user_order_quantity)])
                if not order_response:
                    continue
                print(f'\norder total is ${order_response}')
        elif user_input == 4:
            print('\nSee you next time!\n')
            break
