from django.forms import ModelForm, Select, DateInput, TextInput
from fuelest.models import UserInfo, Address, Quote
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class ProfileForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['name']
        labels = {
            'name': _('Full name'),
        }

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['address1', 'address2', 'city', 'state', 'zip']
        labels = {
            'address1': _('Address line 1'),
            'address2': _('Address line 2'),
            'city': _('City'),
            'state': _('State'),
            'zip': _('ZIP Code'),
        }
    def clean(self):
        cleaned_data = super(AddressForm, self).clean()
        zip = cleaned_data.get('zip')
        if len(str(zip)) not in [5, 9]:
            self.add_error(None, ValidationError("ZIP must either be 5 digits or 9"))
            print("Error" + str(len(str(zip))))
        return cleaned_data

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ['gallons', 'date']
        labels = {
            'gallons': _('Gallons requested'),
            'date': _('Date of delivery'),
        }
        widgets = {
            'date': DateInput(attrs={'class':'datepicker'}),
        }