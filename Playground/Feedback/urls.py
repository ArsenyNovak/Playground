from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('contact/', views.FeedbackMessage.as_view(), name='contact'),
    path('contact/done', TemplateView.as_view(template_name='Feedback/send_message_done.html'), name='contact_done'),
    ]


