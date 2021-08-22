from django import forms
from ADMINPANEL.models import Department_Information

class Information(forms.ModelForm):

    class Meta:

        model = Department_Information

        fields = ['NAME', 'SCHOOL_NAME', 'PROGRAM_NAME', 'EMAIL_ID']

        widgets = {

            'NAME':forms.TextInput(attrs={'placeholder': "Enter Faculty Name",
                                    'class':'textinputclass', 'required': True,
                                    }
                                    ),

            'SCHOOL_NAME':forms.TextInput(attrs={'placeholder': "Enter Faculty's School",
                                    'class':'textinputclass', 'required': True,
                                    }
                                    ),

            'PROGRAM_NAME':forms.TextInput(attrs={'placeholder': "Enter Faculty's Program",
                                    'class':'textinputclass', 'required': True,
                                    }
                                    ),

            'EMAIL_ID':forms.EmailInput(attrs={'placeholder': "Enter Faculty's Email",
                                    'class':'textinputclass', 'type':'email','required': True,
                                    }
                                    ),
        }
