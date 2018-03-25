## exambuilder

Simple python class that parses a YAML config file containing multiple choice or fill-in exam quesions and produces multiple versions of `.docx` exam files with randomized question order.

### Dependencies

*   Python 3.6 
    *  PyYAML
*   recent version of [`pandoc`](https://pandoc.org/) in search path

### Usage

    from exambuilder.Exam import Exam
    test = Exam(dir ="~/ExamDirectory", examYAML = "Exam.yaml")
    test.make_multiple_versions("BaseFilenameForVersions", n=4)

The `dir` argument provides a directory where all the associated exam files will be placed. If this directory doesn't exist you will get an error. 

The `examYAML` argument points to the YAML file containing the exam questions. Here is a minimal example:

     title: Title For Exam
     instructions: "These instructions apppear below the title, and **can contain markdown formatting**"
     questions:
         - question: This is a fill in the blank question.  You don't need to provide a block of possible answers
           fill_in: True
         - question: This is a multiple choice question.  There is a block of answers.  The correct answer has two asterisks \*\* at the end to mark it as the correct one. 
           image: imagefile.jpg
           answers:
              - Wrong answer, buddy!
              - Keep trying, friend!
              - Still don't have it, amigo!
              - You got it!**

The `make_multiple_versions()` has a positional argument which provides the base filename for all versions that will be produced. 

The value for the `n` argument determines how many versions will be created.  All versions and grading keys are saved in `dir`

### Styles

If a file named `reference.docx` exists in `dir` then the styles in this document will be applied to the output files.  Read more on the `pandoc` documentation for details on how this works. 

### Images

There is rudimentary support for images. Just include a relative file path in the `image` block in your YAML file for the question you want to provide an image for.  This file is expected to be found in an `images/` subdirectory of `dir`, and will produce an error if not found. The image will be included before the associated question in the resulting document. 

