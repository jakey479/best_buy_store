from create_classes import classes
from helper_functions import helpers

PRODUCT_LIST = [classes.Product("MacBook Air M2", price=1450, quantity=100),
                classes.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                classes.Product("Google Pixel 7", price=500, quantity=250)
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
        if not user_order and not user_order_quantity:
            #this one will not return an error
            return False, False
        if user_order.isnumeric() and user_order_quantity.isnumeric():
            user_order_in_inventory = helpers.is_input_in_inventory(store_inventory, int(user_order))
            if user_order_in_inventory:
                product = store_inventory[int(user_order)]
                product_quantity = int(user_order_quantity)
                return product, product_quantity
            else:
                print('\n*** PLEASE ENTER A VALID ORDER AND ORDER QUANTITY OR ELSE EXIT ORDER ***')
                continue
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
            BEST_BUY.print_store_inventory(store_inventory)
        elif user_input == 2:
            print(f'\nThere are {BEST_BUY.get_total_quantity()} items in the store!')
        elif user_input == 3:
            exit_order = False
            while not exit_order:
                user_order, user_order_quantity = return_user_order_and_quantity()
                if not all([user_order, user_order_quantity]):
                    break
                print(f'\nOrder purchase total is: {BEST_BUY.order([(user_order, user_order_quantity)])}')
        elif user_input == 4:
            print('\nSee you next time!\n')
            break
