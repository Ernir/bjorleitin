from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django.db.models import Min, Max
from django.forms import NumberInput
from beer_search.models import Beer, Style, ContainerType


def generate_choices(model):
    all_objects = model.objects.all()
    return tuple([(object.id, object.name) for object in all_objects])


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

    min_price = forms.IntegerField(
        label="Lágmarksverð",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "min": Beer.objects.aggregate(Min("price"))["price__min"],
            "max": Beer.objects.aggregate(Max("price"))["price__max"]
        })
    )

    max_price = forms.IntegerField(
        label="Hámarksverð",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "min": Beer.objects.aggregate(Min("price"))["price__min"],
            "max": Beer.objects.aggregate(Max("price"))["price__max"]
        })
    )

    min_abv = forms.DecimalField(
        label="Lágmarks áfengisprósenta",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "min": Beer.objects.aggregate(Min("abv"))["abv__min"],
            "max": Beer.objects.aggregate(Max("abv"))["abv__max"]
        })
    )

    max_abv = forms.DecimalField(
        label="Hámarks áfengisprósenta",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "min": Beer.objects.aggregate(Min("abv"))["abv__min"],
            "max": Beer.objects.aggregate(Max("abv"))["abv__max"]
        })
    )

    styles = forms.MultipleChoiceField(
        label="Bjórstílar",
        choices=generate_choices(Style),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    containers = forms.MultipleChoiceField(
        label="Umbúðir",
        # Skipping the "undefined" container.
        choices=generate_choices(ContainerType)[:-1],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    helper = FormHelper()
    helper.form_id = "main-form"
    helper.layout = Layout(
        Div(
            Div(
                Field("beer_name", placeholder="Hluti af nafni bjórs"),
                css_class="col-md-12"
            ),
            Div(
                Field("min_volume", placeholder="Lágmarksrúmmál í ml"),
                css_class="col-md-6"
            ),
            Div(
                Field("max_volume", placeholder="Hámarksrúmmál í ml"),
                css_class="col-md-6"
            ),
            Div(
                Field("min_price", placeholder="Lágmarksverð í kr."),
                css_class="col-md-6"
            ),
            Div(
                Field("max_price", placeholder="Hámarksverð í kr."),
                css_class="col-md-6"
            ),
            Div(
                Field("min_abv", placeholder="%"),
                css_class="col-md-6"
            ),
            Div(
                Field("max_abv", placeholder="%"),
                css_class="col-md-6"
            ),
            Div(
                Field("containers"),
                css_class="checkbox col-md-12"
            ),
            Div(
                Field("styles"),
                css_class="checkbox col-md-12"
            )
        )
    )
    helper.form_action = "/search/"



