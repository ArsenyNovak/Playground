from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from Feedback.forms import FeedbackMessageForm
from Playground.settings import DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL


# Create your views here.
class FeedbackMessage(LoginRequiredMixin, FormView):
    template_name = 'Feedback/send_message.html'
    form_class = FeedbackMessageForm
    success_url = reverse_lazy('contact_done')
    extra_context = {'title': 'Обратная связь'}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            message = form.cleaned_data['message'] + f'\nписьмо отправил пользователь {request.user}'
            try:
                send_mail('Предложение по сайту спортивных площадок', message,
                          DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

