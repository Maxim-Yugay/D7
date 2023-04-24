from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django_filters import FilterSet, DateFilter
from django.forms import DateTimeInput
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .models import *
from .filters import PostFilter
from .forms import PostForm



class AuthorList(ListView):
    model = Author
    context_object_name = 'Author'

class PostList(ListView):
    model = Post
    context_object_name = 'post'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_paper.add_post')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_paper/post_edit.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_paper.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_paper/post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_paper.delete_post')
    model = Post
    template_name = 'news_paper/post_delete.html'
    success_url = reverse_lazy('news')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()
    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'news_paper/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

