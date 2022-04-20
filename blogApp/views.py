from django.shortcuts import render,redirect,reverse
from django.http.response import HttpResponse
from django.views.generic import ListView,DetailView,DeleteView,CreateView,View,UpdateView
from .models import PostComment,Post,Categories
from users.models import Author
from .forms import PostForm,CommentForm
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
# Create your views here.

class Indexview(View):
    def get(self,request,*args,**kwargs):
        featured_posts = Post.objects.filter(featured = True)[0:3]
        latest_posts = Post.objects.order_by("-post_date")[0:3]
        print(featured_posts)
        context = {"featured_posts":featured_posts,"latest_posts":latest_posts}
        return render(request,"blogApp/index.html",context= context)

    def post(self,request,*args,**kwargs):
        email = request.POST.get("email")
        newletter = Newsletter()
        newletter.email= email
        newletter.save()
        messages.info(request,"succesfully suscribed")
        return redirect("index")


class PostDetailView(DetailView):
    model = Post
    template_name = "blogApp/post_detail.html"
    comment_from = CommentForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_post"] = Post.objects.all().order_by("-post_date")[0:3]
        context["categories"] = Categories.objects.all()
        context["comment_form"] = self.comment_from
        return context

    def post(self,request,*args,**kwargs):
        _post = self.get_object()
        _comment_form = CommentForm(request.POST)
        if _comment_form.is_valid():
            _comment_form.instance.sender = request.user
            _comment_form.instance.post = _post
            _comment_form.save()
            return redirect(_post)


class PostListView(ListView):
    model = Post
    template_name = "blogApp/post_list.html"
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_post"] = Post.objects.all().order_by("post_date")[0:3]
        context["categories"] = Categories.objects.all()
        return context


class SearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "")
        search_result = Post.objects.filter(
            Q(title__icontains=q) | Q(body__icontains=q)
        ).all()
        context = {"search_result": search_result}
        return render(request, "blogApp/search.html", context=context)


class PostCreateView(CreateView):
    model = Post
    template_name = "blogApp/post_create.html"
    form_class = PostForm

    def form_valid(self,form):
        form.instance.author = Author.objects.filter(user = self.request.user).first()
        form.save()
        return redirect(reverse("post_detail",kwargs= {"slug": form.instance.slug}))


class PostUpdateView(UpdateView):
    model = Post
    template_name = "blogApp/post_update.html"
    form_class = PostForm

    def form_valid(self, form):
        if form.instance.author == self.request.user.author:
            form.save()
            return redirect(reverse("post_detail",kwargs={"slug":form.instance.slug}))


class PostDeleteView(DeleteView):
    model = Post
    template_name = "blogApp/post_delete.html"
    success_url = reverse_lazy("index")