from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
from django.http import JsonResponse,HttpResponse
from MCQ.models import QuizData, UserRegistration

# all static packages import below
import csv
import os
import pandas as pd
from . import ADMIN_PAGE_MAPPER, staticVariables
from sqlalchemy import create_engine

# Create your views here.
global dataBaseMapper

dataBaseMapper={
 1:'MCQ_allowedenrollments',
 2:'MCQ_enrollemntsforquiz',
 3:'MCQ_question',
 }

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
    "GNDR": staticVariables.GENDR_LIST, # gender list
    "SCHOL": staticVariables.SCHOL_LIST, # school list
    "PRGM": staticVariables.PROGRM_LIST, # program list
    }


    if request.method == 'POST':

        school = request.POST.getlist("school_POST")
        program = request.POST.getlist("program_POST")
        gender = request.POST.getlist("gender_POST")

        print(school, program, gender)
















    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)

@login_required
def student_report(request):

    pageDictKey = 'student'

    context = {
    'WARNING_MSG': 'DISABLE',
    }

    if request.method == 'POST':

        enrollmentid = request.POST.get("enrollmentid")

        studentData = UserRegistration.objects.filter(ENROLLMENT_NUMBER__iexact=enrollmentid).values()
        print(studentData)
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

        context.update({
        'studentData':studentData,
        })
    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey], context)
