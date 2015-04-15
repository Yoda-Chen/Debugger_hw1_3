from xml.parsers.xmlproc import xmlproc
import sys
import re
import outputters,getopt

#you can change the file name to you want to test
origin_file_name = 'demo/urls.xml'

#global variable
PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"
tests = {}
circumstances = []
test_file_name = "test.xml"
test_file = ""
p = ""
warnings=1
entstack=0
rawxml=0


def split(circumstances, n):
    """Split a configuration CIRCUMSTANCES into N subsets;
       return the list of subsets"""

    subsets = []
    start = 0
    for i in range(0, n):
        len_subset = int((len(circumstances) - start) / float(n - i) + 0.5)
        subset = circumstances[start:start + len_subset]
        subsets.append(subset)
        start = start + len(subset)

    assert len(subsets) == n
    for s in subsets:
        assert len(s) > 0

    return subsets

def listminus(c1, c2):
    """Return a list of all elements of C1 that are not in C2."""
    s2 = {}
    for delta in c2:
        s2[delta] = 1
        
    c = []
    for delta in c1:
        if not s2.has_key(delta):
            c.append(delta)

    return c

def ddmin(circumstances, test):    
	assert test([]) == PASS
	assert test(circumstances) == FAIL
	
	n = 2
	while len(circumstances) >= 2:
		subsets = split(circumstances, n)
		assert len(subsets) == n

		some_complement_is_failing = 0
		for subset in subsets:
			complement = listminus(circumstances, subset)

			if test(complement) == FAIL:
				circumstances = complement
				n = max(n - 1, 2)
				some_complement_is_failing = 1
				break

		if not some_complement_is_failing:
			if n == len(circumstances):
				break
			n = min(n * 2, len(circumstances))

	return circumstances

def string_to_list(s):
        c = []
        for i in range(len(s)):
            c.append((i, s[i]))
        return c

def mytest(c):
	#test_file.truncate()	
	
	test_file = open(test_file_name, 'w')

        s = ""
        for (index, char) in c:
            s += char
	test_file.write(s)

        if s in tests.keys():
            return tests[s]

        map = {}
        for (index, char) in c:
            map[index] = char

        x = ""
        for i in range(len(circumstances)):
            if map.has_key(i):
                x += map[i]
            else:
                x += "."

        print "%02i" % (len(tests.keys()) + 1), "Testing", `x`,
	test_file.close()
	try:
		p.parse_resource(test_file_name)
	except:
		print FAIL
		tests[s] = FAIL
		return FAIL
        print PASS
        tests[s] = PASS
        return PASS

if __name__ == '__main__':

	#open the .xml file
	origin_file = open(origin_file_name, 'r')
	
	app = xmlproc.Application()
	p = xmlproc.XMLProcessor()

	err=outputters.MyErrorHandler(p, p, warnings, entstack, rawxml)
	p.set_error_handler(err)

	file_str = ""
	for line in origin_file.readlines():	
		file_str = file_str + line
	
	#par_fail == 0 : sucessful, par_fail == 1 : fail
	
	circumstances = string_to_list(file_str)
	mytest(circumstances)
	
	print ddmin(circumstances, mytest)



