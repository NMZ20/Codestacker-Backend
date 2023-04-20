from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.UploadFile.as_view()),
    path("list/", views.ListFiles.as_view()),
    path("search/<str:keyword>/", views.Search.as_view()),
    path("get-pdf/<str:id>/", views.FileRetrieve.as_view()),
    path("get-sentences/<str:id>/", views.RetrieveSentences.as_view()),
    path("occurences/<str:id>/<str:word>/", views.CheckOccurence.as_view()),
    path("delete/<str:id>/", views.DeleteFile.as_view()),
    path("top-words/<str:id>/", views.TopWords.as_view()),
    path("get-page/<str:id>/<int:page_number>/", views.GetPage.as_view()),
]
