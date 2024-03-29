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
            self.parsed_exam = yaml.load(testfile, yaml.Loader)
            testfile.close()
            self.dir = dir

    def make_versions(self, baseOutFileName, n=4, version=None, shuffle_questions=True, shuffle_answers=True):
        ## baseOutFileName should not include the file extension
        ## version is the version identifier. If None, it will use capital letters to identify versions

        if n > 1 and version is not None:
            raise Exception("Supplying a custom version identifier only works when making a single exam version. ")

        for versionID in string.ascii_uppercase[0:n]:
            if version is None:
                pass
            else:
                versionID = version
            file = baseOutFileName + "_VERSION_" + versionID + ".docx"
            self.make_exam(outfilename=file, makeGradingKey=True, shuffle_questions=shuffle_questions, shuffle_answers=shuffle_answers, version=versionID)

    def make_exam(self, outfilename, version="A", makeGradingKey=True, shuffle_questions=True, shuffle_answers=True,):
        ## outfile is the name of the resulting exam document
        ## shuffle indicates whether or not questions should be shuffled
        ## key indicates whether or not this is an instructors key or not
        ## version is a letter indicating the exam version

        questions = self.parsed_exam["questions"]
        beginning_questions = []
        shufflable_questions = []
        ending_questions = []
        for q in questions:
            try:
                if q["do_not_shuffle_question"]:
                    #this is to maintain backwards compatibility for when this used to be the flag
                    #should use 'beginning_question' going forward
                    beginning_questions.append(q)
            except KeyError:
                try:
                    if q["beginning_question"]:
                        beginning_questions.append(q)
                except KeyError:
                    try:
                        if q["ending_question"]:
                            ending_questions.append(q)
                    except KeyError:
                        shufflable_questions.append(q)
                
        if shuffle_questions == True:
            random.shuffle(shufflable_questions)
        
        questions = beginning_questions + shufflable_questions + ending_questions


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
                        ## include the image if it is there
                        if question[1]["image"]:
                            try:
                                options = "{width=%s}" %(question[1]["img_width"],)
                            except KeyError:
                                options = ""
                            tempfile.write(
                                "![](%s)%s" % (os.path.join(dir, "images/", str(question[1]["image"])), options))
                    except KeyError:
                        pass
                    
                    try:
                        if question[1]["fill_in"]:
                            ##these are fill in the blank questions
                            tempfile.write("\n\n" + str(question[0] + 1) + ". " + str(question[1]["question"]) )
                            #tempfile.write("\_" * 45 + "\n\n")
                    except:
                        try:
                            if question[1]["matching"]:
                                ## these are matching questions
                                ## making use of pandocs piping table syntax https://pandoc.org/MANUAL.html#tables
                                tempfile.write("\n\n" + str(question[0] + 1) + ". " + str(question[1]["question"]) + "\n\n")
                                tempfile.write("|||\n--|--------|---|----------\n")
                                items = []
                                descriptions = []
                                letters = []
                                blanks_or_answers = []
                            
                                for answer in enumerate(question[1]["answers"]):
                                    items.append(answer[1]["item"])
                                    descriptions.append(answer[1]["description"])
                                    letters.append(string.ascii_uppercase[answer[0]])
                                    blanks_or_answers.append("<span custom-style='correct_answer'>__" + string.ascii_uppercase[answer[0]] + "__</span>")
                                indices = [i for i in range(0, len(items))]
                                shuffled_indices = [i for i in range(0, len(items))]
                                random.shuffle(shuffled_indices)
                                for i in indices:
                                    tempfile.write("%s. | %s | %s | %s\n" %(string.ascii_uppercase[i], items[i], blanks_or_answers[shuffled_indices[i]], descriptions[shuffled_indices[i]]))
                                tempfile.write("\n")
                            
                        except KeyError: #these are multiple choice questions

                            tempfile.write("\n\n" + str(question[0] + 1) + ". " + str(question[1]["question"]) + "\n\n")
                            answers = []

                            try:
                                #format your answers depending on whether we are dealing with a key or not
                                for answer in question[1]["answers"]:
                                    if isKey and str(answer).find("**") > -1:
                                        #depends on a character style called correct_answer, styled as you want it in reference.docx
                                        answers.append("<span custom-style='correct_answer'>" + str(answer).replace("**","") + "</span>")
                                    else:
                                        answers.append(str(answer).replace("**",""))
                                if shuffle_answers:
                                    try:
                                        check = question[1]["dont_shuffle_answers"]
                                    except KeyError: #only do this if the question lacks the dont_shuffle_answers option
                                        random.shuffle(answers)
                                
                                for answer in enumerate(answers):
                                    tempfile.write("    "  + string.ascii_uppercase[answer[0]] + ".  " + str(answer[1]) + "\n")
                                tempfile.write("\n\n")
                            except:
                                print("Exception on: " + question[1]["question"])
                    
                    


            args=["pandoc",
                  "-s",
                  "-o",
                  os.path.join(self.dir,  outfilename_possibly_with_KEY)]

            fullRefPath = os.path.join(self.dir, "reference.docx")
            if os.path.isfile(fullRefPath):
                args.append("--reference-doc")
                args.append(fullRefPath)

            args.append(os.path.join(self.dir, "temp.md"))
            try:
                subprocess.check_call(args)
                #print(subprocess)
                #print(args)
                #os.remove(os.path.join(self.dir, "temp.md"))
            except:
                print(subprocess)
                print(args)

        writeExamOrKey(isKey=True, outfilename_possibly_with_KEY = outfilename.replace("\.docx", "") + "_KEY" + ".docx", dir=self.dir)
