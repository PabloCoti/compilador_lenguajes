from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load Ui
        uic.loadUi("views/designs/main_view.ui", self)

        # show
        self.show()

        # At Start
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 370)

        # Do something
        self.openFile.clicked.connect(self.create)

    def create(self) -> None:
        # Get file path
        file_name = QFileDialog.getOpenFileName(self, 'Select Program', 'D:/', 'File (*.txt)')

        # if chosen a file
        if file_name[0] != '':
            # print(file_name)

            # Get file actual name
            def get_name(string):
                def invertir_cadena(chain):
                    return chain[::-1]

                cadena_invertida = invertir_cadena(string)
                counter = 0
                letter = ''
                new_string = ''
                while letter != '/':
                    new_string += letter
                    letter = cadena_invertida[counter]
                    counter += 1

                name = invertir_cadena(new_string)
                return name

            # set file edit text to song's name
            self.file_name.setText(get_name(file_name[0]))

            # update table
            self.compile()

    # check code for errors
    def compile(self):
            pass
