from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form fue enviado
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Campos del formulario que pasan por la validacion
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject,message,'arizamoises@gmail.com',[cd['to']])
            sent = True
            #Enviar email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,'form': form, 'sent': sent})

class PostListView(ListView):
    """
        Vista alternativa a la vista de post
    """

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request):
    post_list = Post.published.all()

    #Paginación con 3 post por paginas
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)

    except PageNotAnInteger:
        #Si page-number no es un integer
        posts = paginator.page(1)    

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})

def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
