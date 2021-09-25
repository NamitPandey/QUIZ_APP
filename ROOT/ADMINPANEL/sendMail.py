from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from ADMINPANEL.models import Department_Information
from MCQ.models import QuizData, UserRegistration

helpdeskID =  "abcd@gmail.com"
VISIT_URL = "https://gsfcuniversity.pythonanywhere.com"
FORGOT_URL = VISIT_URL+"/department/iforgot"

def send_mails():
    """ Function will send mail when result declaration is turned on"""

    student_enroll = list(QuizData.objects.values_list('ENROLLMENT_NUMBER', flat=True).distinct())

    TO_MAIL_DICT = {
    'FACULTY_ID': list(Department_Information.objects.values_list('EMAIL_ID', flat=True).distinct()),
    'STUDENT_ID': list(Department_Information.objects.values_list('EMAIL_ID', flat=True).distinct()),#list(UserRegistration.objects.filter(ENROLLMENT_NUMBER__in=student_enroll).values_list('EMAIL', flat=True).distinct()),
    # 'TEMP_ID':['nix.pandey@gmail.com']
    }

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
    facultymessage =  f"""\
    Hi,

    Admin has enabled TASC-PINUPS results. Students now have access to their result section.

    Thanks,
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

        if key == "FACULTY_ID":

            send_mass_mail((
            (subject, facultymessage, 'tasc.pinups@gmail.com', recipient_list),
            # new mail for bulk messages
             ),
             fail_silently=False)
        else:
            send_mass_mail((
            (subject, message, 'tasc.pinups@gmail.com', recipient_list),
            # new mail for bulk messages
             ),
             fail_silently=False)

def forgot_password_mail(candidate_name, enrollment, newpassword, sendTo='0'):
    """ Function will send mail to student's mail ID with password"""

    student_enroll = list(QuizData.objects.values_list('ENROLLMENT_NUMBER', flat=True).distinct())

    TO_MAIL_DICT = {
    # 'FACULTY_ID': list(Department_Information.objects.values_list('EMAIL_ID', flat=True).distinct()),
    # 'STUDENT_ID': list(UserRegistration.objects.filter(ENROLLMENT_NUMBER__in=student_enroll).values_list('EMAIL', flat=True).distinct()),
    'TEMP_ID':["zalak.kansagra@gsfcuniversity.ac.in"]#
    # 'TO': [enrollment+"@gsfcuniversity.ac.in"]
    }

    if sendTo != '0':

        TO_MAIL_DICT = {
        'TO': [sendTo.lower()]
        }

    subject = 'TASC-PINUPS RESET PASSWORD'
    message =  f"""\
Hi {candidate_name},

Your new password to access TASC-PINUPS portal is below. You can access the portal via {VISIT_URL}

Username: {enrollment.lower()}
New Password: {newpassword}

Thanks,
TASC PINUPS
________________________________________________________________________________________________________________________________________________________
** This is an automatically generated email – please do not reply to it. For any queries reach us at {helpdeskID} **
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


def registration_successfull_mail(facultyName, facultyEmail):
    """ Function will send mail to faculty's mail ID with temp password"""

    TO_MAIL_DICT = {
    'FACULTY_ID': [facultyEmail],
    # 'TEMP_ID': ["nix.pandey@gmail.com"]
    }

    subject = 'TASC-PINUPS RESET PASSWORD'
    message =  f"""\
Hi {facultyName},

Welcome to TASC-PINUPS. Your credentials to access dashboard are listed below. You can access the portal via {VISIT_URL}

Username: {facultyEmail.lower()}
Password: tascPortal@21022021

**WE ADVISE YOU TO CHANGE YOUR PASSWORD AFTER YOU LOGIN TO THE PORTAL FOR THE FIRST TIME**

In case you ever forget your password you can access {FORGOT_URL} to reset it.

Thanks,
TASC PINUPS
________________________________________________________________________________________________________________________________________________________
** This is an automatically generated email – please do not reply to it. For any queries reach us at {helpdeskID} **
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
