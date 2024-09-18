from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, Comment
from .forms import CommentForm

def home(request):
    search_query = request.GET.get('q', '')
    videos = Video.objects.filter(title__icontains=search_query)
    return render(request, 'videos/home.html', {'videos': videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comments = video.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.save()
            return redirect('video_detail', video_id=video.id)
    else:
        form = CommentForm()
    return render(request, 'videos/video_detail.html', {
        'video': video,
        'comments': comments,
        'form': form
    })
