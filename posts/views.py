from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from .models import Post
from .forms import PostFrom
from urllib.parse import quote_plus
from django.utils import timezone
from django.db.models import Q
# Create your views here.

def post_home(request):
    return render(request,'home.html')



    # contact_list = Contacts.objects.all()
    # paginator = Paginator(contact_list, 25) # Show 25 contacts per page

    # page = request.GET.get('page')
    # contacts = paginator.get_page(page)
    # return render(request, 'list.html', {'contacts': contacts})

def post_list(request):
    queryset_list = Post.objects.active()
    if request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get('q')
    if query:
        queryset_list = queryset_list.filter(Q(title__icontains=query) | Q(content__icontains=query) ).distinct()
    paginator = Paginator(queryset_list,3)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    

    context = {
        'object_list': queryset,
    }
    return render(request,'posts/post-list.html',context)

def post_detail(request,slug=None):
    instance = get_object_or_404(Post,slug=slug)
    if instance.publish.date() > timezone.now().date() or instance.draft:
        if not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.title)
    context = {
        'object':instance,
        'share_string':share_string,
    }
    return render(request,'posts/post-detail.html',context)

def post_create(request):
    if not request.user.is_superuser:
        raise Http404
    # if not request.user.is_authenticated:
    #     raise Http404
    form = PostFrom(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,'SuccessFully Created')
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request,'Sorry couldnt create')
    # if request.method == 'POST':

    context = {
        'form':form,
    }
    
    return render(request,'posts/post-create.html',context)

    
def post_update(request,slug=None):
    if not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,slug=slug)

    form = PostFrom(request.POST or None,request.FILES or None, instance=instance, )
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,'Post Updated')
        return HttpResponseRedirect(instance.get_absolute_url())
        
    context = {
        'title': instance.title,
        'instance':instance,
        'form':form,
    }
    return render(request,'posts/post-create.html',context)

def post_delete(request,slug=None):
    if  not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post,slug=slug)
    instance.delete()

    messages.success(request,'Post Deleted')
    return redirect('posts:list')