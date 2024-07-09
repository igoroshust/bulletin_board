from django import forms
from django.core.exceptions import ValidationError
from .models import *

class PubForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = [
            'name',
            'text',
            'category',
        ]

        # def clean(self):
        #     cleaned_data = super().clean()
        #     name = cleaned_data.get("name")
        #     category = cleaned_data.get("category")
        #     date = cleaned_data.get("date")
        #
        #     if name == category:
        #         raise ValidationError(
        #             "Описание не должно совпадать и именем категории"
        #         )
        #
        #     return cleaned_data