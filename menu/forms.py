from django import forms
import datetime
import pytz

from django.forms.extras.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient


def valid_exp_date(value):
    utc = pytz.UTC
    # present = utc.localize(datetime.datetime.now())
    present = datetime.datetime.now()

    if value < utc.localize(present):
        raise forms.ValidationError("Expiration date is not valid")


class MenuForm(forms.ModelForm):
    expiration_date = forms.DateTimeField(
        input_formats=[
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%m/%d/%y'],
        widget=forms.DateTimeInput(format='%m/%d/%Y'),
        validators=[valid_exp_date]
    )

    class Meta:
        model = Menu
        exclude = ('created_date',)
