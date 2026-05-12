from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Таблица 7 – OrderStatuses
class OrderStatus(models.Model):
    id_status = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'OrderStatuses'
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'

# Таблица 1 – Users
class User(models.Model):
    ROLE_BUYER = 'buyer'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_BUYER, 'Покупатель'),
        (ROLE_ADMIN, 'Администратор'),
    ]

    id_user = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_BUYER)

    class Meta:
        db_table = 'Users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

# Таблица 3 – Categories
class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    id_parent_category = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, db_column='id_parent_category'
    )

    class Meta:
        db_table = 'Categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

# Таблица 2 – Products
class Product(models.Model):
    id_product = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField(default=1)
    stock_quantity = models.PositiveIntegerField(default=0)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='id_category')
    image_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'Products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

# Таблица 8 – Cart
class Cart(models.Model):
    id_cart = models.AutoField(primary_key=True)
    id_user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='id_user')

    class Meta:
        db_table = 'Carts'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

# Таблица 4 – Cities
class City(models.Model):
    id_city = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Cities'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

# Таблица 5 – Addresses
class Address(models.Model):
    id_address = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user')
    id_city = models.ForeignKey(City, on_delete=models.CASCADE, db_column='id_city')
    street = models.CharField(max_length=255) 
    apartment = models.CharField(max_length=20, null=True, blank=True) 

    class Meta:
        db_table = 'Addresses'
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

# Таблица 6 – Orders
class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user')
    id_address = models.ForeignKey(Address, on_delete=models.CASCADE, db_column='id_address')
    total_cost = models.PositiveIntegerField(default=0)
    id_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, db_column='id_status')
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    id_order_item = models.AutoField(primary_key=True)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='id_order')
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='id_product')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'OrderItems'
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

# Таблица 9 – Reviews
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user')
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='id_product')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)
    review_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='rating_between_1_and_5'
            )
        ]
    
class CartItem(models.Model):
    id_cart_item = models.AutoField(primary_key=True)
    id_cart = models.ForeignKey(Cart, on_delete=models.CASCADE, db_column='id_cart')
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='id_product')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'CartItems'
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'


class AttributeDefinition(models.Model):
    VALUE_TYPE_ENUM = 'enum'
    VALUE_TYPE_NUMBER = 'number'
    VALUE_TYPE_STRING = 'string'
    VALUE_TYPE_BOOLEAN = 'boolean'
    VALUE_TYPE_CHOICES = [
        (VALUE_TYPE_ENUM, 'Справочник (enum)'),
        (VALUE_TYPE_NUMBER, 'Число'),
        (VALUE_TYPE_STRING, 'Строка'),
        (VALUE_TYPE_BOOLEAN, 'Булево'),
    ]

    id_attribute = models.AutoField(primary_key=True)
    attribute_code = models.CharField(max_length=50, unique=True)
    attribute_name = models.CharField(max_length=100)
    value_type = models.CharField(max_length=20, choices=VALUE_TYPE_CHOICES, default=VALUE_TYPE_ENUM)
    unit = models.CharField(max_length=20, null=True, blank=True)
    is_filterable = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'AttributeDefinitions'
        verbose_name = 'Определение атрибута'
        verbose_name_plural = 'Определения атрибутов'


class AttributeOption(models.Model):
    id_option = models.AutoField(primary_key=True)
    id_attribute = models.ForeignKey(AttributeDefinition, on_delete=models.CASCADE, db_column='id_attribute')
    option_value = models.CharField(max_length=120)
    sort_order = models.PositiveSmallIntegerField(default=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'AttributeOptions'
        verbose_name = 'Вариант атрибута'
        verbose_name_plural = 'Варианты атрибутов'


class CategoryAttributeMap(models.Model):
    id_category_attribute_map = models.AutoField(primary_key=True)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='id_category')
    id_attribute = models.ForeignKey(AttributeDefinition, on_delete=models.CASCADE, db_column='id_attribute')
    step_order = models.PositiveSmallIntegerField(null=True, blank=True)
    is_required = models.BooleanField(default=False)
    is_filterable_override = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'CategoryAttributeMap'
        verbose_name = 'Связь категории и атрибута'
        verbose_name_plural = 'Связи категорий и атрибутов'


class ProductAttributeValue(models.Model):
    id_product_attribute_value = models.AutoField(primary_key=True)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='id_product')
    id_attribute = models.ForeignKey(AttributeDefinition, on_delete=models.CASCADE, db_column='id_attribute')
    id_option = models.ForeignKey(
        AttributeOption,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_option'
    )
    value_string = models.CharField(max_length=255, null=True, blank=True)
    value_number = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    value_boolean = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = 'ProductAttributeValues'
        verbose_name = 'Значение атрибута товара'
        verbose_name_plural = 'Значения атрибутов товаров'