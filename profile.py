"""have a profile class - 
attributes/instance variables - num,"grade",full name, experience, studies, contact, misc
skills, current job + time, studies, a short paragraph analysis (misc)

build the class, initialzing and encapsulating it - @property, @value.setter
_str_ method - returns some "Error"
using _ in all uses of the value except in init setter

class methods - ??


"""

class Candidate:
    def __init__(self, num, full_name, experience, studies, contact, misc, analysis, score):
        self.num = num
        self.full_name = full_name
        self.experience = experience
        self.studies = studies
        self.contact = contact
        self.misc = misc
        self.analysis = analysis
        self.score = score

    def __str__(self):
        return f"Num: {self.num} Full Name: {self.full_name} Experience: {self.experience} Studies: {self.studies} Contact: {self.contact} Misc: {self.misc} Analysis: {self.analysis} Score: {self.score} "

    #Getter for num
    @property
    def num(self):
        return self._num
    #Setter for num
    @num.setter
    def num(self, num):
        if num > 100:
            raise ValueError("Num above 100")
        self._num = num

    #Getter for full_name
    @property
    def full_name(self):
        return self._full_name
    #Setter for full_name
    @full_name.setter
    def full_name(self, full_name):
        #error checking - raise error
        self._full_name = full_name

    #Getter for experience
    @property
    def experience(self):
        return self._experience
    #Setter for experience
    @experience.setter
    def experience(self, experience):
        #error checking - raise error
        self._experience = experience
    
    #Getter for studies
    @property
    def studies(self):
        return self._studies
    #Setter for studies
    @studies.setter
    def studies(self, studies):
        #error checking - raise error
        self._studies = studies

    #Getter for contact
    @property
    def contact(self):
        return self._contact
    #Setter for contact
    @contact.setter
    def contact(self, contact):
        #error checking - raise error
        self._contact = contact

    #Getter for misc
    @property
    def misc(self):
        return self._misc
    #Setter for misc
    @misc.setter
    def misc(self, misc):
        #error checking - raise error
        self._misc = misc
    
    #Getter for analysis
    @property
    def analysis(self):
        return self._analysis
    #Setter for analysis
    @analysis.setter
    def analysis(self, analysis):
        #error checking - raise error
        self._analysis = analysis
    
    #Getter for score
    @property
    def score(self):
        return self._score
    #Setter for score
    @score.setter
    def score(self, score):
        #error checking - raise error
        self._score = score
    
def main(): #self, num, full_name, experience, studies, contact, misc, analysis, score
    candidate = Candidate(0, "Daniel Nama", "Little experience", "Reichman", "0584525392", "NA", "Good candidate", 75)
    print(candidate)

if __name__ == "__main__":
    main()