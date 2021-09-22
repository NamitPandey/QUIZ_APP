from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from ADMINPANEL.models import Department_Information
from MCQ.models import QuizData, UserRegistration

def send_mails():
    """ Function will send mail when result declaration is turned on"""
    helpdeskID =  "abcd@gmail.com"
    student_enroll = list(QuizData.objects.values_list('ENROLLMENT_NUMBER', flat=True).distinct())

    TO_MAIL_DICT = {
    'FACULTY_ID': list(Department_Information.objects.values_list('EMAIL_ID', flat=True).distinct()),
    # 'STUDENT_ID': list(UserRegistration.objects.filter(ENROLLMENT_NUMBER__in=student_enroll).values_list('EMAIL', flat=True).distinct()),
    # 'TEMP_ID':['nix.pandey@gmail.com']
    }

    VISIT_URL = "https://gsfcuniversity.pythonanywhere.com"

    subject = 'TASC PINUPS RESULTS'
    message =  f"""\
Hi,

Your TASC-PINUPS result has been declared.

Please Visit {VISIT_URL} to see you result.

All The Best,
TASC PINUPS
________________________________________________________________________________________________________________________________________________________
** This is an automatically generated email – please do not reply to it. If you have any queries regarding your result please email {helpdeskID} **
________________________________________________________________________________________________________________________________________________________

            """
    email_from = 'tasc.pinups@gmail.com'#settings.EMAIL_HOST_USER
    # recipient_list = ['nix.pandey@gmail.com',
    #                     # 'zalak.kansagra@gsfcuniversity.ac.in',
    #                     # 'sanjukta.goswami@gsfcuniversity.ac.in',
    #                     ]
    for key, val in TO_MAIL_DICT.items():


        recipient_list = TO_MAIL_DICT[key]


        send_mass_mail((
        (subject, message, 'tasc.pinups@gmail.com', recipient_list),
        # new mail for bulk messages
         ),
         fail_silently=False)

def forgot_password_mail(enrollment, newpassword):
    """ Function will send mail to student's mail ID with password"""
    helpdeskID =  "abcd@gmail.com"
    student_enroll = list(QuizData.objects.values_list('ENROLLMENT_NUMBER', flat=True).distinct())

    TO_MAIL_DICT = {
    # 'FACULTY_ID': list(Department_Information.objects.values_list('EMAIL_ID', flat=True).distinct()),
    # 'STUDENT_ID': list(UserRegistration.objects.filter(ENROLLMENT_NUMBER__in=student_enroll).values_list('EMAIL', flat=True).distinct()),
    'TEMP_ID':["zalak.kansagra@gsfcuniversity.ac.in"]#['nix.pandey@gmail.com']
    }

    subject = 'TASC-PINUPS RESET PASSWORD'
    message =  f"""\
Hi {enrollment},

Your new password to access TASC-PINUPS portal.

New Password: {newpassword}

Thanks,
TASC PINUPS
________________________________________________________________________________________________________________________________________________________
** This is an automatically generated email – please do not reply to it. If you have any queries regarding your result please email {helpdeskID} **
________________________________________________________________________________________________________________________________________________________

            """
    email_from = 'tasc.pinups@gmail.com'#settings.EMAIL_HOST_USER

    for key, val in TO_MAIL_DICT.items():


        recipient_list = TO_MAIL_DICT[key]


        send_mass_mail((
        (subject, message, 'tasc.pinups@gmail.com', recipient_list),
        # new mail for bulk messages
         ),
         fail_silently=False)
