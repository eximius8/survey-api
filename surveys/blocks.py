from wagtail.core import blocks



class QuestionTextBlock(blocks.StructBlock):
    """block for question with text answer"""

    question = blocks.CharBlock(required=True,  label="Текст вопроса")
    caption = blocks.CharBlock(required=False, help_text = "Подпись к картинке", label="Подпись")

    class Meta:  # noqa
        template = "streams/image_with_caption_block.html"
        icon = "image"
        label = "Картинка с подписью"



class QuestionMultipleChoiceBlock(blocks.StructBlock):
    """block for question with multiple answer"""

    question = blocks.CharBlock(required=True,  label="Текст вопроса")
    answers = blocks.StreamBlock(
        [
            ('Answer', blocks.CharBlock(required=True,  label="Ответ")), 
        ], 
        min_num=1,         
        label = 'Ответы (минимум 1)') 

    class Meta:  # noqa        
        icon = "image"
        label = "Картинка с подписью"


class QuestionSingleChoicBlock(blocks.StructBlock):
    """block for question with single answer"""

    question = blocks.CharBlock(required=True,  label="Текст вопроса")
    answers = blocks.StreamBlock(
        [
            ('Answer', blocks.CharBlock(required=True,  label="Ответ")), 
        ], 
        min_num=1,
        label = 'Ответы (минимум 1)') 

    class Meta:  # noqa       
        icon = "image"
        label = "Вопрос с одним вариантом ответа"