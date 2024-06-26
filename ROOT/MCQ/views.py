from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Count

# django models import below
from .models import (Question, UserRegistration,
                    AllowedEnrollments, EnrollemntsForQuiz, QuizData, FeedbackForm)
# python packages import below
import pandas as pd
import  numpy as np
import datetime

# all static packages import below
from . import (PAGE_MAPPER, staticVariables)
from .password_gen import generate_random_password
from ADMINPANEL.views import get_result_status
from ADMINPANEL.university_data import UniversityData
from ADMINPANEL.sendMail import forgot_password_mail
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
        # firstname = request.POST.get("firstname") # getting username
        # lastname = request.POST.get("lastname") # getting username
        #
        #
        #
        # gender = request.POST.get("gender") # getting user's gender
        # semester = request.POST.get("semester") # getting user's semesters

        school = request.POST.get("school") # getting user's program
        program = request.POST.get("program") # getting user's program

        # email = request.POST.get("email") # getting username
        password_main = request.POST.get("password_main") # getting password
        password_confirm = request.POST.get("password_confirm") # getting password confirm

        university = UniversityData() # opening up university data file
        # University_data = UniversityData.get_university_data()
        searchRes = university.search_enrollment(enrollment)
        # phone = request.POST.get("phone") # getting contact number
        # company = request.POST.get("companyname") # getting company name

        allowedEnrollments = [_.lower() for _ in list(AllowedEnrollments.objects.values_list("ENROLLMENT_NUMBER", flat=True).distinct())]# enrollment numbers of students allowed to take the test



        if User.objects.filter(username=enrollment).exists(): # check to see if user name exists

            context.update({'MSG':"ERROR", 'INFO': "ENROLLMENT ALREADY EXISTS"})

        elif (enrollment not in allowedEnrollments) or (searchRes == 'NO'):

            context.update({'MSG':"ERROR", 'INFO': "ENTER A REGISTERED ENROLLMENT NUMBER"})

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
            firstname, lastname, semester, gender = university.get_enrollment_detail(enrollment)

            userProfile = UserRegistration.objects.create(
            FIRST_NAME=firstname.title(),
            LAST_NAME=lastname.title(),
            ENROLLMENT_NUMBER=enrollment,
            EMAIL=str(enrollment)+"@gsfcuniversity.ac.in",
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
                                            email=str(enrollment)+"@gsfcuniversity.ac.in",
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
    chooseFrom = list(Question.objects.filter(CATEGORY__iexact='LOGICAL').values_list("QUESTION_ID", flat=True))

    mainID = np.random.choice(chooseFrom,1)[0]
    loggedin_detail = UserRegistration.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username)

    context={
    "PAGE_MSG": "HOMEPAGE",
    "mainID":mainID,
    "randmNmbr":f"{np.random.randint(834, 10000)}",
    "randmNmbr2":f"{np.random.randint(834750, 1000000)}",
    "genderList": staticVariables.GENDR_LIST,
    "schoolList": staticVariables.SCHOL_LIST,
    "programsList": staticVariables.PROGRM_LIST,
    'disabled':'',
    "counter":1,
    "resultStat":get_result_status(),
    "student_detail":loggedin_detail,
    }

    # list uploaded by admin to grant access to students to take the test
    approvedEnrollment = list(EnrollemntsForQuiz.objects.values_list("ENROLLMENT_NUMBER", flat=True).distinct())#+['admin']

    if request.user.is_superuser:

        access = 'granted'

    else:
        access = 'denied'
        try:
            startTime = list(EnrollemntsForQuiz.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username).values_list("START_TIME", flat=True))[0]
            endtTime = list(EnrollemntsForQuiz.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username).values_list("END_TIME", flat=True))[0]

        except:

            context.update({'disabled':'disabled',})
            return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)


    if request.user.username not in approvedEnrollment:

        context.update({'disabled':'disabled',})

    if access == 'denied':
        if datetime.datetime.now() <= startTime or datetime.datetime.now() > endtTime:
            context.update({'disabled':'disabled',})

    return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)

def feedback(request):


    if request.method == 'POST':

        answer_one = request.POST.get('question_one')
        answer_two = request.POST.get('question_two')
        answer_three = request.POST.getlist('question_three')
        comments = request.POST.get('comments')

        if comments.strip() == "" or comments.strip() == " ":

            comments = "999"

        if len(answer_three) == 4:

            FeedbackForm.objects.create(
            QSTN_ONE='Did you enjoy taking the Test ?',
            QSTN_TWO='The Test you found ?',
            QSTN_THREE='The experience of the Test reveals that ?',
            QSTN_ONE_ANSWR = answer_one,
            QSTN_TWO_ANSWR = answer_two,
            QSTN_THREE_ANSWR_CHOICE_1 = answer_three[0],
            QSTN_THREE_ANSWR_CHOICE_2 = answer_three[1],
            QSTN_THREE_ANSWR_CHOICE_3 = answer_three[2],
            QSTN_THREE_ANSWR_CHOICE_4 = answer_three[3],
            COMMENTS = comments,
            ).save()

        elif len(answer_three) == 3:

            FeedbackForm.objects.create(
            QSTN_ONE='Did you enjoy taking the Test ?',
            QSTN_TWO='The Test you found ?',
            QSTN_THREE='The experience of the Test reveals that ?',
            QSTN_ONE_ANSWR = answer_one,
            QSTN_TWO_ANSWR = answer_two,
            QSTN_THREE_ANSWR_CHOICE_1 = answer_three[0],
            QSTN_THREE_ANSWR_CHOICE_2 = answer_three[1],
            QSTN_THREE_ANSWR_CHOICE_3 = answer_three[2],
            COMMENTS = comments,
            ).save()

        elif len(answer_three) == 2:

            FeedbackForm.objects.create(
            QSTN_ONE='Did you enjoy taking the Test ?',
            QSTN_TWO='The Test you found ?',
            QSTN_THREE='The experience of the Test reveals that ?',
            QSTN_ONE_ANSWR = answer_one,
            QSTN_TWO_ANSWR = answer_two,
            QSTN_THREE_ANSWR_CHOICE_1 = answer_three[0],
            QSTN_THREE_ANSWR_CHOICE_2 = answer_three[1],
            COMMENTS = comments,
            ).save()

        elif len(answer_three) == 1:

            FeedbackForm.objects.create(
            QSTN_ONE='Did you enjoy taking the Test ?',
            QSTN_TWO='The Test you found ?',
            QSTN_THREE='The experience of the Test reveals that ?',
            QSTN_ONE_ANSWR = answer_one,
            QSTN_TWO_ANSWR = answer_two,
            QSTN_THREE_ANSWR_CHOICE_1 = answer_three[0],
            COMMENTS = comments,
            ).save()


    return render(request, "MAIN_PAGE/thank_you_msg.html")
    # return render(request, 'MAIN_PAGE/testPage.html')


@login_required
def quiz_page(request,randmNmbr,mainID,randmNmbr2, counter, resultedTime):

    pageDictKey = 'quiz_page'
        # list uploaded by admin to grant access to students to take the test
        # REMOVE ADMIN FROM THE LIST DURING DEPLOYMENT
    approvedEnrollment = list(EnrollemntsForQuiz.objects.values_list("ENROLLMENT_NUMBER", flat=True).distinct())#+['admin']

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

        schoolName = list(UserRegistration.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username).values_list("SCHOOL", flat=True))[0]
        prgName = list(UserRegistration.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username).values_list("PROGRAM", flat=True))[0]
        semstr = list(UserRegistration.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username).values_list("SEMESTER", flat=True))[0]
        gndr = list(UserRegistration.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username).values_list("GENDER", flat=True))[0]



        QuizData.objects.create(
        QUESTION_ID=mainID,
        ACTUAL_QUESTION=actQST,
        ENROLLMENT_NUMBER=request.user.username,
        ANSWER=answer1,
        SCHOOL = schoolName,
        PROGRAM = prgName,
        CORRECT_ANSWER=CrrctAnswr,
        CATEGORY=qstnCAT,
        SEMESTER=semstr,
        GENDER=gndr,
        ).save()

        if counter == quizEnd:

            user = EnrollemntsForQuiz.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username)
            # put feedback form function here
            user.delete()
            # nowTime=datetime.datetime.now()
            # maxTime = datetime.datetime.strptime(resultedTime, "%Y-%m-%d %H:%M:%S.%f")
            # resultedTime = datetime.datetime.strptime(str(maxTime - nowTime), "%H:%M:%S.%f")

            context.update({'AUTHORIZED':'NO', 'feedback':'YES',
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
     'COMN_MSG': "TIMES UP! THANK YOU FOR TAKING THE TEST. RESULTS WILL BE ANNOUNCED SOON. ALL THE BEST",
     }

    return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)



def feedback_time_out(request, username):

    if request.method == 'POST':

        answer_one = request.POST.get('question_one')
        answer_two = request.POST.get('question_two')
        answer_three = request.POST.getlist('question_three')
        comments = request.POST.get('comments')

        if comments.strip() == "" or comments.strip() == " ":

            comments = "999"

        if len(answer_three) == 4:

            FeedbackForm.objects.create(
            QSTN_ONE='Did you enjoy taking the Test ?',
            QSTN_TWO='The Test you found ?',
            QSTN_THREE='The experience of the Test reveals that ?',
            QSTN_ONE_ANSWR = answer_one,
            QSTN_TWO_ANSWR = answer_two,
            QSTN_THREE_ANSWR_CHOICE_1 = answer_three[0],
            QSTN_THREE_ANSWR_CHOICE_2 = answer_three[1],
            QSTN_THREE_ANSWR_CHOICE_3 = answer_three[2],
            QSTN_THREE_ANSWR_CHOICE_4 = answer_three[3],
            COMMENTS = comments,
            ).save()

        elif len(answer_three) == 3:

            FeedbackForm.objects.create(
            QSTN_ONE='Did you enjoy taking the Test ?',
            QSTN_TWO='The Test you found ?',
            QSTN_THREE='The experience of the Test reveals that ?',
            QSTN_ONE_ANSWR = answer_one,
            QSTN_TWO_ANSWR = answer_two,
            QSTN_THREE_ANSWR_CHOICE_1 = answer_three[0],
            QSTN_THREE_ANSWR_CHOICE_2 = answer_three[1],
            QSTN_THREE_ANSWR_CHOICE_3 = answer_three[2],
            COMMENTS = comments,
            ).save()

        elif len(answer_three) == 2:

            FeedbackForm.objects.create(
            QSTN_ONE='Did you enjoy taking the Test ?',
            QSTN_TWO='The Test you found ?',
            QSTN_THREE='The experience of the Test reveals that ?',
            QSTN_ONE_ANSWR = answer_one,
            QSTN_TWO_ANSWR = answer_two,
            QSTN_THREE_ANSWR_CHOICE_1 = answer_three[0],
            QSTN_THREE_ANSWR_CHOICE_2 = answer_three[1],
            COMMENTS = comments,
            ).save()

        elif len(answer_three) == 1:

            FeedbackForm.objects.create(
            QSTN_ONE='Did you enjoy taking the Test ?',
            QSTN_TWO='The Test you found ?',
            QSTN_THREE='The experience of the Test reveals that ?',
            QSTN_ONE_ANSWR = answer_one,
            QSTN_TWO_ANSWR = answer_two,
            QSTN_THREE_ANSWR_CHOICE_1 = answer_three[0],
            COMMENTS = comments,
            ).save()
        print("black box: ",username)
        user = EnrollemntsForQuiz.objects.filter(ENROLLMENT_NUMBER__iexact=username)

        user.delete()

        context={'AUTHORIZED':'NO',
         'COMN_MSG': "TIMES UP! THANK YOU FOR TAKING THE TEST. RESULTS WILL BE ANNOUNCED SOON. ALL THE BEST",
         }

        return render(request, "MAIN_PAGE/thank_you_msg.html", context)

    return render(request, "MAIN_PAGE/feedback_page.html")

def forgot_password(request):

    pageDictKey = 'forgot_password'

    context = {"reset":"ENABLED"}

    if request.method == "POST":

        username = request.POST.get("username").lower()

        candidate_list = list(UserRegistration.objects.all().values_list("FIRST_NAME", flat=True))
        try:
            candidate_name = list(UserRegistration.objects.filter(ENROLLMENT_NUMBER__iexact=username).values_list("FIRST_NAME", flat=True))[0]

        except:
            candidate_name = username

        if candidate_name in candidate_list:

            user = User.objects.get(username__iexact=username)
            newPassword = generate_random_password()
            forgot_password_mail(candidate_name, username, newPassword)

            user.set_password(newPassword)
            user.save()

            context.update({
            "reset":"DISABLED",
            "HEADER":"Password Reset",
            "MSG": f"Your new password has been mailed to your <span style='color:black;'>{username}@gsfc.ac.in</span> Email-ID"

            })
        else:
            context.update({
            "reset":"DISABLED",
            "HEADER":"Sorry!",
            "MSG": f"Enrollment ID <b style='color:black;'>{username}</b> is not found in our records."
            })

    return render(request, PAGE_MAPPER.pageDict[pageDictKey], context)
