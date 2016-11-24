import glob

class IozoneTest:
    def __init__(self, testname):
        self.name = testname
        self.results = {}

    def add_result(self, kb, reclen, num):
        if not kb in self.results.keys():
            self.results[kb] = {reclen:num}
        else:
            self.results[kb][reclen] = num
        #self.results[(kb, reclen)] = num

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
                newdn[loc2] =  up[loc1] +" "+  dn[loc2]
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
        self.tests = {}
        lastpos, x =  self.findTests()
        i = 2
        for k, v in sorted(x.items())[2:]:
            self.tests[i] = IozoneTest(v)
            i += 1
        self.parse(lastpos)
        #for k,v in self.tests.items():
        #    print k,v.name
        #    for kk, vv in v.results.items():
        #        print v.name, kk, sorted(vv)
        

    def findTests(self):
        oldline = self.content[0][:-1]
        i = 1
        for line in self.content[1:]:
            newline = line[:-1]
            if newline.strip().startswith("kB  reclen"):
                if oldline.strip().startswith("File stride"):
                    # no two line test name
                    return newline.strip().split()[2:]
                else:
                    return  (i+1, two_line_headers(oldline, newline))
            else:
                oldline=newline
            i+=1

    def parse(self, lastpos):
        for pos in range(lastpos, len(self.content)):
            line = self.content[pos].strip()
            if len(line.strip()) == 0:
                break
            t = line.split()
            kb = int(t[0])
            reclen = int(t[1])
            i = 2
            for n in t[2:]:
                self.tests[i].add_result(kb, reclen, n)
                i += 1
                

class IozoneTestGroup:
    def __init__(self, description, directory):
        self.description = description
        self.directory = directory
        self.tests = {}
        for fname in glob.glob("%s/*" % self.directory):
            self.tests[fname] = Iozone(fname)

        self.average = {}
        self.maximum = {}
        self.minimum = {}
        
        tests = [test.name for test in self.tests.values()[0].tests.values()]
        temp = {}
        for test in tests:
            for testitem in [k for k in self.tests.values()]:
                for testname in [k for k in testitem.tests.values()]:
                    for kb in [ k for k in testname.results.keys()]:
                        for reclen in [rec for rec in testname.results[kb].keys()]:
                            print testitem.fname, testname.name, kb, reclen, testname.results[kb][reclen]


if __name__ == "__main__":
    esoslocal = IozoneTestGroup("Esos local disk test", "esos-local")
    esosremote = IozoneTestGroup("Esos remote disk test", "esos-remote")
    #f = Iozone("sample.txt")
