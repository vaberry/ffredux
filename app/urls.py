from django.urls import path
from .views import (
    Landing,
    Home,
    ProfileView,
    ProfileEditView,
    
    PostDetailView,
    PostEditView,
    PostDeleteView,
    PostPinView,
    PostCommentDeleteView,
    PostAddLike,
    PostAddDislike,
    PostSearch,

    TradePartner,
    TradeRoom,
    UpdateList,
    TradeRoomDeleteView,

    Draftboard,

    ListThreads,
    CreateThread,
    ThreadView,
    CreateMessage,

    PostNotification,
    MessageNotification,
    TradeNotification,
    RemoveNotification,
    ClearNotifications,

    CommToolsView,
    )

urlpatterns = [
    path('',Landing.as_view(),name='landing'),


    path('home/',Home.as_view(),name='home'),
    path('profile/<int:pk>',ProfileView.as_view(),name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),

    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/update-pin/<int:pk>',PostPinView.as_view(),name='post-pin'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', PostCommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/like', PostAddLike.as_view(), name='like'),
    path('post/<int:pk>/dislike', PostAddDislike.as_view(), name='dislike'),
    path('post/search/', PostSearch.as_view(), name='post-search'),

    path('trade/',TradePartner.as_view(),name='trade'),
    path('trade/traderoom/<int:pk>/',TradeRoom.as_view(),name='trade-room'),
    path('trade/traderoom/<int:pk>/update-list/<int:pick_pk>',UpdateList.as_view(),name='update-list'),
    path('trade/delete/<int:pk>',TradeRoomDeleteView.as_view(),name='trade-room-delete'),

    path('draftboard/',Draftboard.as_view(),name='draftboard'),

    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),


    path('notification/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name='post-notification'),
    path('notification/<int:notification_pk>/inbox/', MessageNotification.as_view(), name='message-notification'),
    path('notification/<int:notification_pk>/trade/traderoom/<int:trade_pk>', TradeNotification.as_view(), name='trade-notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),
    path('notification/clear/', ClearNotifications.as_view(), name='clear-notifications'),

    path('commtools/',CommToolsView.as_view(), name='comm-tools'),

    
]