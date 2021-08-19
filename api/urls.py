
from django.urls import path

from . import views

urlpatterns = [
  path('api-token-auth/', views.CustomAuthToken.as_view()),

  path('init/', views.init),
  path('verify/email/', views.verify_email),

  path('check/sent/invite/', views.check_sent_invite),
  path('send/invite/', views.send_invite),
  path('delete/invite/', views.DeleteInvite.as_view()),
  path('received/invites/', views.ReceivedInvites.as_view()),
  path('accept/invite/', views.accept_invite),
  path('reject/invite/', views.RejectInvite.as_view()),

  path('list/items/', views.ListItemView.as_view()),
  path('add/item/', views.ListAddItemView.as_view()),
  path('delete/listitem/<int:pk>/', views.ListItemDeleteView.as_view()),
]