*Last Update: 2016-02-24*

# Duplitector

Duplitector is a command line duplicate files detection and removal tool.

Duplitector is written in Python 2.7, so you must have python installed.

## How to use it

Simply clone the project and run duplitector using the python interpreter providing a filesystem path to it:

    git clone https://github.com/erickthered/duplicate-files-remover.git
    cd duplicate-files-remover
    python duplitector.py <path>

The program will report what duplicate files it finds and how much space is being used by them.

Depending on the number of duplicated files you may want to save the output to a report file, in such cases you can use a command like this:

    python duplitector.py <path> > report.txt

This will save the program output to a file named *report.txt*.

## Autodelete files

If you want to automatically delete duplicated files from the filesystem you must specifiy the *--delete* flag as the first parameter:

	python duplitector.py --delete <path>

The output of the program will show you what files the program deleted and how much disk space was freed.

## License

Duplitector is released under the terms of the MIT License. See licence.txt for
details.

## Coding Standard

Duplitector adheres to the [PEP8 Standard](https://www.python.org/dev/peps/pep-0008/)