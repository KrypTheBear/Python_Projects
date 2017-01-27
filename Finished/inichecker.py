import glob, re, os

'''
@brief Searches through current working directory and subfolders for files with a given variable, prints new file with results
@param var Variable to be searched for
@param fileextension Fileextension(Format ".fileextension") of the files to be search for (can be wildcard .*)
'''
def inichecker(var, fileextension):
    workingdir = os.getcwd()
    with open("vars.txt", "w") as text:
        for file in glob.glob("%s/**/*"+fileextension % workingdir, recursive=True):
            with open(file, "r+") as check:
                text.write("%s : \n" % file)
                m = re.findall("^([^\W]+(?==\s*"+re.escape(var)+"))", check.read(), re.M)
                for part in m:
                    text.write("%s\n" % part)
                text.write("\n")
