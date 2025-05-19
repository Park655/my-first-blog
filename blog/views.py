from django.shortcuts import render
from django.utils import timezone
from .models import Post, Supplement
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login

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
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            return redirect('post_list')  # 원하는 페이지로 이동
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})