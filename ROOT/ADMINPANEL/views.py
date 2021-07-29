from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
from django.http import JsonResponse,HttpResponse
from MCQ.models import QuizData, UserRegistration, Question
from .models import Declare_Result
from django.db.models import F, Count, Sum

# all static packages import below
import csv
import os
import pandas as pd
from . import ADMIN_PAGE_MAPPER, staticVariables
from sqlalchemy import create_engine
import datetime
# Create your views here.
global dataBaseMapper

dataBaseMapper={
 1:'MCQ_allowedenrollments',# total number of students
 2:'MCQ_enrollemntsforquiz', # students that will appear for test
 3:'MCQ_question',
 }

def get_result_status():

    try:
        resultStat = int(list(Declare_Result.objects.values_list("RESULT_STATUS", flat=True))[0])
    except:

        return 0

    return resultStat

def update_result_status(request, status):

    try:
        resultStat = Declare_Result.objects.get(id=1)
        resultStat.RESULT_STATUS= int(status)
        resultStat.save()
    except:

        resultStat = Declare_Result.objects.all()
        resultStat.RESULT_STATUS= 0
        resultStat.save()


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



    context={"MSG":"NOT_UPLOADED", "resultStat":get_result_status(), "pageDictKey":pageDictKey,}

    if request.method == "POST":

        tableName = dataBaseMapper[dataBaseKey]
        uploadedFile = request.FILES['document']
        #
        FILE = FileSystemStorage()
        FILE.save(uploadedFile.name, uploadedFile)

        mediaPath = os.path.abspath("./media")

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

            uploadedData.to_sql(tableName, conn, if_exists='append', index=False)
            os.remove(mediaPath+"/"+str(uploadedFile))

        except Exception as e:

            print(e)
            # os.remove(mediaPath+"/"+str(uploadedFile))


        # context.update({"MSG":"UPLOADED","uploadedData":uploadedData})


    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context=context)

@login_required
def download_data(request):

    # pageDictKey = "downloadPage"

    fileName = f"QUIZ_DATA-{now()}"


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachement; filename= "{fileName}.xlsx"'
    writer = csv.writer(response)

    writer.writerow(
        [
         "QUESTION_ID",
         "ACTUAL QUESTION",
         "ENROLLMENT NUMBER",
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
                                        'CATEGORY',
                                        'ANSWER',
                                        'CORRECT_ANSWER',
                                        "START_TIME",
                                        )

    for user in users:
        writer.writerow(user)

    return response

@login_required
def template_download(request, setNO):

    fileName_dict = {
    1:"UPLOAD_STUDENTS_DATA_SET_A",
    2:"UPLOAD_ENROLLMENTS_FOR_TEST_SET_B",
    3:"UPLOAD_QUESTIONS_SET_C",
    }



    fileName = fileName_dict[int(setNO)]


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachement; filename= "{fileName}.xlsx"'
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


    return response

@login_required
def dashboard(request):

    pageDictKey = 'dashboard'

    context={
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
                                            # SEMESTER__in=program,
                                            # GENDER__in=gender,
                                            ).values("PROGRAM", "ENROLLMENT_NUMBER",).annotate(COUNT=Count("ENROLLMENT_NUMBER")).order_by("PROGRAM", "ENROLLMENT_NUMBER",)

        schoolWiseFourty = actualdata.filter(COUNT__gte=40).count()

        totalStrength_PRG = UserRegistration.objects.filter(
                                            PROGRAM__in=program,
                                            # SEMESTER__in=program,
                                            # GENDER__in=gender,
                                            ).count()

        completionPrcnt = round((schoolWiseFourty/totalStrength_PRG)*100,1)

        #  list of students with all questions attempted
        allQuestionAtmptd_school = list(actualdata.filter(COUNT__gte=40).values_list("ENROLLMENT_NUMBER", flat=True))
        query1_answer_one = UserRegistration.objects.filter(
                                            ENROLLMENT_NUMBER__in=allQuestionAtmptd_school,
                                            )
        query1_answer_two = UserRegistration.objects.filter(PROGRAM__in=program).exclude(
                                            ENROLLMENT_NUMBER__in=allQuestionAtmptd_school,
                                            )
        schoolLists_fetched = list(query1_answer_one.values_list("SCHOOL", flat=True).distinct())


        context.update({
            "DASH": "ENABLED",
            "students_with_all_fourth":students_with_all_fourthy,
            "TOTAL_ATTEMPT":TOTAL_ATTEMPT,
            # query1
            "schoolNames": ", ".join(schoolLists_fetched),
            "completionPrcnt":completionPrcnt,
            "query1_answer_one":query1_answer_one,
            "query1_answer_two":query1_answer_two,

            })

    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)

def get_report(enrollmentNo):

    studntRep = QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=enrollmentNo,)
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
            print("studntRep \n", studntRep)
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

        try:
            studntRep = get_report(enrollmentid)
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
            print(timeTakenSeries)
            # question
            questionTable = QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=enrollmentid)#.order_by("CATEGORY")

            context.update({
            'studentData':studentData,
            'studntRep':studntRep,
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
        except:
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

    context={
    "pageDictKey":pageDictKey,
    "status":status,
    "resultStat":get_result_status(),
    }

    if int(status) != get_result_status():

        update_result_status(request, status)

        context.update({"resultStat":get_result_status(),})

    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)
