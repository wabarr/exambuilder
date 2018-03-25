## run this code from a python3 shell started from the root exambuilder directory

from exambuilder.Exam import Exam

test = Exam(dir = "/Users/wabarr/PycharmProjects/exambuilder/example/", examYAML = "Exam.yaml")

test.make_multiple_versions("BaseFilenameForVersions", n=4)