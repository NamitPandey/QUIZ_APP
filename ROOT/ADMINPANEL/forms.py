from django import forms
from ADMINPANEL.models import Department_Information
from ADMINPANEL import staticVariables

SCHOOL_CHOICE = (
("School_of_Technology","School_of_Technology".replace("_"," ")),
("School_of_Science","School_of_Science".replace("_"," ")),
("School_of_Management","School_of_Management".replace("_"," ")),
)
PROGRAM_CHOICE = [(x, x.replace("_", " ")) for x in staticVariables.PROGRM_LIST]

class Information(forms.ModelForm):
    SCHOOL_NAME = forms.ChoiceField(choices = SCHOOL_CHOICE, required=True,)
    PROGRAM_NAME = forms.ChoiceField(choices = PROGRAM_CHOICE, required=True)
    class Meta:

        model = Department_Information

        fields = ['NAME', 'SCHOOL_NAME', 'PROGRAM_NAME', 'EMAIL_ID']

        widgets = {

            'NAME':forms.TextInput(attrs={'placeholder': "Enter Faculty Name",
                                    'class':'textinputclass', 'required': True,
                                    }
                                    ),

            # 'SCHOOL_NAME':forms.ChoiceField(attrs={'placeholder': "Enter Faculty's School",
            #                         'class':'textinputclass', 'required': True,
            #                         },
            #                         ),

            # 'PROGRAM_NAME':forms.TextInput(attrs={'placeholder': "Enter Faculty's Program",
            #                         'class':'textinputclass', 'required': True,
            #                         }
            #                         ),

            'EMAIL_ID':forms.EmailInput(attrs={'placeholder': "Enter Faculty's Email",
                                    'class':'textinputclass', 'type':'email','required': True,
                                    }
                                    ),
        }
