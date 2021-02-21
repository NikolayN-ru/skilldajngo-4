from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm, PostForm2
from django.urls import reverse_lazy


class PostDelete(DeleteView):
	model = Post
	template_name = 'post_delete.html'
	success_url = '/news/'
	context_object_name = 'news'


class PostUpdate(UpdateView):
	model = Post
	template_name = 'post_update.html'
	form_class = PostForm

	def get_obect(self, **kwargs):
		pk = self.kwargs.get('pk')
		return Post.objects.get(pk=pk)



class PostCreate(CreateView):
	template_name = 'post_create.html'
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
		return context

	# def post(self, request, *args, **kwargs):
	#  	form = self.form_class(request.POST)

	#  	if form.is_valid():
	#  		form.save()

	#  	return super().get(request, *args, **kwargs)
