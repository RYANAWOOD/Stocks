import enum

class Relation(enum.Enum):
    NA = 0
    EQ = 1
    GT = 2
    GTE = 3
    LT = 4
    LTE = 5

class PatternSet():
    
    patterns = []
  
    def AddPattern(self, n=""):  # this method not yet tested
        self.patterns.append(Pattern(n))
        return(len(self.patterns))

    def LoadSet(path):
    
        file = open(path, 'r')
        lines = file.read().splitlines()
        for line in lines:
            elements = line.split(' ')
            self.AddPattern(elements[0])

            for i in range(int( (len(elements) - 1)/3) ):
                self.AddCondition(elements[1+3*i],relation.(elements[2+3*n]),elements[3+3*n])

        return True

if __name__ == '__main__':
    patternset = PatternSet()
    