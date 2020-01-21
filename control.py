

import csv 
import sys
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow,QFileDialog,QTableWidgetItem
from viewGUI import *
import xlrd
    
 
class MyForm(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.excel)
        self.ui.toolButton.clicked.connect(self.openFileNameDialog)
        self.show()

    def csvload(self):
        filename = "fin.csv"
          
        # initializing the titles and rows list 
        fields = [] 
        rows = [] 
          
        # reading csv file 
        with open(filename, 'r') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
              
            # extracting field names through first row 
            fields =next(csvreader) 
          
            # extracting each data row one by one 
            for row in csvreader: 
                rows.append(row) 
          
            # get total number of rows 
            print("Total no. of rows: %d"%(csvreader.line_num)) 
          
        # printing the field names 
        print('Field names are:' + ', '.join(field for field in fields)) 
          
        #  printing first 5 rows 
        print('\nFirst 5 rows are:\n') 
        for row in rows[:csvreader.line_num]: 
            # parsing each column of a row
            count=0
            for col in row:
                count+=1 
                if(count==8):
                    break
                print("%10s"%col), 
            print('\n') 

    def openFileNameDialog(self,MainWindow):

        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.ui.lineEdit.setText(fileName)

    def excel(self,MainWindow):
        book = xlrd.open_workbook("C:/Users/ypate/fsf_2020_screening_task/input_fin.xlsx")
        sheet = book.sheets()[0] 
        shName=["FinPlate","TensionMember","BCEndPlate","CleatAngle"]
        shCol=[7,5,8,7]
        data = [] 
        print(shName[0])
        for k in range(len(shName)):
            sheet = book.sheet_by_name(shName[k])
            #sheet = book.sheet_by_index(1) 
            print(shName[k])
            r = sheet.row(0) 
            c = sheet.col_values(0) 
            
            
            for i in range(sheet.nrows):
              data.append(sheet.row_values(i))
            print(data)
            for cp in range(1,len(data)):
                for gtr in range(shCol[k]):
                    newitem = QTableWidgetItem(str(data[cp][gtr]))
                    if k==0:
                        self.ui.tableWidget.setItem(cp,gtr,newitem)
                    if k==1:
                        self.ui.tableWidget_2.setItem(cp,gtr,newitem)
                    if k==2:
                        self.ui.tableWidget_3.setItem(cp,gtr,newitem)
                    if k==3:
                        self.ui.tableWidget_4.setItem(cp,gtr,newitem)
            data.clear()
   
 
if __name__=="__main__": 

    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
# csv file name 

    