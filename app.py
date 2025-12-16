
import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

from views.ui.files_rc import qInitResources
qInitResources()

from views.main_window import MainWindow
from controllers.main_controller import MainController
from services.socket_service import SocketService


def main():
    
    window = MainWindow()
    
    socket_service = SocketService()
    socket_service.start()
    
    controller = MainController(window, socket_service)
    
    window.controller = controller
    window.socket_service = socket_service
    
    window.refresh_machine_grid = controller.refresh_machine_grid
    
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
