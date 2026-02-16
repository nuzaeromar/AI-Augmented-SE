import pytest
from src.utils import Product, add_to_cart, remove_from_cart, clear_cart, calculate_total

@pytest.fixture
def sample_product():
    return Product("Test Product", 10.0, "A test product")

@pytest.fixture
def empty_cart():
    return []

def test_add_to_cart(empty_cart, sample_product):
    add_to_cart(empty_cart, sample_product)
    assert len(empty_cart) == 1
    assert empty_cart[0] == sample_product

def test_remove_from_cart(empty_cart, sample_product):
    add_to_cart(empty_cart, sample_product)
    remove_from_cart(empty_cart, sample_product)
    assert len(empty_cart) == 0

def test_clear_cart(empty_cart, sample_product):
    add_to_cart(empty_cart, sample_product)
    clear_cart(empty_cart)
    assert len(empty_cart) == 0

def test_calculate_total(empty_cart, sample_product):
    add_to_cart(empty_cart, sample_product)
    add_to_cart(empty_cart, sample_product)
    assert calculate_total(empty_cart) == 20.0

def test_remove_nonexistent_item(empty_cart, sample_product):
    remove_from_cart(empty_cart, sample_product)
    assert len(empty_cart) == 0
