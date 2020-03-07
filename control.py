
import json
import csv 
import sys
from PyQt5.QtWidgets import *
from viewGUI import *
import xlrd
    
 
class MyForm(QMainWindow):
    validate=0
    openD=0
    dataExcel=[]
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.cp_validate)
        self.ui.pushButton_2.clicked.connect(self.excel)
        self.ui.pushButton_3.clicked.connect(self.cp_submit)
        self.ui.toolButton.clicked.connect(self.openFileNameDialog)
        self.ui.tabWidget_3.currentChanged.connect(self.onChange)

        self.show()

    def onChange(self,i): #changed!
        noter=0
        print(self.dataExcel)
        self.ui.note_table.clear()
        try:

            for j in range(1,len(self.dataExcel[i])):
                self.addNote(self,len(self.dataExcel[i][0]),self.dataExcel[i][j],noter)
                noter+=1
        except:
            pass


    def addNote(self,MainWindow,x,list,noter):
        shCol=[7,5,8,7]
        curr=self.ui.tabWidget_3.currentIndex()
        try:
            notec=0
            
            newitem = QTableWidgetItem(str(list[shCol[curr]]))
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.note_table.setItem(noter,notec,newitem)

            notec+=1
            newitem = QTableWidgetItem(str(list[shCol[curr]+1]))
            newitem.setFlags(QtCore.Qt.ItemIsEnabled)
            self.ui.note_table.setItem(noter,notec,newitem)
        except:
            pass


    def csvload(self,MainWindow,filename):
        
          
        # initializing the titles and rows list 
        fields = [] 
        rows = [] 
        shCol=[7,5,8,7]
        k=0
        noter=0
        # reading csv file 
        with open(filename, 'r') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
              
            # extracting field names through first row 
            fields =next(csvreader) 
            while('' in fields):
                fields.remove('')
            
            k=self.cp_detect(fields)
            self.ui.tabWidget_3.setCurrentIndex(k)
            # extracting each data row one by one 
            for row in csvreader: 
                rows.append(row)
                row.remove("")
                self.dataExcel.append(rows)
                if(len(row)>shCol[k]):
                    self.addNote(self,shCol[k],row,noter)
                    noter+=1 

        data=[]
        r=0
        for row in rows[:csvreader.line_num]: 
            # parsing each column of a row
            count=0
            c=0
            for col in row:
                count+=1 
                if(count>=len(fields)):
                    r+=1
                    break
                data.append(col)
                
                if col==0:
                    newitem = QTableWidgetItem(str(col))
                else:
                    newitem = QTableWidgetItem(str(col))
                    
                if k==0:
                    self.ui.tableWidget.setRowCount(len(data)+50)
                    self.ui.tableWidget.setItem(r,c,newitem)

                if k==1:
                    self.ui.tableWidget_2.setRowCount(len(data)+50)
                    self.ui.tableWidget_2.setItem(r,c,newitem)

                if k==2:
                    self.ui.tableWidget_2.setRowCount(len(data)+50)
                    self.ui.tableWidget.setItem(r,c,newitem)                    
                if k==3:
                    self.ui.tableWidget_2.setRowCount(len(data)+50)
                    self.ui.tableWidget_2.setItem(r,c,newitem)                        
                c+=1

            
    def cp_detect(self,fields):
        if 'Connection type' in fields:
            return 0
        elif 'Member length' in fields:
            return 1
        elif 'End plate type' in fields:
            return 2
        elif 'Angle leg 1' in fields:
            return 3
        return 0
    def openFileNameDialog(self,MainWindow):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","*.csv *.xlsx", options=options)
        if fileName:
            
            self.ui.lineEdit.setText(fileName)
            self.openD=1


    def excel(self,MainWindow):
        self.dataExcel.clear()
        self.clear_all(self)
        if(self.ui.lineEdit.text()=="") or self.openD==0:
            try:
                self.openFileNameDialog(self)
            except:
                self.openD=0
        self.openD=0
        textstring=self.ui.lineEdit.text()    
        if(textstring[len(textstring)-4:len(textstring)]=='.csv') or (textstring[len(textstring)-5:len(textstring)]=='.xlsx'):
            if(textstring[len(textstring)-4:len(textstring)]=='.csv'):
                self.csvload(self,textstring)
            else:
                filen=self.ui.lineEdit.text()
                book = xlrd.open_workbook(filen)
                sheet = book.sheets()[0] 
                shName=["FinPlate","TensionMember","BCEndPlate","CleatAngle"]
                shCol=[7,5,8,7]
                data = [] 
                for k in range(len(shName)):
                    sheet = book.sheet_by_name(shName[k])
                    r = sheet.row(0) 
                    c = sheet.col_values(0) 
                    
                    
                    for i in range(sheet.nrows):
                        data.append(sheet.row_values(i))
                        try:
                            while 1:
                                data[i].remove("")
                        except: 
                            pass
                    self.dataExcel.append(data)
                
                    ko=self.cp_detect(data[0])
                    for cp in range(1,len(data)):
                        for gtr in range(shCol[k]):
                            if gtr==0:
                                newitem = QTableWidgetItem(str(int(data[cp][gtr])))
                            else:
                                newitem = QTableWidgetItem(str((data[cp][gtr])))
                            if ko==0:
                                self.ui.tableWidget.setRowCount(len(data)+50)
                                self.ui.tableWidget.setItem(cp,gtr,newitem)
                            if ko==1:
                                self.ui.tableWidget_2.setRowCount(len(data)+50)
                                self.ui.tableWidget_2.setItem(cp,gtr,newitem)
                            if ko==2:
                                self.ui.tableWidget_3.setRowCount(len(data)+50)
                                self.ui.tableWidget_3.setItem(cp,gtr,newitem)
                            if ko==3:
                                self.ui.tableWidget_4.setRowCount(len(data)+50)
                                self.ui.tableWidget_4.setItem(cp,gtr,newitem)
                    data=[]
                curr=self.ui.tabWidget_3.currentIndex()
                self.onChange(curr)
    def cp_validate(self,MainWindow):
        shCol=[7,5,8,7]
        shN=["tableWidget","tableWidget_2","tableWidget_3","tableWidget_4"]
        
        p=0
        j=0
        for i in range(len(shCol)):  
            table = (self.findChild(QTableWidget,shN[i]))  
            for p in range(table.rowCount()):
                for j in range(shCol[i]):
                    if(table.item(p,j)==None):
                        continue
                    try:

                        float(str(table.item(p,j).text()))
                        v=1    
                    except ValueError:
                        v=0
                    if v==0:
                        msg=QMessageBox()
                        msg.setWindowTitle("WARNING")
                        msg.setText("Enter Float or int")
                        x = msg.exec_()  # this will show our messagebox
                        return
        self.validate=1
        self.cp_valUniq(shCol,shN)



    def cp_valUniq(self,shCol,shN):
        index=[]

        for i in range(len(shCol)):
            table=(self.findChild(QTableWidget,shN[i]))
            for p in range(table.rowCount()):
                try:
                    val=str(table.item(p,0).text())
                    if val in index:
                        self.validate=0
                        msg=QMessageBox()
                        msg.setWindowTitle("WARNING")
                        msg.setText("Enter Unique ID")
                        x = msg.exec_()  # this will show our messagebox
                        return
                    else:
                        index.append(val)
                except:
                    pass
            index.clear()
        msg=QMessageBox()
        msg.setWindowTitle("VALIDATED")
        msg.setText("You may now proceed to submit")
        x = msg.exec_()  # this will show our messagebox
        return

    def cp_submit(self,MainWindow):
        if self.validate==1:
            shCol=[7,5,8,7]
            shN=["tableWidget","tableWidget_2","tableWidget_3","tableWidget_4"]
            sheetname=["FinPlate","TensionMember","BCEndPlate","CleatAngle"]
            p=0
            j=0
            dictionary={}
            for i in range(len(shCol)):  
                count=0
                table = (self.findChild(QTableWidget,shN[i]))  
                for p in range(table.rowCount()):
                    for j in range(shCol[i]):
                        if(table.item(p,j)==None):
                            continue
                        
                        key=table.horizontalHeaderItem(j).text().rstrip()
                        value=(table.item(p,j).text())
                        dictionary[str(key)]=value
                    if dictionary!={}:
                        count+=1
                        name_file=sheetname[i]+"_"+str(count)+".txt"
                        self.cp_createfile(dictionary,name_file)
                    dictionary.clear()
            self.validate=0
            msg=QMessageBox()
            msg.setWindowTitle("SUBMITTED")
            msg.setText("Text files created at the location of the application")
            x = msg.exec_()  # this will show our messagebox
        else:
            msg=QMessageBox()
            msg.setWindowTitle("WARNING")
            msg.setText("Please Validate Before Submiting")
            x = msg.exec_()  # this will show our messagebox



    def cp_createfile(self,dictionary,name_file):
        f = open(name_file, "w")
        f.write(str(json.dumps(dictionary)).replace("{","").replace("}", ""))
        f.close()

    def clear_all(self,MainWindow):
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setRowCount(50)

        self.ui.tableWidget_2.setRowCount(0)
        self.ui.tableWidget_2.setRowCount(50)
 
        self.ui.tableWidget_3.setRowCount(0)
        self.ui.tableWidget_3.setRowCount(50)

        self.ui.tableWidget_4.setRowCount(0)
        self.ui.tableWidget_4.setRowCount(50)
if __name__=="__main__": 

    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())

    