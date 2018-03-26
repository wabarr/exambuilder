## run this code from a python3 shell started from the root exambuilder directory

from exambuilder.Exam import Exam

test = Exam(dir = "/Path/To/exambuilder/example/", examYAML = "Exam.yaml")

test.make_versions("BaseFilenameForVersions", n=2, shuffle_answers=False)