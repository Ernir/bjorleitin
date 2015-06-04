from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Fieldset, Button
from crispy_forms.bootstrap import InlineCheckboxes
from django.db.models import Min, Max
from django.forms import NumberInput
from beer_search.models import Beer, Style, ContainerType, Store


def generate_choices(model):
    all_objects = model.objects.all()
    return tuple([(obj.id, obj.name) for obj in all_objects])


def generate_store_choices():
    stores = Store.objects.all().prefetch_related("region")
    return tuple([(store.id, store.region.name + ": " + store.location)
                  for store in stores])


def min_for_attribute(model, attribute_name):
    return model.objects.filter(available=True). \
        aggregate(Min(attribute_name))[attribute_name + "__min"]


def max_for_attribute(model, attribute_name):
    return model.objects.filter(available=True). \
        aggregate(Max(attribute_name))[attribute_name + "__max"]


class SearchForm(forms.Form):
    """

    Convenience class for defining the main search form on the index.
    """

    beer_name = forms.CharField(
        label="Nafn bjórs",
        required=False
    )

    min_volume = forms.IntegerField(
        label="Lágmarks rúmmál (ml)",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "value": min_for_attribute(Beer, "volume"),
            "min": min_for_attribute(Beer, "volume"),
            "max": max_for_attribute(Beer, "volume"),
        })
    )

    max_volume = forms.IntegerField(
        label="Hámarks rúmmál (ml)",
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
            "value": min_for_attribute(Beer, "price"),
            "min": min_for_attribute(Beer, "price"),
            "max": max_for_attribute(Beer, "price"),
        })
    )

    max_price = forms.IntegerField(
        label="Hámarksverð",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "value": max_for_attribute(Beer, "price"),
            "min": min_for_attribute(Beer, "price"),
            "max": max_for_attribute(Beer, "price"),
        })
    )

    min_abv = forms.DecimalField(
        label="Lágmarks áfengisprósenta",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "value": min_for_attribute(Beer, "abv"),
            "min": min_for_attribute(Beer, "abv"),
            "max": max_for_attribute(Beer, "abv"),
        })
    )

    max_abv = forms.DecimalField(
        label="Hámarks áfengisprósenta",
        required=False,
        widget=NumberInput(attrs={
            "type": "number",
            "value": max_for_attribute(Beer, "abv"),
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

    stores = forms.MultipleChoiceField(
        label="Vínbúðir",
        choices=generate_store_choices(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    containers = forms.MultipleChoiceField(
        label="Umbúðir",
        # Skipping the "undefined" container. # ToDo make not a hack.
        choices=generate_choices(ContainerType)[:-1],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    noteworthy = forms.MultipleChoiceField(
        label="Nýir og árstíðabundnir",
        choices=(
            ("new", "Nýr"),
            ("seasonal", "Árstíðabundinn")
        ),
        required=False
    )

    helper = FormHelper()
    helper.form_id = "main-form"
    helper.layout = Layout(
        Fieldset(
            "Leitarskilyrði",
            Div(
                Div(
                    Field("beer_name", placeholder="Hluti af nafni bjórs"),
                    css_class="col-md-12"
                ),
                css_class="row"
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
                css_id="volume-container",
                css_class="row"
            ),
            Div(
                Div(
                    Field("min_price", placeholder="kr."),
                    css_class="col-md-3"
                ),
                Div(
                    css_id="price-slider",
                    css_class="col-md-6 form-slider"
                ),
                Div(
                    Field("max_price", placeholder="kr."),
                    css_class="col-md-3 "
                ),
                css_id="price_container",
                css_class="row"
            ),
            Div(
                Div(
                    Field("min_abv", placeholder="%"),
                    css_class="col-md-3"
                ),
                Div(
                    css_id="abv-slider",
                    css_class="col-md-6 form-slider"
                ),
                Div(
                    Field("max_abv", placeholder="%"),
                    css_class="col-md-3"
                ),
                css_id="abv-container",
                css_class="row"
            ),
            Div(
                Div(
                    InlineCheckboxes("containers"),
                    css_class="checkbox col-md-12",
                ),
                css_class="row"
            ),
            Div(
                # Div(
                # Div(
                #         Field("stores"),
                #         css_class="checkbox"
                #     ),
                #     css_class="col-md-6"
                # ),
                Div(
                    Div(
                        Field("styles"),
                        css_class="checkbox"
                    ),
                    css_class="col-md-6"
                ),
                css_class="row"
            ),
            Div(
                Div(
                    InlineCheckboxes(
                        "noteworthy",
                        css_class="checkbox"
                    ),
                    css_class="col-md-8"
                ),
                css_class="row"
            )
        ),
    )
    helper.form_action = "/search/"