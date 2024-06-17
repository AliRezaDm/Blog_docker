from django.urls import path

from . import views

app_name = "comment"

urlpatterns = [
    path("detail/<int:product_id>/comment/", views.create_comment_view, name="create_comment"),
    path("detail/<int:product_id>/comment/<int:comment_id>/", views.reply_comment_view, name="reply_comment"),
]
