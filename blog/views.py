from django.shortcuts import render
from django.utils import timezone
from .models import Post, Supplement, EffectCategory
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from datetime import date
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    # 마이페이지용 profile, age
    profile = None
    age = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.birthdate:
                age = calculate_age(profile.birthdate)
        except ObjectDoesNotExist:
            pass

    # 영양제 정보용
    query = request.GET.get('q')
    category_ids = request.GET.getlist('categories')

    supplements = Supplement.objects.all()
    if query:
        supplements = supplements.filter(name__icontains=query)
    if category_ids:
        for cid in category_ids:
            supplements = supplements.filter(categories__id=cid)
    categories = EffectCategory.objects.all()

    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'profile': profile,
        'age': age,
        'supplements': supplements,
        'query': query,
        'categories': categories,
        'selected_categories': list(map(int, category_ids)),
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.title == '마이페이지':
        return HttpResponseRedirect(reverse('mypage'))
    elif post.title == '설문조사':
        return render(request, 'blog/survey.html', {'post': post})
    elif post.title == '캘린더':
        return render(request, 'blog/calendar.html', {'post': post})
    elif post.title == '영양제 정보':
        return HttpResponseRedirect(reverse('supplement_list'))
    else:
        return render(request, 'blog/post_detail.html', {'post': post})

def supplement_list(request):
    query = request.GET.get('q')
    category_ids = request.GET.getlist('categories')

    supplements = Supplement.objects.all()

    if query:
        supplements = supplements.filter(name__icontains=query)

    if category_ids:
        for cid in category_ids:
            supplements = supplements.filter(categories__id=cid)

    categories = EffectCategory.objects.all()

    return render(request, 'blog/supplement_list.html', {
        'supplements': supplements,
        'query': query,
        'categories': categories,
        'selected_categories': list(map(int, category_ids)),
    })

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('post_list')
            except IntegrityError:
                form.add_error('username', '이미 사용 중인 아이디입니다.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
def calculate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age

@login_required
def mypage_view(request):
    profile = getattr(request.user, 'profile', None)
    age = calculate_age(profile.birthdate) if profile and profile.birthdate else None

    return render(request, 'blog/mypage.html', {
        'profile': profile,
        'age': age,
    })
def survey_view(request):
    return render(request, 'blog/survey.html')
def calendar_view(request):
    return render(request, 'blog/calendar.html')