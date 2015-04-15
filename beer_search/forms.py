from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django.db.models import Min, Max
from django.forms import NumberInput
from beer_search.models import Beer, Style


def generate_style_choices():
    all_styles = Style.objects.all()
    return tuple([(style.id, style.name) for style in all_styles])


class SearchForm(forms.Form):
    beer_name = forms.CharField(
        label="Nafn bjórs",
        required=False
    )

    min_volume = forms.IntegerField(
        label="Lágmarks rúmmál",
        required=False,
        widget=NumberInput(attrs={
            # "type": "range",  # TODO: Add slider in place of number input
            # "step": "10",
            "type": "number",
            "min": Beer.objects.aggregate(Min("volume"))["volume__min"],
            "max": Beer.objects.aggregate(Max("volume"))["volume__max"]
        })
    )

    max_volume = forms.IntegerField(
        label="Hámarks rúmmál",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "min": Beer.objects.aggregate(Min("volume"))["volume__min"],
            "max": Beer.objects.aggregate(Max("volume"))["volume__max"]
        })
    )

    styles = forms.MultipleChoiceField(
        label="Bjórstílar",
        choices=generate_style_choices(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    helper = FormHelper()
    helper.form_id = "main-form"
    helper.layout = Layout(
        Div(
            Div(
                Field("beer_name", placeholder="Hluti af nafni bjórs"),
                # css_class="row"
            ),
            Div(
                Field("min_volume", placeholder="Lágmarksrúmmál í ml"),
                # css_class="row"
            ),
            Div(
                Field("max_volume", placeholder="Hámarksrúmmál í ml"),
            ),
            Div(
                Field("styles"),
                # css_class="row"
            )
        )
    )
    helper.form_action = "/search/"



