from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
from django.http import JsonResponse,HttpResponse
from MCQ.models import QuizData, UserRegistration, Question, FeedbackForm
from .models import Declare_Result, Department_Information
from django.db.models import F, Count, Sum
from django.contrib.auth.models import User

# all static packages import below
import csv
import os
import pandas as pd
from . import ADMIN_PAGE_MAPPER, staticVariables
from sqlalchemy import create_engine
import datetime
from ADMINPANEL.sendMail import send_mails, forgot_password_mail, registration_successfull_mail
from ADMINPANEL.forms import Information
from MCQ.password_gen import generate_random_password
from itertools import chain
# Create your views here.
global dataBaseMapper

dataBaseMapper={
 1:'MCQ_allowedenrollments',# total number of students
 2:'MCQ_enrollemntsforquiz', # students that will appear for test
 3:'MCQ_question',
 4:"ADMINPANEL_Department_Information",
 }

def get_result_status():

    try:
        resultStat = int(list(Declare_Result.objects.values_list("RESULT_STATUS", flat=True))[0])
        return resultStat
    except:

        return 0




def update_result_status(request, status):
    if status == 1:
        send_mails()
    try:
        resultStat = Declare_Result.objects.get(id=1)
        resultStat.RESULT_STATUS= int(status)
        resultStat.save()
    except:

        resultStat = Declare_Result.objects.all()
        resultStat.RESULT_STATUS= 0
        resultStat.save()

def check_missing_cat(querySet):
    print(querySet.to_dataframe())
    querySet = querySet.to_dataframe()["CATEGORY"].tolist()
    missingCat = []
    for cat in ['APPTITUDE', 'GENERAL_KNOWLEDGE', 'LOGICAL', 'WRITTEN_COMMUNICATION']:

        if cat not in querySet:
            missingCat.append(cat)

    return missingCat

def convert_to_str(x):

    return str(int(x))

def convert_to_dateTime(x):

    return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")

""" HOMEPAGE FOR ADMIN PANEL"""
def admin_home(request):

    pageDictKey = 'adminHome'

    context = {"resultStat":get_result_status(), "pageDictKey":pageDictKey,}
    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey],context)

def rearrange_list(arrayList, deleteItm):

    resultedList = []

    if type(deleteItm) != list():

        deleteItm = [deleteItm]

    for item in arrayList:

        if item not in deleteItm:

            resultedList.append(item)

    return resultedList

@login_required
def upload_files(request):

    pageDictKey = 'uploadFiles'
    context = {"resultStat":get_result_status(), "pageDictKey":pageDictKey,}
    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey],context)

@login_required
def upload_data(request, dataBaseKey):

    pageDictKey = 'uploadPage'

    convertLower = lambda x: x.lower()

    context={"MSG":"NOT_UPLOADED", "resultStat":get_result_status(), "pageDictKey":pageDictKey,}

    if request.method == "POST":

        tableName = dataBaseMapper[dataBaseKey]
        uploadedFile = request.FILES['document']
        #
        FILE = FileSystemStorage()
        FILE.save(uploadedFile.name, uploadedFile)

        mediaPath = settings.MEDIA_ROOT#os.path.abspath("./media")

        if ".xlsx" in uploadedFile.name or ".xls" in uploadedFile.name:

            uploadedData = pd.read_excel(mediaPath+"/"+str(uploadedFile.name))

        elif ".csv" in uploadedFile.name:

            uploadedData = pd.read_csv(mediaPath+"/"+str(uploadedFile.name))

        # CHKMSG = uploadCheck.check_data(request, uploadedData)
        os.remove(mediaPath+"/"+uploadedFile.name)

        # uploading data to database
        dbPath = os.path.abspath("../ROOTdb.sqlite3")

        conn = create_engine(f'sqlite:////{dbPath}')


        if dataBaseKey == 2:
            lowercase = lambda x: x.strip().lower()
            uploadedData['ENROLLMENT_NUMBER'] = uploadedData['ENROLLMENT_NUMBER'].apply(lowercase)
            uploadedData['YEAR'] = uploadedData['YEAR'].apply(convert_to_str)
            uploadedData['MONTH'] = uploadedData['MONTH'].apply(convert_to_str)
            uploadedData['DATE'] = uploadedData['DATE'].apply(convert_to_str)
            uploadedData['START_TIME'] = uploadedData['START_TIME'].apply(str)
            uploadedData['END_TIME'] = uploadedData['END_TIME'].apply(str)
            uploadedData['START_TIME'] = uploadedData['YEAR']+"-"+uploadedData['MONTH']+"-"+uploadedData['DATE']+" "+uploadedData['START_TIME']
            uploadedData['END_TIME'] = uploadedData['YEAR']+"-"+uploadedData['MONTH']+"-"+uploadedData['DATE']+" "+uploadedData['END_TIME']
            uploadedData['START_TIME'] = uploadedData['START_TIME'].apply(convert_to_dateTime)
            uploadedData['END_TIME'] = uploadedData['END_TIME'].apply(convert_to_dateTime)
            uploadedData.drop(['YEAR', 'MONTH', 'DATE'],axis=1, inplace=True)

            try:
                # deleting previous allowed students
                pd.read_sql_query(f"DELETE FROM {tableName}", conn)

            except:

                pass


        try:

            if dataBaseKey == 4:
                dataBasId = list(Department_Information.objects.all().values_list("EMAIL_ID", flat=True))
                uploadedData["EMAIL_ID"] = uploadedData["EMAIL_ID"].apply(convertLower)
                emailList = uploadedData["EMAIL_ID"].unique().tolist()
                uploadList = []
                for id in emailList:

                    if id not in dataBasId:
                    # registering user
                        uploadList.append(id)
                        qsData = uploadedData.query(f"EMAIL_ID == '{id}'")
                        qsData.reset_index(drop=True, inplace=True)
                        facultyEmail = qsData['EMAIL_ID'][0]
                        try:
                            facultyFirstName = qsData['NAME'][0].split(" ")[-1]
                        except:
                            facultyFirstName = " "
                        try:
                            facultyLastName = qsData['NAME'][0].split(" ")[-1]
                        except:
                            facultyLastName = " "

                        user = User.objects.create_user(
                                                        username=facultyEmail,
                                                        password='tascPortal@21022021',
                                                        email=facultyEmail,
                                                        first_name=facultyFirstName,
                                                        last_name=facultyLastName,
                                                        )
                        user.is_staff = True
                        user.save()
                        try:
                            registration_successfull_mail(qsData['NAME'][0], qsData['EMAIL_ID'][0])
                        except Exception as e:
                            print(e)


                uploadedData = uploadedData.query(f"EMAIL_ID == {uploadList}")
                uploadedData.to_sql(tableName, conn, if_exists='append', index=False)
            else:

                uploadedData.to_sql(tableName, conn, if_exists='append', index=False)
            # os.remove(mediaPath+"/"+str(uploadedFile))

        except Exception as e:

            print(e)
            # os.remove(mediaPath+"/"+str(uploadedFile))


        # context.update({"MSG":"UPLOADED","uploadedData":uploadedData})


    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context=context)

@login_required
def download_university_template(request):

    fileName = f"STUDENT DATA"


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachement; filename= "{fileName}.xlsx"'
    writer = csv.writer(response)

    writer.writerow(
        [
         "SR.NO.",
         "NAME AS PER HSC MARKSHEET",
         "BRANCH",
         "Semester",
         "ROLL NUMBER",
         "GENDER",
         "GSFCU EMAIL ID ADDRESS",
        ])

    return response


@login_required
def update_university_data(request):

    pageDictKey = 'uploadPage'

    context={"MSG":"NOT_UPLOADED", "resultStat":get_result_status(), "pageDictKey":pageDictKey,}

    if request.method == "POST":

        mediaPath = "./media"
        for fname in os.listdir(mediaPath):
            os.remove(mediaPath+"/"+fname)
        uploadedFile = request.FILES['document']

        FILE = FileSystemStorage(mediaPath)
        FILE.save(uploadedFile.name, uploadedFile)

    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context=context)


@login_required
def download_data(request):

    # pageDictKey = "downloadPage"

    fileName = f"QUIZ_DATA-{now()}"


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachement; filename= "{fileName}.csv"'
    writer = csv.writer(response)

    writer.writerow(
        [
         "QUESTION ID",
         "ACTUAL QUESTION",
         "ENROLLMENT NUMBER",
         "SCHOOL",
         "PROGRAM",
         "CATEGORY",
         "ANSWER",
         "CORRECT ANSWER",
         "TIME",

         # "END_TIME",
        ])

    users = QuizData.objects.all().order_by('ENROLLMENT_NUMBER').values_list(
                                        'QUESTION_ID',
                                        'ACTUAL_QUESTION',
                                        'ENROLLMENT_NUMBER',
                                        "SCHOOL",
                                        "PROGRAM",
                                        'CATEGORY',
                                        'ANSWER',
                                        'CORRECT_ANSWER',
                                        "START_TIME",
                                        )

    for user in users:
        writer.writerow(user)

    return response


@login_required
def download_feedback(request):

    # pageDictKey = "downloadPage"

    fileName = f"FEEDBACK_DATA-{now()}"


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachement; filename= "{fileName}.csv"'
    writer = csv.writer(response)

    file = FeedbackForm.objects.all().to_dataframe()

    one  = file[["QSTN_ONE",
      "QSTN_ONE_ANSWR",
      "QSTN_TWO"]].groupby(["QSTN_ONE",
                             "QSTN_ONE_ANSWR"], as_index=False).count().rename(columns={"QSTN_TWO":"COUNT",
                                                                       "QSTN_ONE":"QUESTION",
                                                                       "QSTN_ONE_ANSWR":"ANSWER"})

    two = file[["QSTN_TWO",
      "QSTN_TWO_ANSWR",
      "QSTN_THREE"]].groupby(["QSTN_TWO",
                             "QSTN_TWO_ANSWR"], as_index=False).count().rename(columns={"QSTN_THREE":"COUNT",
                                                                                       "QSTN_TWO":"QUESTION",
                                                                                       "QSTN_TWO_ANSWR":"ANSWER"})

    q_three_data = pd.DataFrame()
    choiceQ = file.dropna()
    for i in ["QSTN_THREE_ANSWR_CHOICE_1","QSTN_THREE_ANSWR_CHOICE_2","QSTN_THREE_ANSWR_CHOICE_3","QSTN_THREE_ANSWR_CHOICE_4",]:

        tempFile = file.dropna()[["QSTN_THREE",
                          f"{i}",
                          "QSTN_TWO",]].groupby(["QSTN_THREE",
                                                 f"{i}"], as_index=False).count().rename(columns={"QSTN_TWO":"COUNT",
                                                                                  "QSTN_THREE":"QUESTION",
                                                                                 f"{i}":"ANSWER"})

        q_three_data = pd.concat([q_three_data, tempFile])


    three = q_three_data.groupby(["QUESTION", "ANSWER"], as_index=False).sum()
    # print(q_three_data)
    # print(three)
    final = pd.concat([one, two, three]).reset_index(drop=True)
    final.replace("","NT", inplace=True)
    final = final.query("ANSWER != 'NT'").reset_index(drop=True)
    final.to_csv(path_or_buf=response,sep=';',float_format='%.2f',index=False,decimal=",")
    # for user in one:
    #     writer.writerow([(one["QUESTION"]),(one["ANSWER"])])


    return response

@login_required
def template_download(request, setNO):

    fileName_dict = {
    1:"UPLOAD_STUDENTS_DATA_SET_A",
    2:"UPLOAD_ENROLLMENTS_FOR_TEST_SET_B",
    3:"UPLOAD_QUESTIONS_SET_C",
    4:"UPLOAD_DEPARTMENT_DETAILS"
    }



    fileName = fileName_dict[int(setNO)]


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachement; filename= "{fileName}.csv"'
    writer = csv.writer(response)

    if int(setNO) == 1:
        writer.writerow(
            [
             "ENROLLMENT_NUMBER",
            ])

    elif int(setNO) == 2:
        writer.writerow(
            [
             "ENROLLMENT_NUMBER",
             "YEAR",
             "MONTH",
             "DATE",
             "START_TIME",
             "END_TIME",
            ])

    elif int(setNO) == 3:

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachement; filename= "{fileName}.csv"'
        writer = csv.writer(response)

        writer.writerow(
            [
             "QUESTION_ID",
             "CATEGORY",
             "QUESTION",
             "CORRECT",
             "CHOICE_1",
             "CHOICE_2",
             "CHOICE_3",
             "CHOICE_4",
            ])

        users = Question.objects.all().values_list(
                                            "QUESTION_ID",
                                            "CATEGORY",
                                            "QUESTION",
                                            "CORRECT",
                                            "CHOICE_1",
                                            "CHOICE_2",
                                            "CHOICE_3",
                                            "CHOICE_4",
                                            )

        for user in users:
            writer.writerow(user)

    elif int(setNO) == 4:

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachement; filename= "{fileName}.csv"'
        writer = csv.writer(response)

        writer.writerow(
            [
             "NAME",
             "SCHOOL_NAME",
             "PROGRAM_NAME",
             "EMAIL_ID",
            ])

    return response

def percentage_range(prg, sem, gender):

    catList = ['APPTITUDE',"GENERAL KNOWLEDGE", "LOGICAL", "WRITTEN COMMUNICATION"]

    actualData = QuizData.objects.filter(PROGRAM__in=prg,
                                         SEMESTER__in=sem,
                                         GENDER__in=gender,
                                         )

    school_wise_per_series = []

    for pr in prg:
        maxMarks_overall = round(100/(20*len(actualData.filter(PROGRAM__in=[pr],).values_list("ENROLLMENT_NUMBER").distinct())),1)
        # subject_max = 100/(maxMarks_overall//4)
        # print(subject_max)

        correctAnswers_data = actualData.filter(PROGRAM__in=[pr] , ANSWER__iexact = F('CORRECT_ANSWER')).order_by('CATEGORY', 'ANSWER')
        marks_obtained = correctAnswers_data.values('PROGRAM',"CATEGORY").annotate(PERCENTAGE=(Count('ENROLLMENT_NUMBER')*2)*maxMarks_overall).order_by('PROGRAM',"CATEGORY").to_dataframe()

        school_wise_per_series.append(
        {'name':pr.replace("_", " ").upper(),
        'data': marks_obtained['PERCENTAGE'].tolist()}
        )

    return catList, school_wise_per_series

def count_correct(filteredData):

    filteredData = filteredData.values("ENROLLMENT_NUMBER","SCHOOL",
                                        "PROGRAM",'CATEGORY', 'ANSWER').filter(ANSWER__iexact = F('CORRECT_ANSWER')).order_by("ENROLLMENT_NUMBER","SCHOOL",
                                                                                                                    "PROGRAM",'CATEGORY', 'ANSWER','CATEGORY', 'ANSWER')

    filteredData = filteredData.values("ENROLLMENT_NUMBER","SCHOOL","PROGRAM").annotate(MARKS = Count("ENROLLMENT_NUMBER")*2).order_by("ENROLLMENT_NUMBER","SCHOOL",
                                                                                "PROGRAM")

    return filteredData

def overall_percentage(catgry, program, semester, gender, lowerLim, upperLim):
    maxMarks = 80
    timesNumerator = (100/maxMarks)*2
    filteredData = QuizData.objects.filter(
                                        # CATEGORY__in=catgry,
                                        PROGRAM__in=program,
                                        SEMESTER__in=semester,
                                        GENDER__in=gender,
                                        ).values("ENROLLMENT_NUMBER","SCHOOL",
                                        "PROGRAM",'CATEGORY', 'ANSWER').filter(ANSWER__iexact = F('CORRECT_ANSWER')).order_by("ENROLLMENT_NUMBER","SCHOOL",
                                                                                                                    "PROGRAM",'CATEGORY', 'ANSWER','CATEGORY', 'ANSWER')

    calcultedPER = filteredData.values("ENROLLMENT_NUMBER").annotate(PERCENTAGE = Count("ENROLLMENT_NUMBER")*timesNumerator).order_by("ENROLLMENT_NUMBER")

    resultedData = calcultedPER.filter(PERCENTAGE__gt=int(lowerLim), PERCENTAGE__lte=int(upperLim))

    return list(resultedData.values_list("ENROLLMENT_NUMBER", flat=True))


@login_required
def dashboard(request):

    pageDictKey = 'dashboard'

    context={
    "program":[],
    "semester":[],
    "gender":[],
    "DASH": "DISABLED",
    "CATGRY": staticVariables.CATEGORY_LIST, # CATEGORY list
    "SCHOL": staticVariables.SCHOL_LIST, # school list
    "PRGM": staticVariables.PROGRM_LIST, # program list
    "GNDR": staticVariables.GENDR_LIST,
    "resultStat":get_result_status(),
    "pageDictKey":pageDictKey,
    }


    if request.method == 'POST':

        catgry = request.POST.getlist("cat_POST")
        program = request.POST.getlist("program_POST")
        semester = request.POST.getlist("semester_POST")
        gender = request.POST.getlist("gender_POST")
        percentageRange = request.POST.get("perRange").strip()

        quizData = QuizData.objects.values("ENROLLMENT_NUMBER").annotate(COUNT = Count("QUESTION_ID")).order_by("ENROLLMENT_NUMBER")
        TOTAL_ATTEMPT = UserRegistration.objects.all().count()
        students_with_all_fourthy = round((quizData.filter(COUNT__gte=40).count()/TOTAL_ATTEMPT)*100) # percentage of students with all 40 questions

        all_fourty_list = list(quizData.filter(COUNT__gte=40).values_list("ENROLLMENT_NUMBER", flat=True))
        # UserRegistration.objects.filter()

        # query 1: % of students completing the test with attempting all 40 question and 2. Remaining students
        # School wise
        actualdata = QuizData.objects.filter(
                                            # CATEGORY__in=catgry,
                                            PROGRAM__in=program,
                                            SEMESTER__in=semester,
                                            GENDER__in=gender,
                                            ).values("PROGRAM", "GENDER","ENROLLMENT_NUMBER",).annotate(COUNT=Count("ENROLLMENT_NUMBER")).order_by("PROGRAM", "GENDER","ENROLLMENT_NUMBER",)

        # print(actualdata.to_dataframe())
        schoolWiseFourty = actualdata.filter(COUNT__gte=40).count()

        totalStrength_PRG = UserRegistration.objects.filter(
                                            PROGRAM__in=program,
                                            SEMESTER__in=semester,
                                            GENDER__in=gender,
                                            ).count()



        completionPrcnt = round((schoolWiseFourty/totalStrength_PRG)*100)

        #  list of students with all questions attempted
        allQuestionAtmptd_school = list(actualdata.filter(COUNT__gte=40).values_list("ENROLLMENT_NUMBER", flat=True))
        query1_answer_one = UserRegistration.objects.filter(
                                            ENROLLMENT_NUMBER__in=allQuestionAtmptd_school,
                                            )
        query1_answer_two = UserRegistration.objects.filter(PROGRAM__in=program, SEMESTER__in=semester,GENDER__in=gender,).exclude(
                                            ENROLLMENT_NUMBER__in=allQuestionAtmptd_school,
                                            )
        schoolLists_fetched = list(query1_answer_one.values_list("SCHOOL", flat=True).distinct())

        # calculating total number of students who gave exams
        # 1. for students who attempted all 40 questions
        students_who_gave_test_LIST = list(QuizData.objects.filter(PROGRAM__in=program).values_list("ENROLLMENT_NUMBER", flat=True))

        student_not_completed_test = list(UserRegistration.objects.filter(PROGRAM__in=program).exclude(ENROLLMENT_NUMBER__in=students_who_gave_test_LIST,).values_list("ENROLLMENT_NUMBER", flat=True))

        # overall percentage as per program selection
        moduleList,  school_wise_per_series = percentage_range(program, semester, gender)



        # Overall result of registered students and with option to select (100-90, 90-80, 80-70, 70-60, 60-50)
        if len(percentageRange) < 1:

            pass

        else:

            lowerLim = percentageRange.split(',')[0]
            upperLim = percentageRange.split(",")[1]

            enrollmentFound  = overall_percentage(catgry, program, semester, gender, lowerLim, upperLim)

            fecthRecords = QuizData.objects.filter(
                                                # CATEGORY__in=catgry,
                                                PROGRAM__in=program,
                                                ENROLLMENT_NUMBER__in = enrollmentFound,
                                                SEMESTER__in=semester,
                                                GENDER__in=gender,
                                                )

            finalResult = count_correct(fecthRecords)

            if len(finalResult) > 0:
                context.update({
                "lowerLim":lowerLim,
                "upperLim":upperLim,
                "showMe":'Enabled',
                "percentageRangetable":finalResult.order_by("-MARKS","ENROLLMENT_NUMBER"),
                })

        context.update({
            # "catgry":catgry,
            "program":program,
            "semester":semester,
            "gender":[_.upper() for _ in gender],

            "DASH": "ENABLED",
            "students_with_all_fourth":students_with_all_fourthy,
            "TOTAL_ATTEMPT":TOTAL_ATTEMPT,
            # query1
            "schoolNames": ", ".join(schoolLists_fetched),
            "completionPrcnt":completionPrcnt,
            "query1_answer_one":query1_answer_one,
            "query1_answer_two":query1_answer_two,
            "student_not_completed_test":student_not_completed_test,

            "completionPrcnt":completionPrcnt,

            "moduleList":moduleList,
            "school_wise_per_series":school_wise_per_series,

            })

    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)

def get_report(enrollmentNo):

    studntRep = QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=enrollmentNo,)
    totalAttempt = studntRep.values('CATEGORY').annotate(TOTAL_ATTEMPT = Count('CORRECT_ANSWER')).order_by('CATEGORY')
    studntRep = studntRep.values('CATEGORY', 'ANSWER').filter(ANSWER__iexact = F('CORRECT_ANSWER')).order_by('CATEGORY', 'ANSWER')
    studntRep = studntRep.values('CATEGORY').annotate(COUNT = Count('CATEGORY')).order_by('CATEGORY')
    total = 10#100/sum(studntRep.to_dataframe()['COUNT'])
    studntRep = studntRep.annotate(PER=F('COUNT')*total).order_by('CATEGORY')

    return studntRep

def time_chart(eachIDTime):

    catID = eachIDTime['QUESTION_ID'].tolist()
    series=[{
    "name":'TIME',
    'data': eachIDTime['SECONDS'].tolist(),
    }]

    colorType = []

    for chk, crt in zip(eachIDTime['ANSWER'], eachIDTime['CORRECT_ANSWER']):

        colorVal = "#15d629"
        if chk != crt:
            colorVal = "#ff3030"

        colorType.append(colorVal)

    return catID, series, colorType


def capture_time(enrollmentNo):

    studntRep = QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=enrollmentNo,).to_dataframe()

    studntRep['START_TIME'] = studntRep['START_TIME'].apply(pd.to_datetime)
    # total time(sesonds) taken each question
    totalTime = studntRep['START_TIME'].max()- studntRep['START_TIME'].min()
    eachIDTime = studntRep.copy()

    minute = int(str(eachIDTime['START_TIME'].max() - eachIDTime['START_TIME'].min()).split(" ")[-1].split(".")[0].split(":")[1])
    second = int(str(eachIDTime['START_TIME'].max() - eachIDTime['START_TIME'].min()).split(" ")[-1].split(".")[0].split(":")[-1])
    totalSeconds = (minute*60)+second
    eachIDTime['SECONDS'] = eachIDTime[['ENROLLMENT_NUMBER',
                                    'START_TIME']].groupby(['ENROLLMENT_NUMBER']).START_TIME.diff().shift(-1).dt.seconds

    eachIDTime.fillna(totalSeconds-eachIDTime['SECONDS'].sum(), inplace=True)

    # total time taken wach category
    studntRep['SECONDS'] = studntRep[['ENROLLMENT_NUMBER', 'CATEGORY',
                    'START_TIME']].groupby(['ENROLLMENT_NUMBER',
                                'CATEGORY']).START_TIME.diff().shift(-1).dt.seconds.fillna(0)

    studntRep = studntRep[['ENROLLMENT_NUMBER', 'CATEGORY',
                    'SECONDS']].groupby(['ENROLLMENT_NUMBER',
                                    'CATEGORY'], as_index=False).sum()

    studntRep['MINUTES'] = round(studntRep['SECONDS']/60,1)

    return studntRep, totalTime, eachIDTime

def highchart(feature):

    feature = feature.to_dataframe()

    resultedList = []
    # pie chart
    for cat, val in zip(feature['CATEGORY'], feature['PER']):

        resultedList.append({
                            'name': cat.replace("_", " "),
                            'y': val
                        })

    # column chart
    crtList, incrtList = [], []

    for cat in feature['COUNT']:

        crtList.append(cat)
        incrtList.append(10-cat)


    columnSeries = [{
                        'name': 'Correct',
                        'data': crtList

                    }, {
                        'name': 'Incorrect',
                        'data': incrtList
                    }]

    categoryList = [_.replace("_", " ") for _ in feature['CATEGORY'].unique().tolist()]

    return resultedList, columnSeries, categoryList

@login_required
def student_report(request, enroll):
    pageDictKey = 'student'

    chkEnrolls = [request.user.username]
    # list(UserRegistration.objects.all().values_list("ENROLLMENT_NUMBER", flat=True))+['admin']
    # try:
    #     chkEnrolls.remove(enroll)
    # except:
    #     pass

    if enroll == "0" or len(enroll) < 1 :
        enroll = request.user.username

    else:

        if enroll not in chkEnrolls and request.user.is_superuser == False:

            enroll = request.user.username
        else:
            enroll = enroll

    studentData = UserRegistration.objects.filter(ENROLLMENT_NUMBER__iexact=enroll).values()

    context = {
    'WARNING_MSG': 'DISABLE',
    'studentData':studentData,
    "resultStat":get_result_status(),
    "pageDictKey":pageDictKey,

    }

    if request.user.is_superuser and enroll == request.user.username:
        pass
    else:
        try:
            studntRep = get_report(enroll)
            piechartSeries, columnSeries, categoryList = highchart(studntRep)
            TOTAL_CRT = sum(studntRep.to_dataframe()['COUNT'])

            timeTakenSeries, totalTime, eachIDTime = capture_time(enroll)

            catQstnID, qstnDtaSeries, colorType = time_chart(eachIDTime)

            timeTakenSeries = timeTakenSeries['MINUTES'].tolist()
            totalTimetaken = datetime.datetime.strptime(str(totalTime).split(" ")[-1], '%H:%M:%S.%f')
            timeTakenSeries = [{
            'name': "CATEGORY",
            'data': timeTakenSeries,
            'colorByPoint':'true',
            }]

            # question
            questionTable = QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=enroll)#.order_by("CATEGORY")

            # get actual attempts
            try:
                qsData = QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=enroll,)
                acualAttempts = qsData.values('CATEGORY').annotate(TOTAL_ATTEMPT = Count('CORRECT_ANSWER')).order_by('CATEGORY').to_dataframe()
                totalActAttempts = sum(acualAttempts['TOTAL_ATTEMPT'])

                context.update({            "acualAttempts":acualAttempts,
                            "totalActAttempts":totalActAttempts,})
            except:
                pass

            context.update({
            'studentData':studentData,
            'studntRep':studntRep,
            'TOTAL_CRT':TOTAL_CRT,

            'categoryList':categoryList,
            'piechartSeries':piechartSeries,
            'columnSeries': columnSeries,
            "enrollmntNO": enroll,

            "timeTakenSeries":timeTakenSeries,
            "totalTimetaken": totalTimetaken,

            "questionTable":questionTable,
            "catQstnID":catQstnID,
            "qstnDtaSeries":qstnDtaSeries,
            "colorType":colorType,

            })
        except:
            context.update({
            'WARNING_MSG': 'ENABLE',
            "MSG":f"Looks like <u style='color:red;'>{enroll}</u>" +" has not given the test till now <br><br> PLEASE CHECK BACK AGAIN!",
            })

    if request.method == 'POST':


        enrollmentid = request.POST.get("enrollmentid")

        studentData = UserRegistration.objects.filter(ENROLLMENT_NUMBER__iexact=enrollmentid).values()

        if len(enrollmentid) == 0:

            context.update({
            'WARNING_MSG': 'ENABLE',
            "MSG":"Search Result Cannot be Blank",
            })

            return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)

        elif len(studentData) == 0:

            context.update({
            'WARNING_MSG': 'ENABLE',
            "MSG":f"<u style='color:red;'>{enrollmentid}</u>" +" Cannot be found in our records",
            })

            return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)

        # get actual attempts
        try:
            qsData = QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=enrollmentid,)
            acualAttempts = qsData.values('CATEGORY').annotate(TOTAL_ATTEMPT = Count('CORRECT_ANSWER')).order_by('CATEGORY').to_dataframe()
            totalActAttempts = sum(acualAttempts['TOTAL_ATTEMPT'])
            # print(acualAttempts)

            context.update({            "acualAttempts":acualAttempts,
                        "totalActAttempts":totalActAttempts,})
        except:
            pass

        try:
            studntRep = get_report(enrollmentid)
            missingCat = check_missing_cat(studntRep)
            missinglenght = len(missingCat)
            piechartSeries, columnSeries, categoryList = highchart(studntRep)
            TOTAL_CRT = sum(studntRep.to_dataframe()['COUNT'])

            timeTakenSeries, totalTime, eachIDTime = capture_time(enrollmentid)

            catQstnID, qstnDtaSeries, colorType = time_chart(eachIDTime)

            timeTakenSeries = timeTakenSeries['MINUTES'].tolist()
            totalTimetaken = datetime.datetime.strptime(str(totalTime).split(" ")[-1], '%H:%M:%S.%f')
            timeTakenSeries = [{
            'name': "CATEGORY",
            'data': timeTakenSeries,
            'colorByPoint':'true',
            }]

            # question
            questionTable = QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=enrollmentid)#.order_by("CATEGORY")

            context.update({
            'studentData':studentData,
            'studntRep':studntRep,
            "missingCat":missingCat,
            "missinglenght": missinglenght,
            'TOTAL_CRT':TOTAL_CRT,
            "enrollmntNO": enrollmentid,

            'categoryList':categoryList,
            'piechartSeries':piechartSeries,
            'columnSeries': columnSeries,

            "timeTakenSeries":timeTakenSeries,
            "totalTimetaken": totalTimetaken,

            "questionTable":questionTable,
            "catQstnID":catQstnID,
            "qstnDtaSeries":qstnDtaSeries,
            "colorType":colorType,
            })
        except Exception as e:
            print(e)
            context.update({
            'WARNING_MSG': 'ENABLE',
            "MSG":f"Looks like <u style='color:red;'>{enrollmentid}</u>" +" has not given the test till now <br><br> PLEASE CHECK BACK AGAIN!",
            })
    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)


@login_required
def records(request):

    pageDictKey = 'records'

    registeredUsers = UserRegistration.objects.all().order_by("SCHOOL","PROGRAM", "SEMESTER", "ENROLLMENT_NUMBER")
    schoolHeader = list(set(registeredUsers.values_list("SCHOOL", flat=True)))
    semesterHeader = list(set(registeredUsers.values_list("SEMESTER", flat=True)))

    context={
    "SCHOL": staticVariables.SCHOL_LIST, # school list
    "registeredUsers":registeredUsers,
    "GNDR": staticVariables.GENDR_LIST, # program list
    "schoolHeader":', '.join(schoolHeader),
    "semesterHeader":', '.join([str(_) for _ in semesterHeader]),
    "totalStrength":registeredUsers.count(),
    "resultStat":get_result_status(),
    "pageDictKey":pageDictKey,
    }

    if request.method == 'POST':

        # catgry = request.POST.getlist("cat_POST")
        schol = request.POST.getlist("school_POST")
        semstr = request.POST.getlist("semester_POST")
        gender = request.POST.getlist("gender_POST")

        registeredUsers = UserRegistration.objects.filter(SCHOOL__in=schol,
                                                        SEMESTER__in=semstr,
                                                        GENDER__in=gender,
                                                        )
                                                        # .order_by("SCHOOL","PROGRAM", "SEMESTER", "ENROLLMENT_NUMBER")
        schoolHeader = list(set(registeredUsers.values_list("SCHOOL", flat=True)))
        semesterHeader = list(set(registeredUsers.values_list("SEMESTER", flat=True)))
        context.update({
        "scholList": schol, # school list
        'semstrList':semstr,
        "genderLIst": gender,
        "registeredUsers":registeredUsers,
        "schoolHeader":schoolHeader,
        "semesterHeader":semesterHeader,
        "schoolHeader":', '.join(schoolHeader),
        "semesterHeader":', '.join([str(_) for _ in semesterHeader]),
        "totalStrength":registeredUsers.count()
        })


    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)


def toggle_result(request, status, pageDictKey):

    pageDictKey = "result_message"
    message = "Students do not have access to their result section."
    context={
    "pageDictKey":pageDictKey,
    "status":status,
    "resultStat":get_result_status(),
    "message":message,
    }

    if int(status) != get_result_status():

        update_result_status(request, status)
        if int(status) == 1:
            message = "Result Announced! Students have been notified via mail on their GSFC Email-ID."
        else:
            message = "Students do not have access to their result section."
        context.update({"resultStat":get_result_status(),"message":message,})

    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)


@login_required()
def get_dept_information(request):

    pageDictKey = 'department'

    department_info = Department_Information.objects.all().order_by('-id')

    form = Information()

    context = {
    'department_table': department_info,
    "pageDictKey":pageDictKey,
    'form':form,
    "resultStat":get_result_status(),
    "school_list": staticVariables.SCHOL_LIST,
    "program_list": staticVariables.PROGRM_LIST,
    }

    if request.method == 'POST':
        departmentEmailList = list(Department_Information.objects.all().values_list('EMAIL_ID', flat=True))
        try:
            facultyFirstName = request.POST.get("NAME").split(" ")[:-1][0].title()
        except:
            facultyFirstName = request.POST.get("NAME").title()
        try:
            facultyLastName = request.POST.get("NAME").split(" ")[-1].title()
        except:
            facultyLastName = " "
        facultySchool = request.POST.get("SCHOOL_NAME")
        facultyProgram = request.POST.get("PROGRAM_NAME")
        facultyEmail = request.POST.get("EMAIL_ID").lower()

        form = Information(request.POST)

        if facultyEmail not in departmentEmailList:
            if form.is_valid():

                # saving form
                save_it = form.save(commit=False)
                save_it.save()

                # registering user
                user = User.objects.create_user(
                                                username=facultyEmail,
                                                password='tascPortal@21022021',
                                                email=facultyEmail,
                                                first_name=facultyFirstName,
                                                last_name=facultyLastName,
                                                )
                user.is_staff = True
                user.save() #saving the user to database
                try:
                    registration_successfull_mail(request.POST.get("NAME"), facultyEmail)
                    context.update({
                    'error': 'YES',
                    "msg":f"{request.POST.get('NAME')} with email-ID <u style='color:black;'>{facultyEmail}</u> added to our records and mail has been sent with his/her dashboard credentials. "
                    })
                except Exception as e:
                    print(e)
        else:
            context.update({
            'error': 'YES',
            "msg":f"{request.POST.get('NAME')} with email-ID <u style='color:black;'>{facultyEmail}</u> is already registered into our portal"
            })
    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)

def feedback_page(request):

    pageDictKey = 'comments'

    commentsData = FeedbackForm.objects.all()

    context = {"comments":commentsData,"pageDictKey":pageDictKey,
    "resultStat":get_result_status(),}

    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)

def reset_faculty_pass(request):

    pageDictKey = 'reset_faculty_pass'

    context = {"reset":"ENABLED"}

    if request.method == "POST":

        facultyID = request.POST.get("facultyID").lower()

        allIDs = list(Department_Information.objects.all().values_list("EMAIL_ID", flat=True))


        if facultyID in facultyID:
            try:
                facultyName = list(Department_Information.objects.filter(EMAIL_ID__iexact=facultyID).values_list("NAME", flat=True))[0]
                user = User.objects.get(username__iexact=facultyID)
            except:

                context.update({
                "reset":"DISABLED",
                "HEADER":"Sorry!",
                "MSG": f"<b style='color:black;'>{facultyID}</b> is not found in our records."
                })

                return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)


            newPassword = generate_random_password()
            forgot_password_mail(facultyName.title(), facultyID, newPassword, sendTo=facultyID)

            user.set_password(newPassword)
            user.save()

            context.update({
            "reset":"DISABLED",
            "HEADER":"Password Reset",
            "MSG": f"Your new password has been mailed to your <span style='color:black;'>{facultyID}</span> Email-ID"

            })
        else:
            context.update({
            "reset":"DISABLED",
            "HEADER":"Sorry!",
            "MSG": f"Email ID <b style='color:black;'>{facultyID}</b> is not found in our records."
            })

    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)

@login_required()
def my_detail(request):

    pageDictKey = 'whoami'

    facultyData = Department_Information.objects.filter(EMAIL_ID__iexact=request.user.username)
    context={
    "resultStat":get_result_status(),
    "pageDictKey":pageDictKey,
    "facultyData":facultyData,
    "matchColor": 'black',
    "Color": 'black',
    "ERROR": "disabled",
    }

    if request.method == "POST":

        currentPass = request.POST.get("currentPass")
        newPass = request.POST.get("newPass")
        confirmPass = request.POST.get("confirmPass")

        if check_password(currentPass, request.user.password):

            if confirmPass != newPass:

                context.update({
                "ERROR": "enabled",
                "MSG": "Password did not Matched",
                "matchColor": 'red',
                "para": 'red',
                })

            else:

                user = User.objects.get(username__iexact=request.user.username)
                user.set_password(confirmPass)
                user.save()

                context.update({
                "ERROR": "enabled",
                "MSG": "Password Changes Successfully",
                "matchColor": 'green',
                "para": 'green',
                })

        else:
            context.update({
            "ERROR": "enabled",
            "MSG": "Incorrect Current Password",
            "Color": 'red',
            "para": 'red',
            })

    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)
