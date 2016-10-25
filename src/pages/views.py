from django.contrib.auth.views import login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', *args, **kwargs)
    else:
        return login(request, *args, **kwargs)


class IndexView(TemplateView):

    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        #context['last_questions'] = Question.objects.filter(is_published=True)[:5]
        #context['last_answers'] = Answer.objects.filter(question__is_published=True)[:5]
        #context['categories'] = Category.objects.all()
        return context