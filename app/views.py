from datetime import datetime
from django.db.models import Q
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage
from django.views import View
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


from .models import Owner,Post,Comment,Pick,Trade,ThreadModel,MessageModel,Notification
from .forms import PostForm,CommentForm,FranchiseForm,UpdatePickForm,ThreadForm,MessageForm
# Create your views here.

years=['2022','2023']

class Test(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        owners = Owner.objects.all().order_by('teamname')
        context = {
            'owners':owners,
        }
        return render(request,'app/test.html',context)



class Landing(View):
    def dispatch(self, request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'app/landing.html')

class Home(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        owners = Owner.objects.all().order_by('teamname')
        form = PostForm()
        posts = Post.objects.all().order_by('-created_on')
        
        p = Paginator(posts,10)
        page_num = request.GET.get('page',1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        context = {
            'owners' : owners,
            'all' : posts,
            'last_page' : p.num_pages,
            'feed': page,
            'form': form,
        }
        return render(request,'app/home.html', context)


    def post(self, request, *args, **kwargs):
        ## DEFINE ALL CONTEXT
        owners = Owner.objects.all().order_by('teamname')
        form = PostForm(request.POST)
        posts = Post.objects.all().order_by('-created_on')
        p = Paginator(posts,10)
        page_num = request.GET.get('page',1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            form = PostForm()
        ##

        context = {
            'owners' : owners,
            'all' : posts,
            'last_page' : p.num_pages,
            'feed': page,
            'form': form,
        }
        return render(request,'app/home.html', context)

class ProfileView(LoginRequiredMixin,View):
    def get(self,request,pk,*args,**kwargs):
        profile = Owner.objects.get(pk=pk)
        user = request.user
        posts = Post.objects.filter(author=user).order_by('-created_on')
        picks = Pick.objects.all().order_by('year','round','pick')

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'picks': picks,
        }

        return render(request, 'app/profile.html', context)

class ProfileEditView(LoginRequiredMixin,UpdateView):
    model = Owner
    fields = ['user', 'teamname', 'picture']
    template_name = 'app/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

class PostDetailView(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('created_on')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'app/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            form = CommentForm()
        
        comments = Comment.objects.filter(post=post).order_by('created_on')

        if new_comment.author != post.author:
            notification = Notification.objects.create(notification_type=2,from_user=request.user,to_user=post.author,comment=new_comment)

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'app/post_detail.html', context)

class PostEditView(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['body']
    template_name = 'app/post_edit.html'
    
    def get_success_url(self):
        post= self.get_object()
        post.body = post.body + "\n\n(updated: " + str(datetime.now().replace(microsecond=0)) + ")"
        post.save()
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'app/post_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostPinView(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        if request.method == 'POST':
            post = Post.objects.get(pk=pk)
            if post.pinned is False:
                post.pinned = True
            else:
                post.pinned = False
            post.save()
            next = request.POST.get('next')
            return HttpResponseRedirect(next)

class PostCommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Comment
    template_name = 'app/post_comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class PostAddLike(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
            if post.author != request.user:
                notification = Notification.objects.create(notification_type=1,from_user=request.user,to_user=post.author,post=post)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')


        return HttpResponseRedirect(next)

class PostAddDislike(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class PostSearch(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        post_list = Post.objects.filter(
            Q(body__icontains=query) | Q(title__icontains=query)
        ).order_by('-created_on')

        comment_list = Comment.objects.filter(
            Q(comment__icontains=query)
        ).order_by('-created_on')

        context = {
            'post_list': post_list,
            'comment_list': comment_list,
        }

        return render(request, 'app/post_search.html', context)

class TradePartner(LoginRequiredMixin,View):
    def get(self,request, *args,**kwargs):
        if request.method == 'GET':
            users = User.objects.all()
            picks = Pick.objects.all()
            owners = Owner.objects.all()
            trades = Trade.objects.all().order_by('-trade_date')

            context = {
                'trades' : trades,
                'users' : users,
                'picks' : picks,
                'owners' : owners
            }
            return render(request,'app/trade.html',context)

    def post(self,request, *args,**kwargs):
        if request.method == 'POST':
            trader_one = Owner.objects.get(user__username=request.user)
            partner_input = request.POST['partner']
            trader_two = Owner.objects.get(user__username=partner_input)
            new_trade = Trade(
                trader_one = trader_one.user,
                trader_two = trader_two.user,
                trade_status = "In Talks"
            )
            new_trade.save()

            return redirect(f'traderoom/{new_trade.pk}')

class TradeRoom(LoginRequiredMixin,View):
    def get(self, request,pk, *args, **kwargs):
        if request.method == 'GET':
            trade = Trade.objects.all().order_by('-trade_date')
            users = User.objects.all()
            picks = Pick.objects.all().order_by('year','round')
            owners = Owner.objects.all()
            trade = Trade.objects.get(pk=pk)

            context = {
                'trade' : trade,
                'users' : users,
                'picks' : picks,
                'owners' : owners
            }
            return render(request, 'app/trade_rooms.html', context)

    def post(self,request,pk,*args,**kwargs):
        trade = Trade.objects.get(pk=pk)
        if request.method =='POST':
            if 'propose' in request.POST:
                trade.trade_status = "Proposed"
                trade.trader_one_accepted = False
                trade.trader_two_accepted = False
                trade.save()
                if trade.trader_one == request.user:
                    trade.trader_one_accepted = True
                    trade.save()
                    notification = Notification.objects.create(notification_type=4,from_user=request.user,to_user=trade.trader_two,trade=trade)
                else:
                    trade.trader_two_accepted = True
                    trade.save()
                    notification = Notification.objects.create(notification_type=4,from_user=request.user,to_user=trade.trader_one,trade=trade)

            elif 'counter' in request.POST:
                if trade.trader_one == request.user:
                    trade.trader_one_accepted = False
                    trade.trader_two_accepted = False
                    trade.save()
                    notification = Notification.objects.create(notification_type=5,from_user=request.user,to_user=trade.trader_two,trade=trade)
                else:
                    trade.trader_one_accepted = False
                    trade.trader_two_accepted = False
                    trade.save()
                    notification = Notification.objects.create(notification_type=5,from_user=request.user,to_user=trade.trader_one,trade=trade)

            elif 'accept' in request.POST:
                if trade.trader_one == request.user:
                    trade.trader_one_accepted = True
                    trade.trade_status = "Completed"
                    trade.trade_date = datetime.datetime.now()
                    for pick in trade.trader_one_list.all():
                        print('PICK',pick)
                        pick.owner = trade.trader_two
                        pick.save()
                    for pick in trade.trader_two_list.all():
                        print('PICK',pick)
                        
                        pick.owner = trade.trader_one
                        pick.save()
                    trade.save()
                    notification = Notification.objects.create(notification_type=6,from_user=request.user,to_user=trade.trader_two,trade=trade)

                else:
                    trade.trader_two_accepted = True
                    trade.trade_status = "Completed"
                    for pick in trade.trader_one_list.all():
                        print('PICK',pick)

                        pick.owner = trade.trader_two
                        pick.save()
                    for pick in trade.trader_two_list.all():
                        print('PICK',pick)

                        pick.owner = trade.trader_one
                        pick.save()
                    trade.save()
                    notification = Notification.objects.create(notification_type=6,from_user=request.user,to_user=trade.trader_one,trade=trade)
                
                all_trades = Trade.objects.all()
                for other_trade in all_trades:
                    if other_trade.trade_status != "Completed":
                        for pick in other_trade.trader_one_list.all():
                            if (pick in trade.trader_one_list.all()) or (pick in trade.trader_two_list.all()):
                                other_trade.flagged = True
                                other_trade.save()
                        for pick in other_trade.trader_two_list.all():
                            if (pick in trade.trader_one_list.all()) or (pick in trade.trader_two_list.all()):
                                other_trade.flagged = True
                                other_trade.save()



            next = request.POST.get('next',f'/trade/traderoom/{trade.pk}')
            return HttpResponseRedirect(next)

class UpdateList(LoginRequiredMixin,View):
    def post(self,request,pk,pick_pk,*args,**kwargs):
        if request.method == 'POST':
            trade = Trade.objects.get(pk=pk)
            pick = Pick.objects.get(pk=pick_pk)
            if 'addpick' in request.POST:
                if trade.trader_one == pick.owner:
                    trade.trader_one_list.add(pick)
                else:
                    trade.trader_two_list.add(pick)
                trade.save()
            elif 'removepick' in request.POST:
                if trade.trader_one == pick.owner:
                    trade.trader_one_list.remove(pick)
                else:
                    trade.trader_two_list.remove(pick)
                trade.save()

            next = request.POST.get('next',f'/trade/traderoom/{trade.pk}')
            return HttpResponseRedirect(next)

class TradeRoomDeleteView(LoginRequiredMixin,DeleteView):
    model = Trade
    success_url = reverse_lazy('trade')

    def test_func(self):
        room = self.get_object()
        self.request.method == 'GET'
        if room.trade_status != "Accepted":
            if room.trader_one == self.request.user:
                return self.request.user == room.trader_one
            else:
                return self.request.user == room.trader_two

class Draftboard(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        if request.method == 'GET':
            picks = Pick.objects.all().order_by('pick','round')
            owners = Owner.objects.all().order_by('pick_spot')
            context = {
                'picks' : picks,
                'owners' : owners,
            }

            return render(request,'app/draftboard.html',context)

class ListThreads(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        users = User.objects.all()

        context = {
            'users' : users,
            'threads': threads
        }

        return render(request, 'app/inbox.html', context)

class CreateThread(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        username = request.POST.get('username')
        
        context = {
            'users' : users,
            'username' : username,
        }

        return render(request, 'app/inbox_create_thread.html', context)

    def post(Self,request,*args,**kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')
        print('FROM POST',username)

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            return redirect('create-thread')

class ThreadView(LoginRequiredMixin,View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user)).order_by('user')
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        users = User.objects.all()
        context = {
            'users' : users,
            'threads' : threads,
            'thread': thread,
            'form': form,
            'message_list': message_list,
        }

        return render(request, 'app/inbox_thread.html', context)

class CreateMessage(LoginRequiredMixin,View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )

        message.save()

        # if message.sender_user != request.user:
        notification = Notification.objects.create(notification_type=3,from_user=request.user,to_user=message.receiver_user,thread=thread)

        return redirect('thread', pk=pk)

class PostNotification(LoginRequiredMixin,View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post-detail', pk=post_pk)

class MessageNotification(LoginRequiredMixin,View):
    def get(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        
        notification.user_has_seen = True
        notification.save()

        return redirect('inbox')

class TradeNotification(LoginRequiredMixin,View):
    def get(self, request, notification_pk, trade_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        trade = Trade.objects.get(pk=trade_pk)
        
        notification.user_has_seen = True
        notification.save()

        return redirect('trade-room', pk=trade_pk)

class RemoveNotification(LoginRequiredMixin,View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')

class ClearNotifications(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        notifications = Notification.objects.filter(to_user=request.user).exclude(user_has_seen=True).order_by('-date')
        for notification in notifications:
            notification.user_has_seen = True
            notification.save()
        return redirect('home')

class CommToolsView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        franchise_form = FranchiseForm()
        pick_form = UpdatePickForm()

        context = {
            'franchise_form': franchise_form,
            'pick_form': pick_form,
        }        
        return render(request,'app/comm_tools.html', context)

    def post(self, request, *args, **kwargs):
        if 'franchise_next' in request.POST:
            form = FranchiseForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                if form.instance.manager is None:
                    form.instance.manager = self.request.user
                    form.instance.name = 'Unclaimed'
                else:
                    form.instance.name = Owner.objects.filter(user=form.instance.manager).values('teamname')

                for y in years:
                    for i in range(1,16):
                        new_pick = Pick(
                            original_owner = form.instance.manager,
                            owner = form.instance.manager,
                            year = y,
                            round = i,
                            pick = None
                        )
                        new_pick.save()
                form.save()
                
                franchise_form = FranchiseForm()
                pick_form = UpdatePickForm()

                context = {
                    'franchise_form': franchise_form,
                    'pick_form': pick_form,
                } 

            return render(request,'app/comm_tools.html',context)

        elif 'pick_next' in request.POST:
            form = UpdatePickForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                owner_user = form.instance.owner_user
                owner = Owner.objects.get(user=owner_user)
                updated_pick = int(form.instance.updated_pick_spot)
                owner.pick_spot = updated_pick
                owner.save()

                user_picks = Pick.objects.filter(owner=owner.user)
                for pick in user_picks:
                    pick.pick = updated_pick
                    pick.save()

                franchise_form = FranchiseForm()
                pick_form = UpdatePickForm()
        
                context = {
                    'franchise_form': franchise_form,
                    'pick_form': pick_form,
                } 

            return render(request,'app/comm_tools.html',context)