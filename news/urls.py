from django.urls import path
from .views import ProductList, ProductDetail, ProductSearch, PostCreate, PostUpdate, PostDelete

urlpatterns = [

	path('<int:pk>/edit/', PostUpdate.as_view(), name='update'),
	path('create/', PostCreate.as_view(), name='create'),
	path('search/', ProductSearch.as_view(), name='search'),
	path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
	path('<int:pk>/', ProductDetail.as_view(), name='post'),
	path('', ProductList.as_view(), name='head'),
]
