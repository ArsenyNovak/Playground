from django import forms

from django.forms import ModelChoiceField

from SportsGrounds.models import Playground, Category, Comment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class CatModelChoiceField(ModelChoiceField):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        self.validate_no_null_characters(value)
        # try:
        #     key = self.to_field_name or "pk"
        #     if isinstance(value, self.queryset.model):
        #         value = getattr(value, key)
        #     value = self.queryset.get(**{key: value})
        # except (ValueError, TypeError, self.queryset.model.DoesNotExist):
        #     raise ValidationError(
        #         self.error_messages["invalid_choice"],
        #         code="invalid_choice",
        #         params={"value": value},
        #     )
        return value

class AddPlayGroundForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-input'}), label='Название')
    description = forms.CharField(widget=forms.Textarea(attrs={'cols':80, 'rows': 10}), label='Описание')
    cat = CatModelChoiceField(queryset=Category.objects.all(),
                           widget=forms.CheckboxSelectMultiple(),label='Наличие площадок:')
    photo_all = MultipleFileField(label='Добавить фотографии:')



class AddCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows': 3}))


