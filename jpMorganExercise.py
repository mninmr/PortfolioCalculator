'''
jpMorganExercise.py

'''
import pandas as pd
import numpy as np
from PySide import QtCore, QtGui

class ForecastEngine(QtGui.QDialog):

	def __init__(self, parent=None):
		super(ForecastEngine, self).__init__()

		self.setGeometry(100, 100, 900, 700)
		self.setWindowTitle('Forecasting Calculator')

		self.tabWidget = QtGui.QTabWidget()
		self.tabWidget.addTab(MainTab(), "Main")
		self.tabWidget.addTab(PortfolioTab(), "Portfolio")
		self.tabWidget.addTab(MacroeconTab(), "Macroeconomic Data")
		self.tabWidget.addTab(BalanceTab(), "Balance")

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addWidget(self.tabWidget)
		self.setLayout(mainLayout)

		self.show()

class MainTab(QtGui.QWidget):

	def __init__(self, parent=None):
		super(MainTab, self).__init__()
		self.initUI()
		self.setupConnections()

	def initUI(self):
		self.portFile = QtGui.QLabel("Portfolio File")
		self.econFile = QtGui.QLabel("Macroeconomic Data File")
		self.portEdit = QtGui.QLineEdit("Please import portfolio file here")
		self.econEdit = QtGui.QLineEdit("Please import macroeconomic data file here")
		self.portFile.setBuddy(self.portEdit)
		self.econFile.setBuddy(self.econEdit)

		self.browseButtonP = QtGui.QPushButton("Browse")
		self.browseButtonE = QtGui.QPushButton("Browse")

		self.quitButton = QtGui.QPushButton("Exit")
		self.runButton = QtGui.QPushButton("Run")

		upperLayout = QtGui.QHBoxLayout()
		upperLayout.addWidget(self.portFile)
		upperLayout.addWidget(self.portEdit)
		upperLayout.addWidget(self.browseButtonP)

		middleLayout = QtGui.QHBoxLayout()
		middleLayout.addWidget(self.econFile)
		middleLayout.addWidget(self.econEdit)
		middleLayout.addWidget(self.browseButtonE)

		lowerLayout = QtGui.QHBoxLayout()
		lowerLayout.addWidget(self.runButton)
		lowerLayout.addWidget(self.quitButton)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addLayout(upperLayout)
		mainLayout.addLayout(middleLayout)
		mainLayout.addLayout(lowerLayout)
		mainLayout.addStretch(1)
		self.setLayout(mainLayout)

	def setupConnections(self):
		self.connect(self.browseButtonP, QtCore.SIGNAL("clicked()"), self.browsePClicked)
		self.connect(self.browseButtonE, QtCore.SIGNAL("clicked()"), self.browseEClicked)
		self.connect(self.quitButton, QtCore.SIGNAL("clicked()"), self.on_quit)

	def browsePClicked(self):
		f, _ = QtGui.QFileDialog.getOpenFileName(self)
		if f != "":
			self.portEdit.setText(f)

	def browseEClicked(self):
		f, _ = QtGui.QFileDialog.getOpenFileName(self)
		if f != "":
			self.econEdit.setText(f)

	def on_quit(self):
		print "exiting"
		QtCore.QCoreApplication.instance().quit()


class PortfolioTab(QtGui.QWidget):
	def __init__(self, parent=None):
		super(PortfolioTab, self).__init__(parent)
		self.portfolio = self.get_data(filename="loanData")
		self.initUI()

	def initUI(self):
		header = self.portfolio.columns
		data = self.portfolio.values
		self.table = QtGui.QTableWidget(len(data), len(header))

		for ii in range(len(header)):
			item = QtGui.QTableWidgetItem(str(header[ii]))
			self.table.setItem(0, ii, item)
		for ii in range(len(data)):
			for jj in range(len(header)):
				item = QtGui.QTableWidgetItem(str(data[ii][jj]))
				self.table.setItem(ii+1, jj, item) 
		self.table.resizeColumnsToContents()

		mainLayout = QtGui.QHBoxLayout()
		mainLayout.addWidget(self.table)
		self.setLayout(mainLayout)

	# may need to write a special get_data function for portfolio data
	# to avoid running out of memory
	def get_data(self, filepath=".", filename="loanData"):
		fpath = os.path.join(filepath, filename)
		return pd.read_csv(fpath)

class MacroeconTab(QtGui.QWidget):
	def __init__(self, parent=None):
		super(MacroeconTab, self).__init__(parent)
		self.econData = self.get_data(filename="econData")
		self.initUI()

	def initUI(self):
		header = self.econData.columns
		data = self.econData.values
		self.table = QtGui.QTableWidget(len(data), len(header))

		for ii in range(len(header)):
			item = QtGui.QTableWidgetItem(str(header[ii]))
			self.table.setItem(0, ii, item)
		for ii in range(len(data)):
			for jj in range(len(header)):
				item = QtGui.QTableWidgetItem(str(data[ii][jj]))
				self.table.setItem(ii+1, jj, item) 
		#self.table.resizeColumnsToContents()

		mainLayout = QtGui.QHBoxLayout()
		mainLayout.addWidget(self.table)
		self.setLayout(mainLayout)

	def get_data(self, filepath=".", filename="econData"):
		fpath = os.path.join(filepath, filename)
		return pd.read_csv(fpath)

class BalanceTab(QtGui.QWidget):
	def __init__(self, parent=None):
		super(BalanceTab, self).__init__(parent)


# def get_data(filepath='.', filename='loanData', **kwargs):
# 	fpath = os.path.join(filepath, filename)
# 	return pd.read_csv(fpath)
	#iter_csv = pd.read_csv(fpath, iterator=True, chunksize=5)
	#return pd.concat([chunk[chunk['Loan_Channel'] == 'A'] for chunk in iter_csv])

def calc_balance(portfolio):
	balances = []
	for loan in portfolio.values:
		L = loan[3]
		age = loan[9]
		c = loan[7]/12.0
		N = loan[6]
	return balances

def main():
	#portfolio = get_data(filename='loanData')
	#econData = get_data(filename='econData')
	app = QtGui.QApplication(sys.argv)
	calculator = ForecastEngine()
	sys.exit(app.exec_())

if __name__ == '__main__':
	import os, sys
	main()