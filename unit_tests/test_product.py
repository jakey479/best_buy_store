import os
import sys
import pytest

# Appending the root directory of this project to the sys.path so that it can call
# sibling packages
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(ROOT_DIR)

from best_buy_store.create_classes import classes


def test_instance_variable_exceptions():
    with pytest.raises(ValueError):
        product = classes.Product('', 100, 100)


def test_create_normal_product():
    product1 = classes.Product('a_product', 100, 100)
    assert product1.price and product1.name and product1.quantity


def test_product_becomes_inactive():
    product1 = classes.Product('a_product', 100, 100)
    product1.activate_product()
    product1.buy(100)
    assert product1.is_active is False


def test_buy_product_returns_correct_output():
    product1 = classes.Product('a_product', 100, 100)
    product1.activate_product()
    assert product1.buy(50) == product1.price * 50


def test_buy_product_reduces_product_quantity():
    product1 = classes.Product('a_product', 100, 100)
    print(product1)
    product1.activate_product()
    product1.buy(50)
    assert product1.get_quantity() == 50


def test_buy_more_than_product_inventory():
    product1 = classes.Product('a_product', 100, 100)
    product1.activate_product()
    assert product1.buy(101) is None


pytest.main()
