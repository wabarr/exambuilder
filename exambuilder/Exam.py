import yaml
import random
import os
import subprocess
import string




class Exam:
    def __init__(self, dir, examYAML):
        ## Each exam has its own folder called dir, all other paths are in reference to this dir
        ## examYAML is the YAML file containing the questions
        with open(os.path.join(dir, examYAML), "r") as testfile:
            self.parsed_exam = yaml.load(testfile)
            testfile.close()
            self.dir = dir

    def make_multiple_versions(self, baseOutFileName, n=4):
        ## baseOutFileName should not include the file extension
        for versionID in string.ascii_uppercase[0:n]:
            self.make_exam(outfilename=baseOutFileName + "_VERSION_" + versionID + ".docx", makeGradingKey=True, shuffle=True, version=versionID)

    def make_exam(self, outfilename, version="A", makeGradingKey=True, shuffle=True):
        ## outfile is the name of the resulting exam document
        ## shuffle indicates whether or not questions should be shuffled
        ## key indicates whether or not this is an instructors key or not
        ## version is a letter indicating the exam version


        questions = self.parsed_exam["questions"]

        if shuffle == True:
            random.shuffle(questions)
            #for question in questions:
            #    random.shuffle(question)

        def writeExamOrKey(isKey, outfilename_possibly_with_KEY, dir):
            #writes either an exam or a key depending on the argument
            #this allows us to reuse the code to write exams and keys with the same shuffled order
            with open(os.path.join(self.dir, "temp.md"), "w") as tempfile:
                tempfile.write("%" + str(self.parsed_exam["title"]) + " (Version " + version + ")")
                if isKey:
                    tempfile.write(" ## GRADING KEY ##")
                tempfile.write("\n" + self.parsed_exam["instructions"] + "\n")
                tempfile.write("\n" + "******" + "\n")

                for question in enumerate(questions):

                    try:
                        if question[1]["fill_in"]:
                            tempfile.write("\n\n" + str(question[0] + 1) + ". " + str(question[1]["question"]) + "\n\n<br><br>")
                            tempfile.write("\_" * 45 + "\n\n")
                    except KeyError: #these are multiple choice questions
                        try:
                            ## include the image if it is there
                            if question[1]["image"]:
                                tempfile.write("![](%s)" %(os.path.join(dir, "images/", str(question[1]["image"]),)), )
                        except KeyError:
                            pass

                        tempfile.write("\n\n" + str(question[0] + 1) + ". " + str(question[1]["question"]) + "\n\n")
                        answers = []

                        #format your answers depending on whether we are dealing with a key or not
                        for answer in question[1]["answers"]:
                            if isKey and str(answer).find("**") > -1:
                                answers.append("**" + str(answer).replace("**","") + "**")
                            else:
                                answers.append(str(answer).replace("**",""))

                        for answer in enumerate(answers):
                            tempfile.write("    "  + string.ascii_uppercase[answer[0]] + ".  " + str(answer[1]) + "\n")
                        tempfile.write("\n\n")


            args=["pandoc",
                  "-s",
                  "-o",
                  os.path.join(self.dir,  outfilename_possibly_with_KEY)]

            fullRefPath = os.path.join(self.dir, "reference.docx")
            if os.path.isfile(fullRefPath):
                args.append("--reference-docx")
                args.append(fullRefPath)

            args.append(os.path.join(self.dir, "temp.md"))
            try:
                subprocess.check_call(args)
                os.remove(os.path.join(self.dir, "temp.md"))
            except:
                print(subprocess)
                print(args)

        if makeGradingKey:
            writeExamOrKey(isKey=True, outfilename_possibly_with_KEY = outfilename.replace("\.docx", "") + "_KEY" + ".docx", dir=self.dir)
            writeExamOrKey(isKey=False,outfilename_possibly_with_KEY = outfilename, dir=self.dir)
        else:
            writeExamOrKey(isKey=False,outfilename_possibly_with_KEY = outfilename, dir=self.dir)