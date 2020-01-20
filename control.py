

import csv 
import sys
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow,QFileDialog
from viewGUI import *

    
 
class MyForm(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.csvload)
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
   
 
if __name__=="__main__": 

    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
# csv file name 

    