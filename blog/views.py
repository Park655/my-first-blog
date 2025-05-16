from django.shortcuts import render
from django.utils import timezone
from .models import Post, Supplement
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.title == '마이페이지':
        return render(request, 'blog/mypage.html', {'post': post})
    elif post.title == '설문조사':
        return render(request, 'blog/survey.html', {'post': post})
    elif post.title == '캘린더':
        return render(request, 'blog/calendar.html', {'post': post})
    elif post.title == '영양제 정보':
        return HttpResponseRedirect(reverse('supplement_list'))
    else:
        return render(request, 'blog/post_detail.html', {'post': post})
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'Blog/post_draft_list.html', {'posts': posts})
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST':
        post.publish()
    return redirect('post_detail', pk=pk)
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
def supplement_list(request):
    query = request.GET.get('q')  # <- 기본값 생략
    if query:
        supplements = Supplement.objects.filter(name__icontains=query)
    else:
        supplements = Supplement.objects.all()  # 전체 출력
    return render(request, 'blog/supplement_list.html', {
        'supplements': supplements,
        'query': query,
    })
