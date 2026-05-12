from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import (
    Category,
    Product,
    User,
    Order,
    OrderStatus,
    City,
    Address,
    Cart,
    Review,
    CartItem,
    OrderItem,
    AttributeDefinition,
    AttributeOption,
    CategoryAttributeMap,
    ProductAttributeValue,
)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderStatus)
admin.site.register(OrderItem)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(AttributeDefinition)
admin.site.register(AttributeOption)
admin.site.register(CategoryAttributeMap)
admin.site.register(ProductAttributeValue)

# Скрываем встроенные модели авторизации из админки.
for model in (Group, get_user_model()):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass