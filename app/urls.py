
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from . forms import LoginForm,MyPasswordChangeForm,MySetPasswordForm,MyPasswordResetForm
from .forms import LoginForm
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.hello),
    path('women/',views.drop),
    path('men/',views.men),
   
    path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path("category-title/<val>",views.CategoryTitle.as_view(),name="category-title"),
    path("product-detail/<int:pk>",views.ProductDetail.as_view(),name="product-detail"),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('updateAddress/<int:pk>',views.updateAddress.as_view(),name='updateAddress'),
    path('updateAddress/<int:pk>',views.updateAddress.as_view(),name='updateAddress'),

    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('orders/',views.orders,name='orders'),
    
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('pluswishlist/<int:id>',views.plus_wishlist),
    path('minuswishlist/<int:id>/',views.minus_wishlist),
    path('wishlist/',views.show_wishlist,name='showwishlist'),

    #path('add-wishlist',views.add_wishlist,name='add_wishlist'),
    path('searchbar/',views.searchbar),
    path('search/',views.search,name='search'),

    #login authentication
    path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('account/login/',auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('logout/',auth_view.LoginView.as_view(next_page='login'),name='logout'),
    #path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    #path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    #path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    #path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),

    
    path('send_otp/', views.send_otp, name='send_otp'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('password-reset/',views.password_reset,name='password_reset'),
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    #path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    #path('password-reset-complete/',views.pwcomplete,name='password_reset_complete'),
    # Add URL patterns for the password reset views here


    #path('password_reset/', auth_views.PasswordResetView.as_view(form_class=MyPasswordResetForm), name='password_reset'),
    #path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header = "KAARLAH CLOTHING STORE"
admin.site.site_title = "KAARLAH CLOTHING STORE"
admin.site.index_title = "WELCOME TO KAARLAH"
