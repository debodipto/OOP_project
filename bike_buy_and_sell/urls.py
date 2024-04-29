from django.urls import path

from bike_buy_and_sell import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('registration/', views.SignUpView.as_view(), name='registration'),
    path('change-password/', views.change_password, name='change_password'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    path('contact-us/', views.contact_view, name='contact'),
    path('booking_list/', views.booking_list, name='booking_list'),
    path('buy_list/', views.buy_list, name='buy_list'),
    path('sell', views.sell_views, name='sell'),
    path('sell_list', views.sell_list, name='sell_list'),

    path('add-to-cart/<int:product_id>', views.add_to_cart_view, name='cart_add'),
    path('bike-details/<int:id>/', views.product_detail, name='product_detail'),
    path('cart-details/', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),

    path('checkout/', views.order_create, name='order_create'),
    path('my-order-details/<int:order_id>/', views.order_details, name='order_details'),

    path('search', views.search_view, name='search'),
    path('category_based_bike/<int:category_id>/', views.category_based_bike, name='category_based_bike'),
]
