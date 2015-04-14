from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div


class SearchForm(forms.Form):
    beer_name = forms.CharField(label="Nafn bjórs", required=False)

    helper = FormHelper()
    helper.form_id = "main-form"
    helper.layout = Layout(
        Div(
            Field("beer_name", placeholder="Hluti af nafni bjórs"),
        )
    )
    helper.form_action = "/search/"