

# ./Utils/helper_gui.py

import FreeCADGui

def show_error_dialog(title, message):
    from PySide2 import QtWidgets
    QtWidgets.QMessageBox.critical(None, title, message)
    
def select_file_dialog(caption, filter):
    from PySide2 import QtWidgets
    return QtWidgets.QFileDialog.getOpenFileName(None, caption, "", filter)[0]