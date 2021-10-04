from django.urls import path
from main import views

urlpatterns = [
    # path('', views.index, name='index')
    path("list/", views.ListPublicationAPIView.as_view(), name="publication_list"),
    path("filter/", views.FilterPublicationAPIView.as_view(), name="publication_filter"),
    path("details/<int:pk>", views.DetailPublicationAPIView.as_view(), name="publication_list"),
    path("create/", views.CreatePublicationAPIView.as_view(), name="publication_create"),
    path("update/<int:pk>/", views.UpdatePublicationAPIView.as_view(), name="update_publication"),
    path("delete/<int:pk>/", views.DeletePublicationAPIView.as_view(), name="delete_publication"),

    path("comment/list/", views.ListCommentAPIView.as_view(), name="response_list"),
    path("comment/create/", views.CreateCommentAPIView.as_view(), name="response_create"),
    path("comment/update/<int:pk>/", views.UpdateAPIView.as_view(), name="update_response"),
    path("comment/delete/<int:pk>/", views.DeleteCommentAPIView.as_view(), name="delete_response"),

    path('api/messages/<str:sender>/<str:receiver>', views.message_list, name='message_detail'),
    path('api/messages/', views.message_list, name='message_list'),
]
