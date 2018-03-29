# infoManagement

Description 

	Used for searching in a tree of files/folder specific information.
	The program uses as input a directory containing files and/or other directories.
	Each file in the structure complies to a rule: information is displayed as belonging to a topic. Topics can have subtopics. 
	Each folder is considered to be a topic. A sub-folder is a subtopic. A file name is also a topic/subtopic.  

	Possible example of a file:  

	cinemas:
		near the center:
			cinema1, cinema2. 

	The first two lines describes topics, the last line defines the description. 

Usage
	First browse for a specific folder containing  well formated files.
	Second enter a keyword to search, and enter type of the search: topic ( searches only topics containing the keyword, return their  description and parent topics),
	description( search for descriptions containing the keyword showing the topic hierarchy they belong to), topic/description  mixed search 
	( combines the previous two types of searches in a single one). 
	If you tick edit file, after browsing to a specific folder you can view the containing files and edit them. 
	
"Installation" 
Run the script , but not before installing pyqt5 with 	"pip install pyqt5".
Pip is located in Scripts folder under your python installation directory. 
You also should have at least python3

				