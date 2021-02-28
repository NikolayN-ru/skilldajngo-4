from django.urls import path
from .views import ProductList, ProductDetail, ProductSearch, PostCreate, PostUpdate, PostDelete
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, upgrade_me

urlpatterns = [

	path('<int:pk>/edit/', PostUpdate.as_view(), name='update'),
	path('create/', PostCreate.as_view(), name='create'),
	path('search/', ProductSearch.as_view(), name='search'),
	path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
	path('<int:pk>/', ProductDetail.as_view(), name='post'),
	path('login/', LoginView.as_view(template_name = 'sign/login.html'), name='login'),
	path('logout/', LogoutView.as_view(template_name = 'sign/logout.html'), name='logout'),
	path('signup/', BaseRegisterView.as_view(template_name = 'sign/signup.html'), name='signup'),
	path('upgrade/', upgrade_me, name = 'upgrade'),
	path('', ProductList.as_view(), name='head'),

]
