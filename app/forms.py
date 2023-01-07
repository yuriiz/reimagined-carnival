from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit
from django import forms


class InputForm(forms.Form):
    image = forms.ImageField()
    type = forms.ChoiceField(choices=(
        ("cyto", "Cytoplasm"),
        ("nuclei", "Nucleus"),
    ))
    diameter = forms.IntegerField(initial=30)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(
            Submit("submit", "Submit", css_class="btn btn-primary"), )
