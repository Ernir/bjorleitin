from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from django.db.models import Min, Max
from django.forms import NumberInput
from beer_search.models import Beer, Style, ContainerType


def generate_choices(model):
    all_objects = model.objects.all()
    return tuple([(object.id, object.name) for object in all_objects])


def min_for_attribute(model, attribute_name):
    return model.objects.filter(available=True).\
               aggregate(Min(attribute_name))[attribute_name + "__min"]


def max_for_attribute(model, attribute_name):
    return model.objects.filter(available=True).\
               aggregate(Max(attribute_name))[attribute_name + "__max"]


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
            "value": min_for_attribute(Beer, "volume"),
            "min": min_for_attribute(Beer, "volume"),
            "max": max_for_attribute(Beer, "volume"),
        })
    )

    max_volume = forms.IntegerField(
        label="Hámarks rúmmál",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "value": max_for_attribute(Beer, "volume"),
            "min": min_for_attribute(Beer, "volume"),
            "max": max_for_attribute(Beer, "volume"),
        })
    )

    min_price = forms.IntegerField(
        label="Lágmarksverð",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "min": min_for_attribute(Beer, "price"),
            "max": max_for_attribute(Beer, "price"),
        })
    )

    max_price = forms.IntegerField(
        label="Hámarksverð",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "min": min_for_attribute(Beer, "price"),
            "max": max_for_attribute(Beer, "price"),
        })
    )

    min_abv = forms.DecimalField(
        label="Lágmarks áfengisprósenta",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "min": min_for_attribute(Beer, "abv"),
            "max": max_for_attribute(Beer, "abv"),
        })
    )

    max_abv = forms.DecimalField(
        label="Hámarks áfengisprósenta",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "min": min_for_attribute(Beer, "abv"),
            "max": max_for_attribute(Beer, "abv"),
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
        # Skipping the "undefined" container. # ToDo make not a hack.
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
                Div(
                    Field("min_volume", placeholder="ml"),
                    css_class="col-md-3"
                ),
                Div(
                    css_id="volume-slider",
                    css_class="col-md-6 form-slider"
                ),
                Div(
                    Field("max_volume", placeholder="ml"),
                    css_class="col-md-3"
                ),
                css_id="volume-container"
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



