from django.db import models


class Words(models.Model):
    en_word = models.CharField(verbose_name='en_word', max_length=100)
    ru_translation = models.CharField(verbose_name='ru_translation', max_length=100)

    def __str__(self):
        return self.en_word + " : " + self.ru_translation
