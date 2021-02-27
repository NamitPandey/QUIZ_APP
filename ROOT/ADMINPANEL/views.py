from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

# all static packages import below
import os
import pandas as pd
from . import ADMIN_PAGE_MAPPER
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


    return render(request, ADMIN_PAGE_MAPPER.pageDict[pageDictKey],context=context)
