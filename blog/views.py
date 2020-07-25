from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView
from django.utils.decorators import method_decorator
from django.utils.crypto import get_random_string

from .models import BlogPost
from .forms import CreateBlogForm


@method_decorator(login_required, name='dispatch')
class HomeView(ListView):
    model = BlogPost
    ordering = '-published_at'
    template_name = 'blog/index.html'


def generate_slug(title):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789-'
    slug = '-'.join(title.lower().split(' '))
    slug = slug + '-' + get_random_string(5, chars)
    return slug


@method_decorator(login_required, name='dispatch')
class CreateBlog(View):
    model = BlogPost
    form_class = CreateBlogForm
    template_name = 'blog/create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            # slug generate
            blog.slug = generate_slug(form.cleaned_data['title'])
            print(generate_slug(form.cleaned_data['title']))
            blog.save()
            return redirect(reverse('home'))


@method_decorator(login_required, name='dispatch')
class BlogDetailView(View):
    model = BlogPost
    template_name = 'blog/detail.html'

    def get(self, request, slug, *args, **kwargs):
        post = self.model.objects.get(slug=slug)
        print(BlogPost.objects.get(slug=slug))
        print(post)
        return render(request, self.template_name, {'post': post})


@method_decorator(login_required, name='dispatch')
class UpdateBlog(View):
    model = BlogPost
    form_class = CreateBlogForm
    template_name = 'blog/create.html'

    def get(self, request, slug, *args, **kwargs):
        post = self.model.objects.get(slug=slug)
        if request.user == post.author:
            form = self.form_class(instance=BlogPost.objects.get(slug=slug))
            return render(request, self.template_name, {'form': form})
        else:
            context = {
                'error': 'You are not authorised to update this post!'
            }
            return render(request, 'blog/error-page.html', context=context)

    def post(self, request, slug, *args, **kwargs):
        form = self.form_class(request.POST)
        post = self.model.objects.get(slug=slug)
        if form.is_valid():
            print(form.cleaned_data)
            post.title = form.cleaned_data['title']
            post.description = form.cleaned_data['description']
            post.save()
            print('saved')
            return redirect(reverse('home'))

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class DeleteBlog(View):
    model = BlogPost

    def get(self, request, slug, *args, **kwargs):
        post = self.model.objects.get(slug=slug)
        if post.author == request.user:
            post.delete()
            return redirect(reverse('home'))
        else:
            context = {
                'error': 'You are not authorised to delete this post!'
            }
            return render(request, 'blog/error-page.html', context=context)
