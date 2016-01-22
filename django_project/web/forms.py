from django.core.validators import URLValidator
from django.forms import forms, fields
from django.utils.translation import ugettext as _


class WeiboCaptureRequestForm(forms.Form):
    """
    Form for weibo capture
    """
    url = fields.CharField(help_text=_('URL need start by http:// or https://'), label=_('URL'))

    def clean_url(self):
        """
        Validate url
        """
        value = self.cleaned_data['url']
        validator = URLValidator(schemes=['http', 'https'])
        validator(value)
        return value