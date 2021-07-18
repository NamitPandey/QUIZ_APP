from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Count

# django models import below
from .models import (Question, UserRegistration,
                    AllowedEnrollments, EnrollemntsForQuiz, QuizData)
# python packages import below
import pandas as pd
import  numpy as np
import datetime

# all static packages import below
from . import (PAGE_MAPPER, staticVariables)

# Create your views here.
global CATEGORY, RNDM_NMBR

def get_category(enrollmentNo):

        countCheck = 10

        catList = staticVariables.CATEGORY_LIST

        # catID = np.random.randint(0, len(catList))

        catCheck = QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=enrollmentNo).values("CATEGORY").annotate(CAT_count=Count('CATEGORY')).order_by("CATEGORY").to_dataframe()

        catCount = catCheck.query(f"CAT_count == {countCheck}")['CATEGORY'].values.tolist()

        for cat in catList:

            if cat not in catCount:

                return cat

            else:

                continue
                # catList.remove(cat)

        # for ind, val in enumerate(catList):
        #
        #     try:
        #         if catCheck.query(f"CATEGORY == '{catList[catID]}'")['CAT_count'][0] == countCheck:
        #
        #             catList.remove(catList[catID])
        #
        #             return catID+1
        #
        #     except:
        #
        #         pass



        # for ind, val in enumerate(catList):
        #
        #     count = catCheck.query(f"CATEGORY == {val}")['CAT_count'][0]
            # if



def get_mainID(mainID, qstnID, enrollmentNo):

    categoryName = get_category(enrollmentNo)

    toalQstn = list(Question.objects.filter(CATEGORY__iexact=categoryName).values_list("QUESTION_ID", flat=True))[-1] + 1 #Question.objects.all().count()+1

    chooseFrom = list(Question.objects.filter(CATEGORY__iexact=categoryName).values_list("QUESTION_ID", flat=True))

    lowerVal = list(Question.objects.filter(CATEGORY__iexact=categoryName).values_list("QUESTION_ID", flat=True))[0]

    loopCounter = 0

    while loopCounter < 1:

        if mainID not in qstnID:

            loopCounter+=1

        else:

            mainID = np.random.choice(chooseFrom,1)[0]#np.random.randint(lowerVal, toalQstn)

    return mainID

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

        enrollment = request.POST.get("enrollment").lower() # getting enrollment number
        firstname = request.POST.get("firstname") # getting username
        lastname = request.POST.get("lastname") # getting username



        gender = request.POST.get("gender") # getting user's gender
        semester = request.POST.get("semester") # getting user's semesters

        school = request.POST.get("school") # getting user's program
        program = request.POST.get("program") # getting user's program

        # email = request.POST.get("email") # getting username
        password_main = request.POST.get("password_main") # getting password
        password_confirm = request.POST.get("password_confirm") # getting password confirm

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
            GENDER =gender,
            SEMESTER =semester,
            SCHOOL =school,
            PROGRAM =program,
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
    toalQstn = Question.objects.all().count()+1
    context={
    "PAGE_MSG": "HOMEPAGE",
    "mainID":np.random.randint(1, 5),
    "randmNmbr":f"{np.random.randint(834, 10000)}",
    "randmNmbr2":f"{np.random.randint(834750, 1000000)}",
    "genderList": staticVariables.GENDR_LIST,
    "schoolList": staticVariables.SCHOL_LIST,
    "programsList": staticVariables.PROGRM_LIST,
    'disabled':'',
    "counter":1,
    }

    # list uploaded by admin to grant access to students to take the test
    approvedEnrollment = list(EnrollemntsForQuiz.objects.values_list("ENROLLMENT_NUMBER", flat=True).distinct())+['admin']

    if request.user.username not in approvedEnrollment:

        context.update({'disabled':'disabled',})

    return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)

@login_required
def quiz_page(request,randmNmbr,mainID,randmNmbr2, counter, resultedTime):

    pageDictKey = 'quiz_page'
        # list uploaded by admin to grant access to students to take the test
        # REMOVE ADMIN FROM THE LIST DURING DEPLOYMENT
    approvedEnrollment = list(EnrollemntsForQuiz.objects.values_list("ENROLLMENT_NUMBER", flat=True).distinct())+['admin']

    context={
    "PAGE_MSG": staticVariables.CATEGORY[1],
    "mainID":mainID,
    "randmNmbr":f"{np.random.randint(834750, 1000000)}",
    "randmNmbr2":f"{np.random.randint(834750, 1000000)}",
    "counter":counter,
    # "mainID":mainID,
    'AUTHORIZED':'YES',
    # "QUIZ_STAT": "GO_ON",/
    }
    # check question id
    quizEnd = 40

    qstnID = list(QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username).values_list("QUESTION_ID", flat=True))
        # checking students enrollment present in allowed list or not to take the test
    if request.user.username not in approvedEnrollment:

        context.update({'AUTHORIZED':'NO','COMN_MSG': "YOU ARE NOT AUTHORIZED TO TAKE THE TEST!"})

        return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)

    if len(qstnID) == quizEnd:

        context.update({'AUTHORIZED':'NO','COMN_MSG': "YOU HAVE ALREADY TAKEN YOUR TEST. PLEASE WAIT FOR THE RESULT TO BE DECLARED."})

        return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)

    if request.method == 'GET':

        mainID = get_mainID(mainID, qstnID, request.user.username)

        # getting time and adding 45 minutes for test time limit
        nowTime=datetime.datetime.now()
        maxTime = nowTime+datetime.timedelta(minutes=45)
        print(nowTime, maxTime)
        resultedTime = datetime.datetime.strptime(str(maxTime - nowTime), "%H:%M:%S")

        # serialList = get_random_numbers(4)
        qstn = Question.objects.filter(
                                    # CATEGORY__iexact=staticVariables.CATEGORY[2],
                                    QUESTION_ID__iexact=mainID,
                                    ).order_by('?')
        context.update({"qstn":qstn, "mainID":mainID,
                        "nowTime":nowTime, "resultedTime":resultedTime,
                        "maxTime":maxTime
                        })

    if request.method == 'POST':

        nowTime=datetime.datetime.now()
        maxTime = datetime.datetime.strptime(resultedTime, "%Y-%m-%d %H:%M:%S.%f")
        try:
            resultedTime = datetime.datetime.strptime(str(maxTime - nowTime), "%H:%M:%S.%f")
        except:
            resultedTime = datetime.datetime.strptime(str(nowTime - maxTime), "%H:%M:%S.%f")

        answer1 = request.POST.get("exampleRadios")

        actQST = list(Question.objects.filter(
                                    QUESTION_ID__iexact=mainID,
                                    ).values_list("QUESTION", flat=True))[0]
        qstnCAT = list(Question.objects.filter(
                                    QUESTION_ID__iexact=mainID,
                                    ).values_list("CATEGORY", flat=True))[0]
        CrrctAnswr = list(Question.objects.filter(
                                    QUESTION_ID__iexact=mainID,
                                    ).values_list("CORRECT", flat=True))[0]

        QuizData.objects.create(
        QUESTION_ID=mainID,
        ACTUAL_QUESTION=actQST,
        ENROLLMENT_NUMBER=request.user.username,
        ANSWER=answer1,
        CORRECT_ANSWER=CrrctAnswr,
        CATEGORY=qstnCAT,
        ).save()

        if counter == quizEnd:

            user = EnrollemntsForQuiz.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username)

            user.delete()
            # nowTime=datetime.datetime.now()
            # maxTime = datetime.datetime.strptime(resultedTime, "%Y-%m-%d %H:%M:%S.%f")
            # resultedTime = datetime.datetime.strptime(str(maxTime - nowTime), "%H:%M:%S.%f")

            context.update({'AUTHORIZED':'NO',
             'COMN_MSG': "THANK YOU FOR TAKING THE TEST. RESULTS WILL BE ANNOUNCED SOON. ALL THE BEST",
             "counter":counter+1,"mainID":mainID, })

        else:
            qstnID = list(QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username).values_list("QUESTION_ID", flat=True))
            mainID = get_mainID(mainID, qstnID, request.user.username)

            # get the response of user and a store to database fetched from GET request
            qstn = Question.objects.filter(
                                        # CATEGORY__iexact=staticVariables.CATEGORY[2],
                                        QUESTION_ID__iexact=mainID,
                                        ).order_by('?')

        # serialList = serialList.copy().remove(counter)

            context.update({"qstn":qstn, "counter":counter+1,"mainID":mainID,
                        "nowTime":nowTime, "resultedTime":resultedTime,
                        "maxTime":maxTime
                        })


    return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)

def time_out(request, username):

    pageDictKey = 'quiz_page'

    user = EnrollemntsForQuiz.objects.filter(ENROLLMENT_NUMBER__iexact=username)

    user.delete()

    context={'AUTHORIZED':'NO',
     'COMN_MSG': "TIMES UP ! THANK YOU FOR TAKING THE TEST. RESULTS WILL BE ANNOUNCED SOON. ALL THE BEST",
     }

    return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)
