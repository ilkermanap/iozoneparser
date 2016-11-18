

class IozoneTest:
    def __init__(self, testname):
        self.name = testname
        self.results = {}

    def add_result(self, result):
        if result.test == self.name:
            self.results = 1

class IozoneRecord:
    def __init__(self, testname, kb, reclen, num):
        self.test = testname
        self.kb = kb
        self.reclen = reclen
        self.numbytes = 1024 * num

def split_with_location(line, separator=None):
    temp = {}
    t = line.strip()
    finished = False
    loc = 0
    while len(t) > 0:
        if separator is not None:
            word = t.split(separator)[0]
        else:
            word = t.split()[0]
        loc = line.find(word,loc)        
        temp[loc] = word
        loc = loc + len(word)
        t = line[loc:].strip()
    return temp

def two_line_headers(line1,line2):
    up = split_with_location(line1)
    dn = split_with_location(line2)
    newdn = dn
    for loc2 in sorted(dn.keys()):
        for loc1 in sorted(up.keys()):
            if overlap(loc2, loc2 + len(dn[loc2]), loc1, loc1 + len(up[loc1])):
                newdn[loc2] =  up[loc1] +" "+  dn[lo1c2]
                break
    return newdn

def overlap(x1,x2, y1,y2):
    res =False
    if (x1 > y2) or (x2 < y1):
        return False
    return True
        
class Iozone:
    def __init__(self, fname):
        self.fname = fname
        self.content = open(self.fname , "r").readlines()

        self.testdate = None
        self.directio = None
        self.cmdline = None
        self.output_term = None
        self.tests = None
        self.findTests()

    def findTests(self):
        oldline = self.content[0][:-1]
        for line in self.content[1:]:
            newline = line[:-1]
            if newline.strip().startswith("kB  reclen"):
                print oldline
                print newline
                if oldline.strip().startswith("File stride"):
                    # no two line test name
                    return newline.strip().split()[2:]
                else:
                    # we have two line test names, find a way to add 
                    # first parts from the oldline
                    headers = two_line_headers(oldline, newline)
                    for k,v in sorted(headers.items()):
                        print k,v
                    names = newline.strip().split()[2:]
                break
            else:
                oldline=newline

    def parse(self):
        pass


if __name__ == "__main__":
   f = Iozone("sample.txt")
