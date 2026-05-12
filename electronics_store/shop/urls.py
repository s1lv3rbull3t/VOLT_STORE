from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('manager/product/<int:product_id>/update/', views.manager_update_product, name='manager_update_product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart/item/<int:product_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/analytics/export/xlsx/', views.manager_export_analytics_xlsx, name='manager_export_analytics_xlsx'),
    path('manager/analytics/template/xlsx/', views.manager_analytics_template_xlsx, name='manager_analytics_template_xlsx'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/update-field/', views.profile_update_field, name='profile_update_field'),
    path('profile/confirm-email/<path:token>/', views.confirm_profile_email_change, name='confirm_profile_email_change'),
    path('register/', views.register, name='register'),
    path('restore/', views.restore, name='restore'),
    path('activate/<path:token>/', views.activate_account, name='activate_account'),
    path('reset-password/<path:token>/', views.reset_password_confirm, name='reset_password_confirm'),
]