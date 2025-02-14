# blog/views.py
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from .models import BlogPost

class Index(ListView):
   model = BlogPost
   queryset = BlogPost.objects.all().order_by('-date')
   template_name = 'blog/index.html'
   paginate_by = 2

   def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_range = paginator.page_range
        total_pages = paginator.num_pages
        current_page = page_obj.number

        # Compute which page numbers to display
        display_pages = [
            total_pages <= 5 or 
            num == 1 or 
            num == total_pages or 
            (num >= current_page - 1 and num <= current_page + 1)
            for num in page_range
        ]

        # Add to context
        context['page_range'] = page_range
        context['display_pages'] = display_pages
        return context

class Featured(ListView):
   model = BlogPost
   queryset = BlogPost.objects.filter(featured=True).order_by('-date')
   template_name = 'blog/featured.html'
   paginate_by = 1


class BlogDetailsView(DetailView):
   model = BlogPost
   template_name = 'blog/blog_post.html'

   def get_context_data(self, **kwargs):
      context = super(BlogDetailsView, self).get_context_data(**kwargs)
      context['liked_by_user'] = False
      blog_post = BlogPost.objects.get(id=self.kwargs.get('pk'))
      if blog_post.likes.filter(pk=self.request.user.id).exists():
         context['liked_by_user'] = True
      return context


class LikeBlogPost(View):
   def post(self, request, pk):
      blog_post = BlogPost.objects.get(id=pk)
      if blog_post.likes.filter(pk=self.request.user.id).exists():
         blog_post.likes.remove(request.user.id)
      else:
         blog_post.likes.add(request.user.id)
      blog_post.save()
      return redirect('blog_details', pk)


class DeletePostView(DeleteView):
   model = BlogPost
   template_name = 'blog/delete_post.html'
   success_url = reverse_lazy('index')

   def get(self, request, *args, **kwargs):
      return self.post(request, *args, **kwargs)