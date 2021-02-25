from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# django models import below
from .models import (Question, UserRegistration, AllowedEnrollments)
# python packages import below
import  numpy as np

# all static packages import below
from . import (PAGE_MAPPER, staticVariables)

# Create your views here.
global CATEGORY, RNDM_NMBR

def get_random_numbers(max_number):

    serielList = []
    counter = 1

    while counter < max_number+1:

        number = np.random.randint(1, max_number+1)

        if number in serielList:

            pass

        else:

            serielList.append(number)

            counter+=1

    return serielList

""" DEFAULT PAGE TO REDIRECT WHEN THE USER IS NOT LOGGED IN"""
def login_message(request):

    return render(request, 'MAIN_PAGE/login_error.html')

""" USER REGISTRATION FORM """
def user_registration(request):

    pageDictKey = 'register'
    context = {}

    if request.method == "POST":

        firstname = request.POST.get("firstname") # getting username
        lastname = request.POST.get("lastname") # getting username
        enrollment = request.POST.get("enrollment").lower() # getting username
        # email = request.POST.get("email") # getting username
        password_main = request.POST.get("password_main") # getting password
        password_confirm = request.POST.get("password_confirm") # getting password confirm
        # gender = request.POST.get("gender") # getting user's gender
        # semester = request.POST.get("semester") # getting user's semesters
        # school = request.POST.get("school") # getting user's program
        # program = request.POST.get("program") # getting user's program
        # phone = request.POST.get("phone") # getting contact number
        # company = request.POST.get("companyname") # getting company name

        allowedEnrollments = [_.lower() for _ in list(AllowedEnrollments.objects.values_list("ENROLLMENT_NUMBER", flat=True).distinct())]# enrollment numbers of students allowed to take the test

        if enrollment not in allowedEnrollments:

            context.update({'MSG':"ERROR", 'INFO': "ENTER A REGISTERED ENROLLMENT NUMBER"})

        elif User.objects.filter(username=enrollment).exists(): # check to see if user name exists

            context.update({'MSG':"ERROR", 'INFO': "ENROLLMENT ALREADY EXISTS"})

        # elif email.split("@")[-1].lower() not in ["gmail.com"]:
        #
        #     context.update({'MSG':"ERROR", 'INFO': "ENTER A VALID EMAIL ADDRESS"})
        #
        # elif User.objects.filter(email=email).exists():# check to see if email address exists
        #
        #     context.update({'MSG':"ERROR", 'INFO': "EMAIL ALREADY EXISTS"})

        elif password_main != password_confirm: # check if password match with confirm password

            context.update({'MSG':"ERROR", 'INFO': "PASSWORD DID NOT MATCH"})

        # elif int(semester) > 7:
        #
        #     context.update({'MSG':"ERROR", 'INFO': "SEMESTER CANNOT BE GREATER THAN 7"})
        #
        # elif int(semester) < 1:
        #
        #     context.update({'MSG':"ERROR", 'INFO': "SEMESTER CANNOT BE LESS THAN 1"})
        #
        # elif UserRegistration.objects.filter(CONTACT=phone).exists():# check to see if contact number exists
        #
        #     context.update({'MSG':"ERROR", 'INFO': "MOBILE NUMBER ALREADY REGISTERED"})

        else:
            # creating new user in database

            userProfile = UserRegistration.objects.create(
            FIRST_NAME=firstname.title(),
            LAST_NAME=lastname.title(),
            ENROLLMENT_NUMBER=enrollment,
            # EMAIL=email,
            # GENDER =gender,
            # SEMESTER =semester,
            # SCHOOL =school,
            # PROGRAM =program,
            # CONTACT = phone,
            )
            userProfile.save()

            user = User.objects.create_user(
                                            username=enrollment,
                                            password=password_main,
                                            # email=email,
                                            first_name=firstname.title(),
                                            last_name=lastname.title(),
                                            )

            user.save() #saving the user to database

            context.update({'MSG':"CREATED"})


    return render(request, PAGE_MAPPER.pageDict[pageDictKey], context=context)

""" PAGE SEEN AS THE SITE OPENS ALSO A LOGIN PAGE"""
@login_required
def homepage(request):

    pageDictKey = 'homepage'

    context={
    "PAGE_MSG": "HOMEPAGE",
    "mainID":1,
    "randmNmbr":f"{np.random.randint(834, 10000)}",
    "randmNmbr2":f"{np.random.randint(834750, 1000000)}",
    "genderList": staticVariables.GENDR_LIST,
    "schoolList": staticVariables.SCHOL_LIST,
    "programsList": staticVariables.PROGRM_LIST,
    # "counter":np.random.randint(1, 5),
    }

    return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)

""" PAGE AS SEEN BY STUDENT WHEN THEY LOGIN """
@login_required
def students_portal(request):

    pageDictKey = 'students_portal'

    context={
    "PAGE_MSG": "HOMEPAGE",
    "mainID":1,
    "randmNmbr":f"{np.random.randint(834, 10000)}",
    "randmNmbr2":f"{np.random.randint(834750, 1000000)}",
    "genderList": staticVariables.GENDR_LIST,
    "schoolList": staticVariables.SCHOL_LIST,
    "programsList": staticVariables.PROGRM_LIST,
    # "counter":np.random.randint(1, 5),
    }

    return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)

@login_required
def quiz_page(request,randmNmbr,mainID,randmNmbr2, counter):

    pageDictKey = 'quiz_page'

    context={
    "PAGE_MSG": staticVariables.CATEGORY[mainID],
    "mainID":mainID,
    "randmNmbr":f"{np.random.randint(834750, 1000000)}",
    "randmNmbr2":f"{np.random.randint(834750, 1000000)}",
    "counter":counter,
    "mainID":mainID,
    # "qstn":qstn,
    }

    if request.method == 'GET':

        serialList = get_random_numbers(4)
        qstn = Question.objects.filter(
                                    CATEGORY__iexact=staticVariables.CATEGORY[mainID],
                                    SR_NO__iexact=np.random.randint(1, 4),
                                    )
        context.update({"qstn":qstn,})

    if request.method == 'POST':
        print(counter)
        answer1 = request.POST.get("exampleRadios")
        # answer2 = request.POST.get("choiceTwo")
        # answer3 = request.POST.get("choiceThree")
        # answer4 = request.POST.get("choiceFour")
        print(answer1)
        qstn = Question.objects.filter(
                                    CATEGORY__iexact=staticVariables.CATEGORY[mainID],
                                    SR_NO__iexact=np.random.randint(1, 4),
                                    )

        # serialList = serialList.copy().remove(counter)

        context.update({"qstn":qstn,})




    return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)
