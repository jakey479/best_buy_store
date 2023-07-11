from create_classes import classes
from helper_functions import helpers

PRODUCT_LIST = [classes.Product("MacBook Air M2", price=1450, quantity=100),
                classes.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                classes.Product("Google Pixel 7", price=500, quantity=250),
                classes.NonPhysicalProduct("Windows License", price=125),
                classes.LimitedProduct("Shipping", price=10, quantity=250, max_per_order=1)
               ]
BEST_BUY = classes.Store(PRODUCT_LIST)


def show_interface():
    print('''
1. List all products in store
2. Show total amount in store
3. Make an order
4. Quit
''')


def return_user_input():
    valid_response = False
    while not valid_response:
        user_input = input('Please enter an option: ')
        if user_input not in ['1', '2', '3', '4']:
            continue
        return int(user_input)


def return_user_order_and_quantity():
    store_inventory = BEST_BUY.create_store_inventory()
    valid_input = False
    while not valid_input:
        BEST_BUY.print_store_inventory(store_inventory)
        print('\n*** To exit out of order enter, leave order and quantity options empty ***')
        user_order = input('\nWhich item number would you like to order: ')
        user_order_quantity = input('\nHow many would you like to order: ')
        user_order_resp = helpers.validate_user_order_and_quantity(store_inventory, user_order, user_order_quantity)
        if not user_order_resp:
            return None
        return user_order_resp


def run_store():
    store_inventory = BEST_BUY.create_store_inventory()
    valid_response = False
    for product in BEST_BUY.products:
        product.activate_product()
    while not valid_response:
        show_interface()
        user_input = return_user_input()
        if user_input == 1:
            BEST_BUY.print_store_inventory(store_inventory)
        elif user_input == 2:
            print(f'\nThere are {BEST_BUY.get_total_quantity()} items in the store!')
        elif user_input == 3:
            exit_order = False
            while not exit_order:
                user_response = return_user_order_and_quantity()
                if not user_response:
                    break
                if type(user_response) == str:
                    print(user_response)
                    continue
                user_order, user_order_quantity = user_response
                order_response = BEST_BUY.order([(user_order, user_order_quantity)])
                if not order_response:
                    continue
                print(f'\norder total is ${order_response}')
        elif user_input == 4:
            print('\nSee you next time!\n')
            break
