import autocomplete_light

from models import Patient

autocomplete_light.register(Patient, search_fields=('name', 'name_ascii',),
    autocomplete_js_attributes={'placeholder': 'invoice_date ..'})


class AutocompletePatient(autocomplete_light.AutocompleteModelBase):
    autocomplete_js_attributes={'placeholder': 'region name ..'}

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        country_id = self.request.GET.get('country_id', None)

        choices = self.choices.all()
        if q:
            choices = choices.filter(name_ascii__icontains=q)
        if country_id:
            choices = choices.filter(country_id=country_id)

        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(Patient, AutocompletePatient)