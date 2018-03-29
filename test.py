import os
import sys

from pathlib import Path
from   PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QHBoxLayout, QPushButton, QLineEdit, QGridLayout, QPlainTextEdit, QFileDialog, QCheckBox
from   PyQt5 import QtGui

def removeEmptyTopics(content):
	while True:
		n = len(content)
		if n >= 2:
			removed = False
			for i in range(n - 1):
				# the same identation level

				if content[i].rfind("\t") >= content[i + 1].rfind("\t") and len(content[i]) > 4 and len(
						content[i + 1]) > 4:
					if (":" in content[i]) and (":" in content[i + 1]):
						# after removal index i+1 becomes i
						content.remove(content[i])
						removed = True
						break
			if not removed:
				break
		else:
			break
	if len(content) == 1:
		content = []
	return content

def removeTrailingTopics(content):
	while True:
		n = len(content)
		removed = False
		if n >= 1:
			if ":" in content[-1]:
				content.remove(content[-1])
				removed = True
		else:
			break

		if not removed:
			break

	return content




def dig(globalContent, file, indentLevel, inputDescription, inputTopicDescription):
	tabsString = ""
	for i in range(indentLevel):
		tabsString += "\t"

	content = []
	with open(file) as f:
		for line in f:
			if ":" in line:
				content.append(tabsString + line)
				#print(tabsString + line)
			#pass
			#skip the empty lines
			elif len(line) > 1:
				if ( (inputDescription in line) and  len(inputDescription) > 1 ) or ((inputTopicDescription in line) and len(inputTopicDescription)> 1):
					#print(tabsString + "\t" + line)
					content.append(tabsString  + line)
				elif len(inputDescription) <= 1 and len(inputTopicDescription) <= 1:
					#print(tabsString + "\t" + line)
					content.append(tabsString  + line)

	#remove empty lines
	content = [ line for line in content if line.strip()]
	content = removeEmptyTopics(content)
	globalContent.extend(content)


def parseFile(content, file, nodeName, indentLevel, inputDescription, inputTopicDescription):
	tabsString = ""
	for i in range(indentLevel):
		tabsString += "\t"
	content.append(tabsString + str(os.path.basename(nodeName)) + ":\n")
	content.append(tabsString + "\t" + str(os.path.splitext(os.path.basename(file))[0]) + ":\n")
	dig(content, file, indentLevel + 2, inputDescription, inputTopicDescription)

def list(content, nodeName, indentLevel, inputDescription, inputTopicDescription):
	files = [x for x in nodeName.iterdir()]
	for file in files:
		if file.is_file():
			fileTokens = os.path.splitext(os.path.basename(file))
			if  len(fileTokens) == 2 and str(fileTokens[1]) == ".txt":
				parseFile(content, file, nodeName, indentLevel, inputDescription, inputTopicDescription)
		else:
			list(content, file, indentLevel + 1, inputDescription, inputTopicDescription)

def getContentFilteredByTopic(p, inputTopic):
	content = []
	list(content, p, 0, "", "")
	content = [line for line in content if line.strip()]
	contentFilteredTopic = buildFilteredTopics(content, inputTopic)
	return contentFilteredTopic

def buildFilteredTopics(content, keyword):
	filteredContent = []
	n = len(content)
	found = False

	for i in range(n):
		if (":" in content[i]) and (keyword in content[i]) and (len(keyword) > 1):
			found = True
			filteredContent.append(content[i])
			it_pos = content[i].rfind("\t")
			for j in range(i-1, 0, -1):
				if (content[j].rfind("\t") < it_pos) and (":" in content[j]):
					filteredContent.insert(0, content[j])
					it_pos = content[j].rfind("\t")
			it_pos = content[i].rfind("\t")
			for j in range(i+1, n):
				if content[j].rfind("\t") > it_pos:
					filteredContent.append(content[j])
				else:
					break
		elif len(keyword) <= 1:
			return content

		if found:
			break

	filteredContent = removeTrailingTopics(filteredContent)
	return filteredContent

def getContentFilteredByDescription(p, inputDescription):
	content = []
	list(content, p, 0, inputDescription, "")
	content = [line for line in content if line.strip()]

	if len(inputDescription) > 1:
		content = removeEmptyTopics(content)
		content = removeTrailingTopics(content)
	return content
					
def btnstate(b):
	global inputType
	if b.text() == "Topic" and b.isChecked():
		print(b.text()+" is selected")
		inputType = 1

	if b.text() == "Description" and b.isChecked():
		print(b.text()+" is selected")
		inputType = 2

	if b.text() == "Topic/Description" and b.isChecked():
		print(b.text()+" is selected")
		inputType = 3
		
				
def browseCallback(b):
	dialog = QFileDialog()
	dialog.setDirectory('C:\\')
	dialog.setFileMode(QFileDialog.AnyFile)
	global informationPath
	informationPath = str(dialog.getExistingDirectory())
	if  b51.isChecked():
		dialog.getOpenFileNames()
	print(informationPath)

def searchCallback(b):
	try:
		p = Path(informationPath)
		print("search informationPath " + informationPath)
	except:
		print("Invalid directory path")
		exit(0)

	b0.clear()

	if inputType == 1:
		contentFilteredTopic = getContentFilteredByTopic(p, b4.text())
		for line in contentFilteredTopic:
			b0.appendPlainText(line)

	elif inputType == 2:
		content = getContentFilteredByDescription(p, b4.text())
		for line in content:
			b0.appendPlainText(line)

	else:
		content = getContentFilteredByDescription(p, b4.text())
		contentFilteredTopic = getContentFilteredByTopic(p, b4.text())
		if (contentFilteredTopic != content) and (not content in contentFilteredTopic) and \
				(not contentFilteredTopic in content):
			content.extend(contentFilteredTopic)
		for line in content:
			b0.appendPlainText(line)

				
app = QApplication(sys.argv)
inputType = 0
informationPath = ""

font = QtGui.QFont("Times New Roman", 14)
# QtWidgets.QApplication.setFont(font, "QPlainTextEdit")
QApplication.setFont(font)

window = QWidget()
window.resize(800 , 550)
window.setWindowTitle('File management')
window.show()

grid = QGridLayout(window)

b0 = QPlainTextEdit();
grid.addWidget(b0,1,1,1,4)
		
b1 = QRadioButton("Topic")
b1.setChecked(True)
b1.toggled.connect(lambda:btnstate(b1))
grid.addWidget(b1, 2, 1)

b2 = QRadioButton("Description")
b2.toggled.connect(lambda:btnstate(b2))
grid.addWidget(b2, 2, 2)

b3 = QRadioButton("Topic/Description")
b3.toggled.connect(lambda:btnstate(b3))
grid.addWidget(b3, 2, 3)

b4 = QLineEdit("key")
grid.addWidget(b4, 2, 4, 1, 1)

b5 = QPushButton("Browse")
b5.clicked.connect(lambda:browseCallback(b5))
grid.addWidget(b5, 3, 2, 1, 1)

b51 = QCheckBox("Edit file")
grid.addWidget(b51, 3, 3, 1, 1)

b6 = QPushButton("Search")
b6.clicked.connect(lambda:searchCallback(b6))
grid.addWidget(b6, 3, 4, 1, 1)


sys.exit(app.exec_())




