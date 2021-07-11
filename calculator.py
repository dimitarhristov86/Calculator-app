import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLineEdit, QPushButton, QVBoxLayout
from functools import partial

__version__ ='0.1'
__author__ = 'Dimitar Hristov'

ERROR_MSG = 'ERROR'


def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result


class CalcCtr:

    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignals()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'MC'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))
        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['MC'].clicked.connect(self._view.clearDisplay)



class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.setFixedSize(500, 500)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()
        self._createButtons()


    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createAdditionalButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {
            'Backspace': (0, 0),
            'Clear All': (0, 1),
            'Clear': (0, 2)}
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(120, 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        self.generalLayout.addLayout(buttonsLayout)

    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {
            'MC': (0, 0),
            '7': (0, 1),
            '8': (0, 2),
            '9': (0, 3),
            '/': (0, 4),
            'Sqrt': (0, 5),
            'MR': (1, 0),
            '4': (1, 1),
            '5': (1, 2),
            '6': (1, 3),
            '*': (1, 4),
            'x2': (1, 5),
            'MS': (2, 0),
            '1': (2, 1),
            '2': (2, 2),
            '3': (2, 3),
            '-': (2, 4),
            '1/x': (2, 5),
            'M+': (3, 0),
            '0': (3, 1),
            '.': (3, 2),
            '+-': (3, 3),
            '+': (3, 4),
            '=': (3, 5),
}
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40, 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText('')


def main():
    calc = QApplication([])
    view = CalculatorApp()
    view.show()
    model = evaluateExpression
    CalcCtr(model=model, view=view)
    sys.exit(calc.exec_())




