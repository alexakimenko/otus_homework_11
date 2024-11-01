import pytest
from unittest.mock import Mock
from domain.models import Product, Order
from domain.services import WarehouseService


@pytest.fixture
def product_repo_mock():
    return Mock()


@pytest.fixture
def order_repo_mock():
    return Mock()


@pytest.fixture
def warehouse_service(product_repo_mock, order_repo_mock):
    return WarehouseService(product_repo=product_repo_mock, order_repo=order_repo_mock)


def test_create_product(warehouse_service, product_repo_mock):
    name = "Test Product"
    quantity = 10
    price = 99.99

    product = warehouse_service.create_product(name=name, quantity=quantity, price=price)

    assert product.name == name
    assert product.quantity == quantity
    assert product.price == price
    product_repo_mock.add.assert_called_once_with(product)


def test_get_product(warehouse_service, product_repo_mock):
    product_id = 1
    expected_product = Product(id=product_id, name="Test Product", quantity=10, price=99.99)
    product_repo_mock.get.return_value = expected_product

    product = warehouse_service.get_product(product_id=product_id)

    assert product == expected_product
    product_repo_mock.get.assert_called_once_with(product_id)


def test_create_order(warehouse_service, order_repo_mock):
    products = [Product(id=1, name="Test Product 1", quantity=5, price=50.00),
                Product(id=2, name="Test Product 2", quantity=3, price=30.00)]
    expected_order = Order(id=None, products=products)
    order_repo_mock.add.return_value = expected_order

    order = warehouse_service.create_order(products=products)

    assert order.products == products
    order_repo_mock.add.assert_called_once_with(order)