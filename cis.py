'''
********************************************************
Filename:            cis.py

Author:              Andrew Yee, Andrew Liu

Date:                6/17/2019

Modifications:       

Description:         This module focuses on our understanding on regular expressions, functions as first order objects, packing/unpacking, and generators. 
                     There is one class in this module named CIS which contains a constructor, 4 methods (getaline, searchByTopic, searchByNumber, and 
                     searchByQuarter) 
                     and a main method to run the code. The 4 methods all get data and help to find all 4 pieces of information for a course.

Data Structures:     The use of a generator was used to store the lines of a file. After separating eat line into its respective category using regex, we stored those
                     groups data into a list. 


********************************************************
'''
import re

classList = "lab5in.txt"


class CIS:
    classregex = r'<strong>(CIS\s\d+[A-Z]*)(?:\s\(.+\))?</strong>'
    nameregex = r'<.*>(?:<.*>)?([A-Za-z0-9\s\.\-/+#]+)(?:&nbsp;)?(?:</a>.*)?</td>'
    quarterregex = r'<strong>(?:&nbsp;)?(x)'
    quarters = ["Fall", "Winter", "Spring", "Summer"]

    def __init__(self, infileName=classList):
        ''' Reads the lines in the file with the help of the getaline method and stores two groups and a list into self.classes. The groups are obtained from the line we read, with the first group containing the CIS class number and the second group containing the class name. The last index of self.classes contains the quarters the class is available in.
                    Argument: self, infileName=classList, the classList is the default filename constant therefore it is optional
                    Return: None
                '''        

        self.classes = []
        with open(infileName, "r") as file:
            filedata = self.getaline(file)
            for line in filedata:
                line = line.rstrip("\r\n")
                matchclass = re.search(self.classregex, line) # Find a class
                if matchclass:
                    next(filedata)  # Not entirely sure why this ends up being needed, but it eats a blank line
                    line = next(filedata)
                    matchname = re.search(self.nameregex, line) # Find class name
                    quarterList = ""
                    for quarter in range(4):
                        next(filedata)
                        line = next(filedata)
                        matchquarter = re.search(self.quarterregex, line)
                        if matchquarter:
                            if quarterList != "":
                                quarterList += " " + CIS.quarters[quarter]
                            else:
                                quarterList = CIS.quarters[quarter]
                    self.classes.append([matchclass.group(1), matchname.group(1), quarterList])
        print("Found", len(self.classes), "CIS classes")

    def getaline(self, file):
        ''' This is a generator function that reads a line from a file
            Argument: self, file
            Yield: inputLine (a line from a file)
        '''        
        while True:
            inputLine = file.readline()
            if not inputLine:
                break
            yield inputLine

    def searchByNumber(self, classnum, exact=False):
        ''' Finds all the class numbers and storing it in the regexString (after the CIS in each line).
            re.compile was used to turn RegexString into a regex object. That object is stored in a list called self.listOfClasses.
            Argument: self, classnum, exact = false
            Return: self.listOFClasses
                    
        '''        
        regexPattern = "CIS " + str(classnum) + "$" if exact else "CIS " + ".*"  + str(classnum) + ".*"
        self.listOfClasses = [c for c in self.classes if re.search(regexPattern, c[0], re.I)]
        return self.listOfClasses

    def searchByTopic(self, topic):
        ''' Tries to find the topic the user is looking for and appends it to self.listOFClasses.
            Argument: self, topic
            Return: self.listOFClasses           
        '''         
        self.listOfClasses = [c for c in self.classes if re.search(r"\b" + topic + r"\b", c[1], re.I)]
        return self.listOfClasses

    def searchByQuarter(self, quarter):
        ''' Determines which quarters the class is offered in.
            Argument: self, quarter
            Return: [] if not a valid quarter, self.listOFClasses
        '''          
        self.listOfClasses = [c for c in self.classes if re.search(quarter, c[2])]
        return self.listOfClasses


def main():
    c = CIS()
    print(c.searchByNumber(2))
    print()
    print(c.searchByNumber(2, exact=True))
    print()
    print(c.searchByTopic('C'))
    print()
    print(c.searchByQuarter("Summer"))

if __name__=="__main__":
    main()