import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.orm import (
    Base,
    ProductORM,
    OrderORM,
)


@pytest.fixture(scope="module")
def engine():
    # Create an in-memory SQLite engine for testing
    return create_engine('sqlite:///:memory:')


@pytest.fixture(scope="module")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_product(session):
    product = ProductORM(name="Test Product", quntity=10, price=99.99)

    session.add(product)
    session.commit()

    retrieved_product = session.query(ProductORM).filter_by(name="Test Product").first()
    assert retrieved_product is not None
    assert retrieved_product.name == "Test Product"
    assert retrieved_product.quntity == 10
    assert retrieved_product.price == 99.99


def test_create_order(session):
    product1 = ProductORM(name="Product 1", quntity=5, price=50.00)
    product2 = ProductORM(name="Product 2", quntity=3, price=30.00)
    session.add_all([product1, product2])
    session.commit()

    order = OrderORM(products=[product1, product2])

    session.add(order)
    session.commit()

    retrieved_order = session.query(OrderORM).filter_by(id=order.id).first()
    assert retrieved_order is not None
    assert len(retrieved_order.products) == 2
    assert retrieved_order.products[0].name == "Product 1"
    assert retrieved_order.products[1].name == "Product 2"


def test_order_product_association(session):
    product = ProductORM(name="Associated Product", quntity=7, price=70.00)
    order = OrderORM()
    order.products.append(product)
    session.add(order)
    session.commit()

    retrieved_order = session.query(OrderORM).filter_by(id=order.id).first()

    assert retrieved_order is not None
    assert len(retrieved_order.products) == 1
    assert retrieved_order.products[0].name == "Associated Product"