import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Blog, Post
from bot.models import TelegramChatInfo
from .scripts.chat_info import get_chat_photo, get_chat_info
from .forms import BlogRegistrationForm

from bot.views import send_message

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

def main(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'user_verse/main_page.html', context)

def dashboard(request):
    return render(request, 'dashboard_base.html')

@csrf_exempt
@login_required
def get_user_info(request):
    if request.method == 'POST':
        user = request.user
        received_user_id = json.loads(request.body)['receivedUserID']
        if user.id == received_user_id:
            return JsonResponse({"status": "ok"}, status=200)
        else:
            return JsonResponse({
                "status": "error",
                "username": user.username,
                "telegram_user": user.telegram_user,
            }, status=404)


class ChannelListView(LoginRequiredMixin, ListView):
    model = TelegramChatInfo
    template_name = 'user_verse/channel_list.html'
    context_object_name = 'channels'

    def get(self, request, *args, **kwargs):
        telegram_user = request.user.telegram_user
        user_channels = TelegramChatInfo.objects.filter(user=telegram_user)
        return render(request, 'user_verse/channel_list.html', 
                    {'user_channels': user_channels})


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    blog_form = BlogRegistrationForm
    template_name = 'user_verse/blog_list.html'

    def post(self, request, *args, **kwargs):
        blog_form = BlogRegistrationForm(request.POST)
        print(blog_form.errors)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.creator = request.user
            blog_form.save()
            return redirect('blog-post-list', blog.id)
    
    
    def get(self, request, *args, **kwargs):
        django_user = request.user
        user_blogs = Blog.objects.filter(creator=django_user)

        context = locals()
        context['form'] = self.blog_form
        context['user_blogs'] = user_blogs
        
        return render(request, self.template_name, context)




@method_decorator(csrf_exempt, name='dispatch')
class PostCreateView(LoginRequiredMixin, CreateView):

    def post(self, request, *args, **kwargs):    
        post_title = json.loads(request.body)['title']
        post_content = json.loads(request.body)['body']
        try:
            channel_id = json.loads(request.body)['channel_id']
            if channel_id:
                try:
                    selected_channel = TelegramChatInfo.objects.get(id=channel_id)

                    Post.objects.create(
                        author=request.user,
                        title=post_title,
                        content=post_content,
                        chat=selected_channel,
                        blog=None,
                    )
                
                    return JsonResponse({"status": "ok"}, status=200)
                except Exception as e:
                    # Log and handle exceptions
                    print(f"Error triggering Celery task: {e}")
                            # Call the Celery task
        except KeyError:
            blog_id = json.loads(request.body)['blog_id']
            if blog_id:
                selected_blog = Blog.objects.get(id=blog_id)
                
                Post.objects.create(
                    author=request.user,
                    title=post_title,
                    content=post_content,
                    chat=None,
                    blog=selected_blog,
                )
        
        return JsonResponse({"status": "ok"}, status=200)
    
    def get(self, request, *args, **kwargs):
        channel_id = kwargs.get('channel_id')
        blog_id = kwargs.get('blog_id')
        if channel_id:
            selected_channel = TelegramChatInfo.objects.get(id=channel_id)
        
            context = {
                "channel_id": channel_id,
                "channel_name": selected_channel.chat_title,
            }
            return render(request, 'user_verse/text_area.html', context=context)
        
        elif blog_id:
            selected_blog = Blog.objects.get(id=blog_id)

            context = {
                "verse_id": blog_id,
                "verse_name": selected_blog.blog_title,
            }
            return render(request, 'user_verse/blog_text_editor.html', context=context)
        
        


@method_decorator(csrf_exempt, name='dispatch')
class PostListView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        channel_id = kwargs.get('channel_id')
        print(channel_id)
        blog_id = kwargs.get('blog_id')
        if channel_id:
            channel = TelegramChatInfo.objects.get(id=channel_id)
            channel_posts = Post.objects.filter(chat=channel_id)
            print(channel_posts)

            context = {
                "channel": channel,
                "posts": channel_posts,
            }

            return render(request, 'user_verse/channel_post_list.html', context=context)
        elif blog_id:
            blog = Blog.objects.get(id=blog_id)
            blog_posts = Post.objects.filter(blog=blog_id)
            print(blog_posts)

            context = {
                "blog": blog,
                "posts": blog_posts,
            }
            
            return render(request, 'user_verse/blog_post_list.html', context=context)

        
        

class PostUpdateView(LoginRequiredMixin, UpdateView):
    
    def get(self, request, *args, **kwargs):
        channel_id = kwargs.get('channel_id')
        channel = TelegramChatInfo.objects.get(id=channel_id)

        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        context = {
            'channel_id': channel.id,
            'channel_name': channel.chat_title,
            'post': post,
        }
        return render(request, 'user_verse/text_area.html', context=context)

    def post(self, request, *args, **kwargs):
        post_title = json.loads(request.body)['title']
        post_content = json.loads(request.body)['body']
        post_id = json.loads(request.body)['post_id']
        channel_id = json.loads(request.body)['channel_id']
        channel = TelegramChatInfo.objects.get(id=channel_id)


        post = get_object_or_404(Post, id=post_id)
        post.title = post_title
        post.content = post_content

        post.save()

        send_message(chat_id=channel.chat_id, title=post_title, content=post_content)
        
        return JsonResponse({"status": "ok"}, status=200)




# @csrf_exempt
# def add_chat_info(request):
#     if request.method == "POST":
#         update = request.body.decode('utf-8')
#         try:
#             print(json.loads(update))
#             bot_status = json.loads(update)['my_chat_member']['new_chat_member']['status']
#             print(f'\nHello bot status: {bot_status}\n')
#             if bot_status == 'kicked':
#                 print('\nkicked\n')
#                 return HttpResponse("Just passing")
#             elif bot_status == 'administrator':
#                 print('\nadministrator\n')
#                 chat_info = get_chat_info(update)
#                 get_chat_photo(chat_info['chat_id'], chat_info['chat_name'])
#                 print(chat_info)
#                 print(type(request.user))
#                 # context = {
#                 #     'data': chat_info
#                 # }

#                 return render(request, 'user_verse/main_page.html', context=chat_info)

#             return HttpResponse(status=204)
#         except TypeError and KeyError:
#             return HttpResponse("Just passing")
#     elif request.method == "GET":
#         # print('success_1')
#         subprocess.run(["python", "user_verse/scripts/testing_with_webhook.py"])
        # result = subprocess.run(["python", "user_verse/utils/timer_with_signal.py"])
        # print(result.stdout)
        # is_stop = result.stdout
        # print(is_stop)
        # if is_stop:
        #     is_deleted = subprocess.run(["python", "user_verse/scripts/delete_webhook.py"])
        #     is_deleted = is_deleted.stdout.strip()
        #     if is_deleted:
        #         print("Webhook deleted successfully.")
        #     else:
        #         print(f"Failed to delete webhook")
        # print('success_2')
        # return HttpResponse(status=204)


# def delete_webhook(request):
#     if request.method == 'GET':
#         is_deleted = subprocess.run(["python", "user_verse/scripts/delete_webhook.py"], capture_output=True)
#         is_deleted = is_deleted.stderr.decode('utf-8').strip()
#         if is_deleted:
#             print("Webhook deleted successfully.")
#         else:
#             print(f"Failed to delete webhook")
#         return HttpResponse(status=204)
