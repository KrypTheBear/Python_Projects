import glob, re
from os import getcwd
# Glob in order to detect all *.ini files
# OS to get the current workingdir
# re for our most beloved regex

workingdir = os.getcwd()
try:
    text = open("vars.txt", "w")
    for file in glob.glob("%s/*.ini" % workingdir):
        check = open(file, "r+")
        text.write("%s : \n" % file)
        m = re.search("^([^\W]+(?==\s*30))", check.read(), re.M)
        for part in m.group(0):
            text.write("%s\n" % part)
        check.close()
        
except Exception as e:
    print(e)
    if text:
        if not text.closed:
            test.close()
    if check:
        if not check.closed:
            check.close()
    quit()
    
text.close()
