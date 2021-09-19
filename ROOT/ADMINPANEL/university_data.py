import os
import pandas as pd


class UniversityData:

    def __init__(self):

        MEDIA_ABS_PTH  = "./media"
        fileName = os.listdir(MEDIA_ABS_PTH)[0]
        filePath = os.path.join(MEDIA_ABS_PTH, fileName)
        columnsName = ['SR.NO.', 'NAME_AS_PER_HSC_MARKSHEET', 'BRANCH',
               'SEMESTER', 'ROLL_NUMBER', 'GENDER', 'GSFCU_EMAIL_ID_ADDRESS', "FIRST_NAME", "LAST_NAME"]

        createMail = lambda x: str(x)+"@gsfcuniversity.ac.in"
        convtr_to_title = lambda x: str(x).title()

        try:
            if (".xlsx" in fileName) or (".xls" in filename):
                print(fileName, filePath)
                self.file = pd.read_excel(filePath)
                self.file.columns = [_.strip().upper().replace(" ","_") for _ in self.file.columns]
                self.file = self.file[columnsName[:-2]]
                self.file['SR.NO.'].fillna("ABC1", inplace=True)
                self.file = self.file[self.file['SR.NO.'] != "ABC1"]
                self.file["FIRST_NAME"] = [" ".join(_.split(" ")[:-1]) for _ in self.file['NAME_AS_PER_HSC_MARKSHEET']]
                self.file["LAST_NAME"] = [_.split(" ")[-1] for _ in self.file['NAME_AS_PER_HSC_MARKSHEET']]
                self.file["GSFCU_EMAIL_ID_ADDRESS"] = self.file["ROLL_NUMBER"].apply(createMail)
                self.file['GENDER'] = self.file['GENDER'].apply(convtr_to_title)
                self.file['SEMESTER'] = self.file['SEMESTER'].apply(int)
                print(self.file)
        except Exception as e:
            print(f"Error: {e}")
            self.file = pd.DataFrame(columns=columnsName)

    def search_enrollment(self,enrollment):

        result = self.file.query(f"ROLL_NUMBER == '{enrollment.strip().upper()}'")

        if len(result) > 0:

            return "YES"

        return "NO"

    def get_enrollment_detail(self,enrollment):

        resultedFile =  self.file.query(f"ROLL_NUMBER == '{enrollment.strip().upper()}'")
        resultedFile.reset_index(drop=True, inplace=True)
        return resultedFile['FIRST_NAME'][0], resultedFile['LAST_NAME'][0], resultedFile['SEMESTER'][0], resultedFile['GENDER'][0]
