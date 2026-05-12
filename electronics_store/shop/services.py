from datetime import date
import random
import re
from django.db.models import Q, Sum, Case, When, Value, IntegerField

from .models import Product, Category, Cart, CartItem, User, OrderItem


CATEGORY_IMAGE_MAP = {
    'Смартфоны и гаджеты': 'https://aljomhuria.com/wp-content/uploads/2024/01/APPLE_IPHONE_THE_BEST_NEWS.jpg',
    'Ноутбуки': 'https://avatars.mds.yandex.net/i?id=8d69629aaf562508c25949b6f417f61c_l-5337489-images-thumbs&n=13',
    'ТВ и консоли': 'https://sun9-87.userapi.com/s/v1/ig2/LC7QE3w7xnBQXnJaTznNaC98bDvaA0Ner1cRlgKuw3PeNDe9Cl2rc-tSRrtNXbqBUj4-xxzeIwqED_Pqa_U6i-eD.jpg?quality=95&crop=0,0,1920,1078&as=32x18,48x27,72x40,108x61,160x90,240x135,360x202,480x269,540x303,640x359,720x404,1080x606,1280x719,1440x808,1920x1078&from=bu&u=ilGG6Q1jtLw0VC6cuTEcT88dLAB1dLR60zFu-KoxjOQ&cs=1920x0',
    'Наушники и аудио': 'https://avatars.mds.yandex.net/i?id=afe421b62c22826afa644b23e343219a_l-6978923-images-thumbs&n=13',
    'Аксессуары': 'https://postavkioptom.by/wp-content/uploads/2024/10/dizajn-bez-nazvaniya-32-1-768x512.jpg',
    'Смартфоны': 'https://wylsa.com/wp-content/uploads/2025/06/huawei-pura80.jpeg',
    'Кнопочные телефоны': 'https://mlwngexlqpag.i.optimole.com/w:1920/h:1080/q:mauto/f:best/https://designwith.love/wp-content/uploads/2017/11/just5-colors-stiven-skyrah-designwithlove-stivenskyrah.jpg',
    'Умные часы': 'https://avatars.mds.yandex.net/i?id=ea3810ae25c8c7d9e4b1df80ee572185_l-4394910-images-thumbs&n=13',
    'Смарт часы': 'https://astmarket.com/upload/resize_cache/iblock/93b/dnh1w1phkwhkcxrk0m3yh1935uq6q4h5/560_1000_1/0218f82b_7e9b_11f0_a7cc_00155d140308.png',
    'Фитнес-браслеты': 'https://static.beeline.ru/shop/media/goods/fullsize/394bdab4-8ae0-4a1f-97ef-024f089168fe.jpg',
    'Раскладушки': 'https://www.dgl.ru/wp-content/uploads/2023/05/nokia-2660-flip-1.jpg',
    'Моноблоки': 'https://avatars.mds.yandex.net/i?id=0333d59d99d1841fee3ea8bc1f2097e3_l-5235483-images-thumbs&n=13',
    'Apple Iphone': 'https://kotofoto.ru/product_img/69/679021/679021_smartfon_apple_iphone_16_pro_max_1tb_myw23za_a_natural_titanium_10m.jpg?v=1727256010',
    'Прочие android-смартфоны': 'https://avatars.mds.yandex.net/i?id=6f81afaed6866d59519dda3e3e39c82c_l-4576832-images-thumbs&n=13',
    'Для компьютеров': 'https://avatars.mds.yandex.net/get-mpic/11740777/2a00000192b936077355284cd4550a087e69/orig',
    'Для телефонов': 'https://wylsa.com/wp-content/uploads/2020/06/letnie-chehly-apple-3.jpg',
    'Кабели и зарядки': 'https://avatars.mds.yandex.net/i?id=e3f4f23dc67911ad10d53e80a47f280e_l-9151019-images-thumbs&n=13',
    'Клавиатуры': 'https://pics.computerbase.de/2/7/9/7/1/1-1080.601511860.jpg',
    'Коврики': 'https://pics.computerbase.de/8/1/3/0/8/4-1080.4277776392.jpg',
    'Мыши': 'https://st.overclockers.ru/legacy/blog/360526/138335_O.jpg',
    'Сумки для ноутбуков': 'https://img.alicdn.com/imgextra/i1/6000000007050/O1CN01vnb2Jv21www9g7qFR_!!6000000007050-0-tbvideo.jpg',
    'Защитные стекла': 'https://asiastore.kg/image/cache/catalog/accessories/for-iphone/ubear/ubearglass/iphone14pro14promax/sftedsx0-1920x1080.jpeg',
    'Чехлы': 'https://avatars.mds.yandex.net/i?id=a90860e124039489392b453298fefbbd_l-4578672-images-thumbs&n=13',
    'Power Bank': 'https://static1.pocketlintimages.com/wordpress/wp-content/uploads/2024/07/pxwaxpy-36800mah-2.jpg',
    'Кабели': 'https://avatars.mds.yandex.net/i?id=e3f4f23dc67911ad10d53e80a47f280e_l-9151019-images-thumbs&n=13',
    'Зарядные блоки': 'https://avatars.mds.yandex.net/i?id=3b9debe1e33f3889fb06f3b0a93eb0d3_l-5233928-images-thumbs&n=13',
    'Беспроводные наушники': 'https://img.odcdn.com.br/wp-content/uploads/2025/08/Samsung-Galaxy-Buds-3-Pro.jpg',
    'Колонки': 'https://avatars.mds.yandex.net/i?id=e02714332e1e0030d3c7cfb646bf54fd_l-12884907-images-thumbs&n=13',
    'Проводные наушники': 'https://cdn2.singteldigital.com/content/dam/singtel/personal/products-services/devices-and-gadgets/earbuds-vs-headphones-for-gaming/jbl-quantum-50.png',
    'TWS': 'https://avatars.mds.yandex.net/i?id=ddbf2535c93cd761e0f699e5a31c40eb_l-3685366-images-thumbs&n=13',
    'Накладные': 'https://avatars.mds.yandex.net/i?id=3d7c7117aa08fe619de732356da9c0c71b30503f-8484564-images-thumbs&n=13',
    'Беспроводные колонки': 'https://reveltime.storage.yandexcloud.net/d8/fields/2023/колонка.jpg',
    'Проводные колонки': 'https://avatars.mds.yandex.net/i?id=386d8f84c0c9a795659d3dc5fd49bd88_l-5695679-images-thumbs&n=13',
    'Для игр': 'https://pultovik-optom.ru/wp-content/uploads/2025/06/8d15efbd532d11f0bf2dd85ed3a25ab2_764d5478783c11f0bf53d85ed3a25ab2.jpg',
    'Повседневные': 'https://onecms-res.cloudinary.com/image/upload/v1710231847/mediacorp/8days/image/2024/03/12/1more.jpg',
    'Студийные': 'https://calcopia.com/wp-content/uploads/2025/09/audeze_mm100_2025_featured.jpg',
    'Игровые ноутбуки': 'https://www.androidauthority.com/wp-content/uploads/2019/04/Predator-Helios-700_PH717-17_05.jpg',
    'Ультрабуки': 'https://www.lydogbillede.dk/wp-content/uploads/2022/01/dell-xps-13.jpg',
    'Трансформеры': 'https://www.newgadgets.de/uploads/2017/05/ASUS-ZenBook-Flip-S-UX370-2-e1496039252604.jpg',
    'Игровые консоли': 'https://assetsio.gnwcdn.com/xbox-series-s-1tb-black.jpg',
    'Телевизоры': 'https://cdn.mos.cms.futurecdn.net/aeUgyn7ryXTTqv68B2BeMD.jpg',
    'Nintendo Switch': 'https://avatars.mds.yandex.net/get-mpic/4887676/2a00000191c841e0b0bf316e7ab4d1322198/orig',
    'PlayStation 5': 'https://avatars.mds.yandex.net/i?id=63e2a123d55cb473ab5c110515c0111104c1c324-5276739-images-thumbs&n=13',
    'Xbox Series X/S': 'https://cdn.mos.cms.futurecdn.net/fZWW92moDpHLp5dqeVdHNN.jpg',
    'Телевизоры 32"-43"': 'https://main-cdn.sbermegamarket.ru/big1/hlr-system/-18/018/196/591/021/116/600022441949b0.jpg',
    'Телевизоры 50"-55"': 'https://avatars.mds.yandex.net/i?id=f8d56106564f6eee22777606c7a1bc68_l-4859680-images-thumbs&n=13',
    'Телевизоры 65" и больше': 'https://cdn.mos.cms.futurecdn.net/aeUgyn7ryXTTqv68B2BeMD.jpg',
    'Безопасность': 'https://ecoonline.s3.amazonaws.com/uploads/2023/05/protect-main.webp',
    'Климат': 'https://www.difel-hvacfactory.com/uploads/42970/list/n2025041811394617e80.jpg',
    'Комфорт': 'https://avatars.mds.yandex.net/i?id=c6fe7221258fa3d58fe5387d90c52b34_l-7756591-images-thumbs&n=13',
    'Освещение': 'https://www.frandroid.com/wp-content/uploads/2019/07/kit-philips-hue.jpg',
    'Умные колонки': 'https://avatars.mds.yandex.net/i?id=8a4328da0e9bd2905fcea1e00d28c87c51862726-6498965-images-thumbs&n=13',
    'Samsung Galaxy': 'https://world-devices.ru/image/cache/catalog/s25_ultra/ScreenShot_20250123011657-500x400.jpeg',
    'Планшеты': 'https://via.placeholder.com/400x300?text=%D0%9F%D0%BB%D0%B0%D0%BD%D1%88%D0%B5%D1%82%D1%8B',
    'Умный дом': 'https://mobistore.by/files/uploads/Yandex_Station/21616f60dd2f86540fb52f7a836cd541.png'
}
DEFAULT_CATEGORY_IMAGE = 'https://via.placeholder.com/400x300?text=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F'

SEARCH_SYNONYMS = {
    'айфон': ['iphone', 'айфон', 'айфоны', 'эппл', 'apple'],
    'айфоны': ['iphone', 'айфон', 'айфоны', 'эппл', 'apple'],
    'iphone': ['iphone', 'айфон', 'айфоны', 'эппл', 'apple'],
    'самсунг': ['samsung', 'самсунг', 'самсунги', 'galaxy'],
    'самсунги': ['samsung', 'самсунг', 'самсунги', 'galaxy'],
    'samsung': ['samsung', 'самсунг', 'самсунги', 'galaxy'],
    'андроид': ['android', 'андроид', 'андроиды', 'android-смартфоны'],
    'андроиды': ['android', 'андроид', 'андроиды', 'android-смартфоны'],
    'android': ['android', 'андроид', 'андроиды', 'android-смартфоны'],
    'кабель': ['кабель', 'кабели', 'cable', 'зарядка', 'зарядки'],
    'кабели': ['кабель', 'кабели', 'cable', 'зарядка', 'зарядки'],
    'зарядка': ['зарядка', 'зарядки', 'зарядку', 'зарядное', 'зарядные', 'charger', 'charging'],
    'зарядки': ['зарядка', 'зарядки', 'зарядку', 'зарядное', 'зарядные', 'charger', 'charging'],
    'зарядку': ['зарядка', 'зарядки', 'зарядку', 'зарядное', 'зарядные', 'charger', 'charging'],
    'колонка': ['колонка', 'колонки', 'speaker', 'speakers'],
    'колонки': ['колонка', 'колонки', 'speaker', 'speakers'],
    'наушник': ['наушник', 'наушники', 'earbuds', 'headphones'],
    'наушники': ['наушник', 'наушники', 'earbuds', 'headphones'],
}


class UserService:
    @staticmethod
    def get_user_from_session(request):
        user_id = request.session.get('user_id')
        if not user_id:
            return None
        try:
            return User.objects.get(id_user=user_id)
        except User.DoesNotExist:
            return None


class CategoryService:
    @staticmethod
    def get_root_categories():
        return Category.objects.filter(id_parent_category__isnull=True)
    
    @staticmethod
    def get_root_categories_ordered():
        return (
            Category.objects
            .filter(id_parent_category__isnull=True)
            .annotate(
                display_order=Case(
                    When(category_name='Смартфоны и гаджеты', then=Value(1)),
                    When(category_name='Ноутбуки', then=Value(2)),
                    When(category_name='ТВ и консоли', then=Value(3)),
                    When(category_name='Наушники и аудио', then=Value(4)),
                    When(category_name='Аксессуары', then=Value(5)),
                    default=Value(999),
                    output_field=IntegerField(),
                )
            )
            .order_by('display_order', 'category_name')
        )
    
    @staticmethod
    def get_subcategories(category):
        return Category.objects.filter(id_parent_category=category).order_by('category_name')
    
    @staticmethod
    def build_category_chain(category):
        chain = []
        while category is not None:
            chain.insert(0, category)
            category = category.id_parent_category
        return chain
    
    @staticmethod
    def get_category_image(category_name):
        direct_match = CATEGORY_IMAGE_MAP.get(category_name)
        if direct_match:
            return direct_match

        normalized_name = (category_name or '').strip().lower().replace('ё', 'е')
        for key, image_url in CATEGORY_IMAGE_MAP.items():
            normalized_key = key.strip().lower().replace('ё', 'е')
            if normalized_name == normalized_key:
                return image_url

        return DEFAULT_CATEGORY_IMAGE
    
    @staticmethod
    def enrich_categories_with_images(categories):
        for category in categories:
            category.card_image = CategoryService.get_category_image(category.category_name)
        return categories


class ProductService:
    @staticmethod
    def _normalize_search_token(token):
        cleaned = token.strip().lower().replace('ё', 'е')
        return re.sub(r'[^0-9a-zа-я-]+', '', cleaned)

    @staticmethod
    def _token_variants(token):
        variants = {token}
        synonyms = SEARCH_SYNONYMS.get(token, [])
        variants.update(synonyms)

        return {variant for variant in variants if variant}

    @staticmethod
    def search_products(query):
        normalized_query = (query or '').strip()
        if not normalized_query:
            return Product.objects.all()

        raw_tokens = re.split(r'\s+', normalized_query)
        tokens = [
            ProductService._normalize_search_token(token)
            for token in raw_tokens
            if ProductService._normalize_search_token(token)
        ]
        if not tokens:
            return Product.objects.all()

        strict_filter = Q()
        priority_score = Value(0, output_field=IntegerField())
        for token in tokens:
            strict_token_filter = Q()
            for variant in ProductService._token_variants(token):
                strict_token_filter |= Q(product_name__icontains=variant)
                strict_token_filter |= Q(id_category__category_name__icontains=variant)
                priority_score += Case(
                    When(product_name__iexact=variant, then=Value(120)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                priority_score += Case(
                    When(id_category__category_name__iexact=variant, then=Value(100)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                priority_score += Case(
                    When(product_name__istartswith=variant, then=Value(70)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                priority_score += Case(
                    When(id_category__category_name__istartswith=variant, then=Value(55)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                priority_score += Case(
                    When(product_name__icontains=variant, then=Value(30)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
                priority_score += Case(
                    When(id_category__category_name__icontains=variant, then=Value(20)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            strict_filter &= strict_token_filter

        return (
            Product.objects.filter(strict_filter)
            .annotate(search_priority=priority_score)
            .order_by('-search_priority', 'product_name')
            .distinct()
        )
    
    @staticmethod
    def get_daily_deals(count=3):
        all_products = list(
            Product.objects.only('id_product', 'product_name', 'price', 'image_url')
            .values_list('id_product', 'product_name', 'price', 'image_url')
        )
        if not all_products:
            return []
        
        day_seed = int(date.today().strftime("%Y%m%d"))
        random.seed(day_seed)
        
        selected_ids = [p[0] for p in random.sample(all_products, min(count, len(all_products)))]
        deals = Product.objects.filter(id_product__in=selected_ids)
        return deals
    
    @staticmethod
    def get_bestsellers(count=3):
        top_product_ids = list(
            OrderItem.objects
            .values('id_product')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity', '-id_product')[:count]
            .values_list('id_product', flat=True)
        )
        if top_product_ids:
            products_by_id = Product.objects.in_bulk(top_product_ids)
            ordered_hits = [products_by_id[pid] for pid in top_product_ids if pid in products_by_id]
            if len(ordered_hits) >= count:
                return ordered_hits
            excluded_ids = [p.id_product for p in ordered_hits]
            extra = list(
                Product.objects.exclude(id_product__in=excluded_ids)
                .order_by('-id_product')[:count - len(ordered_hits)]
            )
            ordered_hits.extend(extra)
            return ordered_hits

        return list(Product.objects.order_by('-id_product')[:count])
    
    @staticmethod
    def get_new_arrivals(count=3):
        return list(Product.objects.order_by('-id_product')[:count])
    
    @staticmethod
    def get_products_by_category(category):
        return Product.objects.filter(id_category=category)
    
    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.get(id_product=product_id)
    
    @staticmethod
    def get_product_reviews(product):
        return product.review_set.all().order_by('-review_date')


class CartService:
    @staticmethod
    def get_or_create_cart(user):
        cart, created = Cart.objects.get_or_create(id_user=user)
        return cart
    
    @staticmethod
    def get_cart_item_count(user):
        if not user:
            return 0
        
        cart = Cart.objects.filter(id_user=user).first()
        if not cart:
            return 0
        
        total_quantity = CartItem.objects.filter(id_cart=cart).aggregate(
            total=Sum('quantity')
        )['total']
        
        return total_quantity or 0
    
    @staticmethod
    def add_product_to_cart(user, product):
        cart = CartService.get_or_create_cart(user)
        cart_item, created = CartItem.objects.get_or_create(
            id_cart=cart,
            id_product=product,
            defaults={'quantity': 1}
        )
        if not created:
            max_quantity = max(product.stock_quantity, 0)
            if max_quantity <= 0:
                return cart_item
            if cart_item.quantity < max_quantity:
                cart_item.quantity += 1
                cart_item.save(update_fields=['quantity'])
        return cart_item

    @staticmethod
    def set_cart_item_quantity(user, product, quantity):
        cart = CartService.get_or_create_cart(user)
        cart_item = CartItem.objects.filter(id_cart=cart, id_product=product).first()
        if not cart_item:
            return None, 'not_in_cart'

        if quantity <= 0:
            cart_item.delete()
            return None, 'removed'

        max_quantity = max(product.stock_quantity, 0)
        if max_quantity <= 0:
            cart_item.delete()
            return None, 'out_of_stock'

        clamped_quantity = min(quantity, max_quantity)
        if clamped_quantity != cart_item.quantity:
            cart_item.quantity = clamped_quantity
            cart_item.save(update_fields=['quantity'])

        if clamped_quantity == max_quantity:
            return cart_item, 'max_reached'
        return cart_item, 'updated'

    @staticmethod
    def get_cart_item_for_product(user, product):
        if not user:
            return None
        cart = Cart.objects.filter(id_user=user).first()
        if not cart:
            return None
        return CartItem.objects.filter(id_cart=cart, id_product=product).first()
    
    @staticmethod
    def get_cart_items_with_totals(user):
        cart = Cart.objects.filter(id_user=user).first()
        
        if not cart:
            return [], 0
        
        cart_items = list(cart.cartitem_set.select_related('id_product').all())
        
        for item in cart_items:
            item.item_total = item.quantity * item.id_product.price
        
        total_cost = sum(item.item_total for item in cart_items)
        
        return cart_items, total_cost
