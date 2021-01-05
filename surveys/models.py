from datetime import date

from django.db import models

from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel


from .blocks import QuestionTextBlock, QuestionMultipleChoiceBlock, QuestionSingleChoicBlock


@register_snippet
class Survey(models.Model):
    """опрос"""   
      
    name = models.CharField(verbose_name='Название опроса', max_length=255)
    description = models.CharField(verbose_name='Описание опроса', max_length=2055)
   
    date_from = models.DateField(verbose_name='дата начала опроса', default=date.today, editable=False)    
    date_to = models.DateField(verbose_name='дата окончания опроса', default=date.today)

    questions = StreamField([
        ('textquestion', QuestionTextBlock()),
        ('singlechoicequestion', QuestionSingleChoicBlock()),
        ('multiplechoicequestion', QuestionMultipleChoiceBlock()),
    ])

    panels = [FieldPanel('name'),
			  FieldPanel('description'),
			  StreamFieldPanel('questions')
	]

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
       

    def __str__(self):
        return self.name
