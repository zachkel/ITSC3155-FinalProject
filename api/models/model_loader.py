from . import customer, menu_items, orders, payment, promotion, reviews

from ..dependencies.database import engine


def index():
    customer.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    orders.Base.metadata.create_all(engine)
    payment.Base.metadata.create_all(engine)
    promotion.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
