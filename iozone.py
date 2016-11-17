

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
                    names = newline.strip().split()[2:]
                break
            else:
                oldline=newline

    def parse(self):
        pass


if __name__ == "__main__":
   f = Iozone("sample.txt")

