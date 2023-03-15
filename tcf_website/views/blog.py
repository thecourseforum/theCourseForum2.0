"""Views for blog pages."""
from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404

from ..models import BlogPost


class BlogView(TemplateView):
    """Blog view."""
    template_name = 'blog/blog.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = BlogPost.objects.all().order_by('-created_at')
        context['featured_posts'] = posts[:3]
        context['all_posts'] = posts
        return context


def post(request, slug):
    """Display specific blog posts"""
    # Note: can replace with DetailView

    post_detail = get_object_or_404(BlogPost, slug=slug)

    return render(request, 'blog/post.html', {'post_detail': post_detail})
