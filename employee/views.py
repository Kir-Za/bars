from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail
from django.views.generic import FormView, DetailView, ListView, View
from django.conf import settings
from .models import Candidate, Djedai
from .forms import AnswerForm, CreateCandForm


def index(request):
    return render(request, 'index.html')


class CreateCandidateView(FormView):
    """
    Добавление пользователем нового канидата
    """
    template_name = "cnd_create.html"
    form_class = CreateCandForm
    cand_id = None

    def form_valid(self, form):
        new_candidate = Candidate.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            planet=form.cleaned_data['planet'],
            email=form.cleaned_data['email'],
            exame=form.cleaned_data['exame'],
        )
        self.success_url = reverse_lazy('ask_candidate', kwargs={'pk': str(new_candidate.pk)})
        return super().form_valid(form)


class CandidateQuestionView(FormView, DetailView):
    """
    Опрос кандидата по пунктам испытания
    """
    template_name = "cnd_question.html"
    model = Candidate
    form_class = AnswerForm
    success_url = reverse_lazy('base_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_list = Candidate.objects.get(id=self.kwargs['pk']).exame.questions.all()
        context['questions'] = list([i.__str__() for i in question_list])
        return context

    def form_valid(self, form):
        cand = Candidate.objects.get(id=self.kwargs['pk'])
        cand.answers = "Ответы на вопросы ордена: \n" + form.cleaned_data['answers']
        cand.save()
        return super().form_valid(form)


class DjejSelectView(ListView):
    """
    Список джедаЁв
    """
    template_name = "djed.html"
    model = Djedai


class DjedCandView(ListView):
    """
    Доступные кандидаты в падаваны
    """
    template_name = "cnd_list.html"
    model = Candidate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        djedai = Djedai.objects.get(pk = self.request.GET['pk'])
        planet_dj = djedai.planet
        context['object_list'] = Candidate.objects.filter(planet=planet_dj).filter(sensei=None)
        context['djedai'] = djedai.id
        return context


class AddPadavanView(View):
    """
    Перевести из кандидатов в падаваны
    """

    def post(self, request):
        djedai = Djedai.objects.get(pk = request.POST['djed_id'])
        if len(djedai.teacher.all()) < 3:
            candidate = Candidate.objects.get(pk=int(request.POST['candidate_id']))
            candidate.sensei = djedai
            candidate.save()
            # Перенаправил в файл, а не через smtp.yandex.ru
            send_mail(subject="Инфо",
                      message="Вы приняты в орден",
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[candidate.email],
                      fail_silently=False)
            return redirect(reverse_lazy('base_page'))
        else:
            return render(request, template_name="overpadavan.html")


class CommonDjedView(ListView):
    """
    Полный список джедаев с указанием количества падаванов
    """
    model = Djedai
    template_name = "common.html"


class OnePadavanView(ListView):
    """
    Джедаи у которых более 1-го падавана
    """
    model = Djedai
    template_name = "common.html"

    def get_context_data(self, **kwargs):
        self.object_list = Djedai.objects.filter(teacher__gt=1)
        return super().get_context_data(**kwargs)