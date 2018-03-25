## exambuilder - a `pandoc` bases solution for creating multiple exam versions

Simple python class that parses a YAML config file containing multiple choice or fill-in exam quesions and produces multiple versions of `.docx` exam files with randomized question order.

### Dependencies

*   Python 3.6 
    *  PyYAML
*   recent version of [`pandoc`](https://pandoc.org/) in search path

### Usage

There is an example project in the `example/` folder in this repo. Below is a partial example. 

    from exambuilder.Exam import Exam
    test = Exam(dir = "/Path/To/exambuilder/example/", examYAML = "Exam.yaml")
    test.make_multiple_versions("BaseFilenameForVersions", n=4)

The `dir` argument expects a full file path (no relative paths) where all the associated exam files will be placed. If this directory doesn't exist you will get an error. 

The `examYAML` argument points to the YAML file containing a title, the instructions for the exam, and exam questions. This file must be located within `dir`. Here is a basic example of this YAML file:

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

The `make_multiple_versions()` method has a positional argument which provides the base filename for all versions that will be produced. 

The value for the `n` argument determines how many versions will be created.  All versions and grading keys are saved in `dir`

### Styles

If a file named `reference.docx` exists in `dir` then the styles in this document will be applied to the output files.  Read more on the `pandoc` documentation for details on how this works. 

### Images

There is rudimentary support for images. Just include a relative file path in the `image` block in your YAML file for the question you want to provide an image for.  This file is expected to be found in an `images/` subdirectory of `dir`, and will produce an error if not found. The image will be included before the associated question in the resulting document. 

