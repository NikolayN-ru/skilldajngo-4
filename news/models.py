from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
	user = models.OneToOneField(User, max_length=100, on_delete = models.CASCADE)
	reit = models.IntegerField(default=0)

	def update_rating(self):
		pq = Post.objects.filter(author=self)
		sumr1=0
		for i in pq:
			print(i.raiting)
			sumr1 += i.raiting*3
		print(f'сумарный рейтинг каждой статьи {sumr1}')
		# сумарный рейтинг каждой статьи умножается на 3


		reit2=0
		coms = Comment.objects.filter(user=self)
		for i in coms:
			reit2 += i.raiting
		print(f'сумарный рейтинг всех комментариев автора равен {reit2}')
		# сумарный рейтинг всех комментариев автора



		reit3=0
		sumcompost = Post.objects.filter(choice='s').filter(author=self)
		# получаем кверисет из статей
		for i in sumcompost:
			t2=Comment.objects.filter(post=i)
			# получаем кверисет из коментариев
			for j in t2:
				reit3+=j.raiting
		print(f'суммарный рейтинг всех комментариев к статьям автора равен {reit3}.')
		# суммарный рейтинг всех комментариев к статьям автора

		self.reit = sumr1 + reit2 + reit3
		self.save()


	def __str__(self):
		return self.user.username


class Category(models.Model):
	category = models.CharField(max_length = 255, unique = True)

	def __str__(self):
		return self.category


class Post(models.Model):
	ch = [
	('s', 'статья'),
	('h', 'новость'),
	]
	author = models.ForeignKey(Author, on_delete = models.CASCADE, verbose_name='автор')
	choice = models.CharField(max_length=1, choices=ch, verbose_name='выбор')
	date = models.DateTimeField(auto_now=True)
	category = models.ManyToManyField(Category, verbose_name='категория')
	title = models.CharField(max_length=255, verbose_name='заголовок')
	content = models.TextField(verbose_name='контент')
	raiting = models.IntegerField(default=0)

	def like(self):
		self.raiting += 1 
		self.save()

	def dislike(self):
		self.raiting -= 1 
		self.save()

	def preview(self):
		return self.content[:124] + '...'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse ('post', kwargs={'pk':self.pk})


class PostCategory(models.Model):
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	def __str__(self):
		return self.post.title


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
	user = models.ForeignKey(Author, on_delete = models.CASCADE)
	content = models.TextField()
	created = models.DateTimeField(auto_now=True)
	raiting = models.IntegerField(default=0)

	def like(self):
		self.raiting += 1
		self.save()

	def dislike(self):
		self.raiting -= 1
		self.save()

	def __str__(self):
		return self.content
