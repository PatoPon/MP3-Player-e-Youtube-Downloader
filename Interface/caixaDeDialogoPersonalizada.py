from PyQt5.QtWidgets import *

from .estilosCSS import estiloCaixaDialogo

class CaixaDeDialogo(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)

        self.setStyleSheet(estiloCaixaDialogo)

        self.setWindowTitle(title)
        self.layout = QVBoxLayout()

        self.label = QLabel(message)
        self.input = QLineEdit()
        self.button = QPushButton("OK")

        self.button.clicked.connect(self.accept)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)