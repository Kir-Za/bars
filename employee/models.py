from django.db import models
from django.core.urlresolvers import reverse_lazy



class Candidate(models.Model):
    """
    Кандидат в падаваны
    """
    name = models.CharField(max_length=255, verbose_name="имя кандидата")
    age = models.PositiveSmallIntegerField(verbose_name="возраст кандидата")
    email = models.EmailField(verbose_name="email кандидата")
    planet = models.ForeignKey('employee.Planet', related_name="home", verbose_name="планета проживания")
    exame = models.ForeignKey(
        'employee.Quest',
        blank=True,
        null=True,
        related_name="quest_for_cand",
        verbose_name="испытание"
    )
    answers = models.TextField()
    sensei = models.ForeignKey('employee.Djedai', related_name="teacher", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'


class Djedai(models.Model):
    """
    Мастер джедай
    """
    name = models.CharField(max_length=255, verbose_name="Имя джедая")
    planet = models.ForeignKey('employee.Planet', related_name="registration", verbose_name="планета обучения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Джедай'
        verbose_name_plural = 'Джедаи'


class Planet(models.Model):
    """
    Планета приписки
    """
    name = models.CharField(max_length=255, verbose_name="название планеты")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Планета'
        verbose_name_plural = 'Планеты'


class Quest(models.Model):
    """
    Испытание ордена джедаев
    """
    code = models.PositiveSmallIntegerField(verbose_name="Номер ордена", unique=True)
    questions = models.ManyToManyField('employee.Question', related_name="test_list", verbose_name="список вопросов")

    def __str__(self):
        return "Орден № " + str(self.code)

    class Meta:
        verbose_name = 'Испытание'
        verbose_name_plural = 'Испытания'


class Question(models.Model):
    """
    Возможные вопросы для составления испытания
    """
    be_asked = models.TextField(verbose_name="вопрос экзаменатора")

    def __str__(self):
        return self.be_asked

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
