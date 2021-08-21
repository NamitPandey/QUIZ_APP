from django.conf import settings
from django.core.mail import send_mail, send_mass_mail

def send_mails():
    """ Function will send mail when result declaration is turned on"""
    VISIT_URL = "https://gsfcuniversity.pythonanywhere.com"

    subject = 'TASC PINUPS RESULTS'
    message =  f"""\
Hi Candidate_Name,

Your TASC-PINUPS result has been declared.

Please Visit {VISIT_URL} to see you result.

All The Best,
TASC PINUPS
________________________________________________________________________________________________________________________________________________________
** This is an automatically generated email – please do not reply to it. If you have any queries regarding your result please email abcd@gmail.com **
________________________________________________________________________________________________________________________________________________________

            """
    email_from = 'tasc.pinups@gmail.com'#settings.EMAIL_HOST_USER
    recipient_list = ['nix.pandey@gmail.com',
                        # 'zalak.kansagra@gsfcuniversity.ac.in', 
                        # 'sanjukta.goswami@gsfcuniversity.ac.in',
                        ]

    send_mass_mail((
    (subject, message, 'tasc.pinups@gmail.com', recipient_list),
    # new mail for bulk messages
     ),
     fail_silently=False)
