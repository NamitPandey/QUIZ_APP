from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
from django.http import JsonResponse,HttpResponse
from MCQ.models import QuizData, UserRegistration
from django.db.models import F, Count

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
def convert_to_str(x):

    return str(int(x))

def convert_to_dateTime(x):

    return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")

""" HOMEPAGE FOR ADMIN PANEL"""
def admin_home(request):

    pageDictKey = 'adminHome'
    # print(ADMIN_PAGE_MAPPER.pageDict.keys())
    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey],)

@login_required
def upload_files(request):

    pageDictKey = 'uploadFiles'

    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey],)

@login_required
def upload_data(request, dataBaseKey):

    pageDictKey = 'uploadPage'



    context={"MSG":"NOT_UPLOADED"}

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
def dashboard(request):

    pageDictKey = 'dashboard'
    context={
    "CATGRY": staticVariables.CATEGORY_LIST, # CATEGORY list
    "SCHOL": staticVariables.SCHOL_LIST, # school list
    "PRGM": staticVariables.PROGRM_LIST, # program list
    }


    if request.method == 'POST':

        catgry = request.POST.getlist("cat_POST")
        program = request.POST.getlist("program_POST")
        gender = request.POST.getlist("gender_POST")


    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)

def get_report(enrollmentNo):

    studntRep = QuizData.objects.filter(ENROLLMENT_NUMBER__iexact=enrollmentNo,)
    studntRep = studntRep.values('CATEGORY', 'ANSWER').filter(ANSWER__iexact = F('CORRECT_ANSWER')).order_by('CATEGORY', 'ANSWER')
    studntRep = studntRep.values('CATEGORY').annotate(COUNT = Count('CATEGORY')).order_by('CATEGORY')
    total = 100/sum(studntRep.to_dataframe()['COUNT'])
    studntRep = studntRep.annotate(PER=F('COUNT')*total).order_by('CATEGORY')

    return studntRep

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
def student_report(request):

    pageDictKey = 'student'


    studentData = UserRegistration.objects.filter(ENROLLMENT_NUMBER__iexact=request.user.username).values()

    context = {
    'WARNING_MSG': 'DISABLE',
    'studentData':studentData,
    }

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

        studntRep = get_report(enrollmentid)
        piechartSeries, columnSeries, categoryList = highchart(studntRep)
        TOTAL_CRT = sum(studntRep.to_dataframe()['COUNT'])

        context.update({
        'studentData':studentData,
        'studntRep':studntRep,
        'TOTAL_CRT':TOTAL_CRT,

        'categoryList':categoryList,
        'piechartSeries':piechartSeries,
        'columnSeries': columnSeries,
        })
    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)
