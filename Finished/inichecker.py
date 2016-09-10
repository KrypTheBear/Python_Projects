import glob, re, os
# Glob in order to detect all *.ini files
# OS to get the current workingdir
# re for our most beloved regex

def inichecker(varvalue):
    workingdir = os.getcwd()
    with open("vars.txt", "w") as text:
        for file in glob.glob("%s/**/*.ini" % workingdir, recursive=True):
            with open(file, "r+") as check:
                text.write("%s : \n" % file)
                m = re.findall("^([^\W]+(?==\s*"+re.escape(varvalue)+"))", check.read(), re.M)
                for part in m:
                    text.write("%s\n" % part)
                text.write("\n")
