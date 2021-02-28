from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm, PostForm2
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Post
	template_name = 'post_delete.html'
	permission_required = ('news.add_post', 'news.change_post', 'news.delete_post', )
	success_url = '/news/'
	context_object_name = 'news'


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Post
	template_name = 'post_update.html'
	permission_required = ('news.add_post', 'news.change_post', 'news.delete_post', )
	form_class = PostForm

	def get_obect(self, **kwargs):
		pk = self.kwargs.get('pk')
		return Post.objects.get(pk=pk)



class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	template_name = 'post_create.html'
	permission_required = ('news.add_post', 'news.change_post', 'news.delete_post', )
	form_class = PostForm
	success_url = reverse_lazy('head')



class ProductList(ListView):
	paginate_by = 3
	model = Post
	template_name = 'posts.html'
	context_object_name = 'products'
	queryset = Post.objects.order_by('-id')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['time_now'] = datetime.utcnow()
		context['value1'] = None
		# context = super().get_context_data(**kwargs)
		context['is_not_premium'] = not self.request.user.groups.filter(name = 'authors').exists()
		return context


class ProductDetail(DetailView):
	model = Post
	template_name = 'post.html'
	context_object_name = 'new'


class ProductSearch(ListView):
	# paginate_by = 2
	model = Post
	template_name = 'search_posts.html'
	context_object_name = 'products'
	queryset = Post.objects.order_by('-id')
	form_class = PostForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
		context['form'] = PostForm()
		# for i in context:
		# 	print(i)
		return context

	# def post(self, request, *args, **kwargs):
	#  	form = self.form_class(request.POST)

	#  	if form.is_valid():
	#  		form.save()

	#  	return super().get(request, *args, **kwargs)


from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/'

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    else:
    	premium_group.user_set.remove(user)
    return redirect('/news')
