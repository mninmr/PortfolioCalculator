'''
jpMorganExercise.py

'''
import pandas as pd
import numpy as np
from PySide import QtCore, QtGui
		

class ForecastEngine(QtGui.QWidget):

	def __init__(self, parent=None):
		super(ForecastEngine, self).__init__()
		self.initUI()
		self.setupConnections()

	def initUI(self):
		self.setGeometry(100, 100, 900, 700)
		self.setWindowTitle('Forecasting Calculator')

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
		self.runButton.setEnabled(0)

		self.viewPortButton = QtGui.QPushButton("View Portfolio")
		self.viewEconButton = QtGui.QPushButton("View Macroeconomic Data")
		self.viewPortButton.setEnabled(0)
		self.viewEconButton.setEnabled(0)

		self.emptyLable = QtGui.QLabel("")

		portLayout = QtGui.QHBoxLayout()
		portLayout.addWidget(self.portFile)
		portLayout.addWidget(self.portEdit)
		portLayout.addWidget(self.browseButtonP)

		econLayout = QtGui.QHBoxLayout()
		econLayout.addWidget(self.econFile)
		econLayout.addWidget(self.econEdit)
		econLayout.addWidget(self.browseButtonE)

		buttonLayout = QtGui.QHBoxLayout()
		buttonLayout.addWidget(self.viewPortButton)
		buttonLayout.addWidget(self.viewEconButton)

		fileLayout = QtGui.QVBoxLayout()
		fileLayout.addLayout(portLayout)
		fileLayout.addLayout(econLayout)
		fileLayout.addLayout(buttonLayout)

		lowerLayout = QtGui.QHBoxLayout()
		lowerLayout.addWidget(self.runButton)
		lowerLayout.addWidget(self.quitButton)

		self.stackLayout = QtGui.QStackedLayout()
		self.stackLayout.addWidget(self.emptyLable)

		mainLayout = QtGui.QVBoxLayout()
		mainLayout.addLayout(fileLayout)
		mainLayout.addLayout(self.stackLayout)
		mainLayout.addLayout(lowerLayout)
		self.setLayout(mainLayout)

		self.show()

	def setupConnections(self):
		self.connect(self.browseButtonP, QtCore.SIGNAL("clicked()"), self.browsePClicked)
		self.connect(self.browseButtonE, QtCore.SIGNAL("clicked()"), self.browseEClicked)
		self.connect(self.runButton, QtCore.SIGNAL("clicked()"), self.runClicked)
		self.connect(self.quitButton, QtCore.SIGNAL("clicked()"), self.on_quit)
		self.viewPortButton.clicked.connect(lambda: self.stackLayout.setCurrentWidget(self.portTable))
		self.viewEconButton.clicked.connect(lambda: self.stackLayout.setCurrentWidget(self.econTable))

	def browsePClicked(self):
		f, _ = QtGui.QFileDialog.getOpenFileName(self)
		if f != "":
			self.portEdit.setText(f)
			self.portData = self.get_data(f)
			self.portTable = self.create_table(self.portData)
			self.stackLayout.addWidget(self.portTable)
			self.viewPortButton.setEnabled(1)
			if self.viewEconButton.isEnabled():
				self.runButton.setEnabled(1)

	def browseEClicked(self):
		f, _ = QtGui.QFileDialog.getOpenFileName(self)
		if f != "":
			self.econEdit.setText(f)
			self.econData = self.get_data(f)
			self.econTable = self.create_table(self.econData)
			self.stackLayout.addWidget(self.econTable)
			self.viewEconButton.setEnabled(1)
			if self.viewPortButton.isEnabled():
				self.runButton.setEnabled(1)

	def runClicked(self):
		self.balanceTable = self.portTable
		self.balanceTable.insertColumn(self.portTable.columnCount())
		self.balanceButtons = []
		for ii in range(self.balanceTable.rowCount()):
			button = QtGui.QPushButton("View Balance")
			self.balanceTable.setCellWidget(ii+1, self.portTable.columnCount()-1, button)
			self.balanceButtons.append(button)
		self.balanceTable.resizeColumnsToContents()
		self.stackLayout.addWidget(self.balanceTable)
		self.stackLayout.setCurrentWidget(self.balanceTable)


	# may need to write a special get_data function for portfolio data
	# to avoid running out of memory
	def get_data(self, filepath):
		return pd.read_csv(filepath)

	def create_table(self, dataFrame):
		header = dataFrame.columns
		data = dataFrame.values
		table = QtGui.QTableWidget(len(data), len(header))

		for ii in range(len(header)):
			item = QtGui.QTableWidgetItem(str(header[ii]))
			table.setItem(0, ii, item)
		for ii in range(len(data)):
			for jj in range(len(header)):
				item = QtGui.QTableWidgetItem(str(data[ii][jj]))
				table.setItem(ii+1, jj, item) 
		table.resizeColumnsToContents()
		return table

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
		self.econData = MacroeconTab().econData
		self.portfolio = PortfolioTab().portfolio
		self.tableLayout = QtGui.QStackedLayout()
		self.initUI()

	def initUI(self):
		header = self.portfolio.columns
		data = self.portfolio.values
		self.table = QtGui.QTableWidget(len(data), len(header)+1)
		results = []

		for ii in range(len(header)):
			item = QtGui.QTableWidgetItem(str(header[ii]))
			self.table.setItem(0, ii, item)
		for ii in range(len(data)):
			for jj in range(len(header)):
				item = QtGui.QTableWidgetItem(str(data[ii][jj]))
				self.table.setItem(ii+1, jj, item) 
			button = QtGui.QPushButton("View Balance")
			results.append(button)
			self.table.setCellWidget(ii+1, len(header), button)
		self.table.resizeColumnsToContents()

		self.label = QtGui.QLabel("")

		
		self.tableLayout.addWidget(self.label)
		self.tableLayout.addWidget(self.table)

		mainLayout = QtGui.QVBoxLayout(self)
		mainLayout.addLayout(self.tableLayout)

		self.setLayout(mainLayout)

	@staticmethod
	def changeLayout(self):
		self.tableLayout.setCurrentWidget(self.table)

	@classmethod
	def hello(self):
		print "hello"


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