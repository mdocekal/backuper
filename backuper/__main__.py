# -*- coding: UTF-8 -*-
""""
Created on 10.01.20
Entry point of application.

:author:     Martin Dočekal
"""
import datetime
from shutil import copyfile
import os
import re
import sys
from argparse import ArgumentParser
from tqdm import tqdm
from windpyutils.logger import Logger
from slugify import slugify

class ArgumentParserError(Exception):
    """
    Exceptions for argument parsing.
    """
    pass


class ExceptionsArgumentParser(ArgumentParser):
    """
    Argument parser that uses exceptions for error handling.
    """

    def error(self, message):
        raise ArgumentParserError(message)


class ArgumentsManager(object):
    """
    Parsers arguments for script.
    """

    @classmethod
    def parseArgs(cls):
        """
        Performs arguments parsing.

        :param cls: arguments class
        :returns: Parsed arguments.
        """
        parser = ExceptionsArgumentParser(description="Tiny tool for fast backup of files.")

        parser.add_argument("-f", "--fromFolder", help="Folder you want to copy from.", type=str,  required=True)
        parser.add_argument("-t", "--toFolder", help="Folder you want to copy to.", type=str, required=True)
        parser.add_argument("--image", help="Backup all images.", action='store_true')
        parser.add_argument("--video", help="Backup all videos.", action='store_true')
        parser.add_argument("--document", help="Backup all documents.", action='store_true')
        parser.add_argument("--audio", help="Backup all audio files.", action='store_true')
        parser.add_argument("--email", help="Backup all e-mail files.", action='store_true')
        parser.add_argument("--database", help="Backup all database/dataset files.", action='store_true')
        parser.add_argument("--compressed", help="Backup all compressed files.", action='store_true')

        parser.add_argument("--fileList", help="Save list of copied files to given file.", type=str)
        parser.add_argument("--skipInvalid",
                            help="By default all problematic file paths for target system are automatically "
                                 "converted, but if you use this they will be skipped.",
                            action='store_true')

        if len(sys.argv) < 2:
            parser.print_help()
            return None
        try:
            parsed = parser.parse_args()

        except ArgumentParserError as e:
            parser.print_help()
            print("\n" + str(e), file=sys.stdout, flush=True)
            return None

        return parsed


def main():
    args = ArgumentsManager.parseArgs()
    if args is None:
        exit(1)

    extensions = {
        "image": {"ai", "bmp", "gif", "ico", "jpg", "jpeg", "png", "ps", "psd", "svg", "tif", "tiff", "3fr",
                   "ari", "sr2", "bay", "cr2", "eip", "kdc", "dng", "erf", "fff", "mef", "mos", "mrw", "nrw",
                   "orf", "pef", "pxn", "R3D", "raf", "rw2", "dng", "rwz", "raw", "rwl", "x3f"},
        "video": {"3g2", "3gp", "avi", "flv", "264", "m4v", "mkv", "mov", "mp4", "mpg", "mpeg", "rm", "swf", "vob", "wmv"},
        "document": {"doc", "docx", "odt", "pdf", "rtf", "tex", "txt", "wpd", "ods", "xls", "xlsm", "xlsx"},
        "email": {"email", "eml", "emlx", "msg", "oft", "ost", "pst", "vcf"},
        "audio": {"aif", "cda", "midi", "mp3", "mpa", "ogg", "wav", "wma", "wpl"},
        "database": {"csv", "dat", "dbf", "log", "mdb", "sql", "tar", "xml"},
        "compressed": {"7z", "arj", "deb", "pkg", "rar", "rpm", "gz", "zip"}
    }

    def log(txt):
        print("{} : INFO : {}".format(datetime.datetime.now(), txt), file=sys.stderr, flush=True)

    Logger().register_observer("LOG", log)

    # select all extensions we will be searching for

    searchExtensions = set()

    for t, ext in extensions.items():
        if getattr(args, t) is True:
            searchExtensions |= ext

    Logger().log("We will be searching all files with extensions: {}".format(", ".join(searchExtensions)))

    rExp = re.compile(".*\.({})$".format("|".join(searchExtensions)), flags=re.IGNORECASE)

    Logger().log("Searching files. This can take a while ...")
    files = []

    for dirPath, _, fileNames in os.walk(args.fromFolder):
        for f in fileNames:
            srcPath = os.path.join(dirPath, f)
            if rExp.match(f) and os.path.exists(srcPath):
                files.append(srcPath)

    Logger().log("I've found {} files.".format(len(files)))

    filesCopyTo = []
    for f in tqdm(files, desc="copying", unit="file"):
        tmpP = f[len(args.fromFolder):]
        if tmpP.startswith(os.sep):
            tmpP = tmpP[len(os.sep):]

        copyTo = os.path.join(args.toFolder, tmpP)
        try:
            os.makedirs(os.path.dirname(copyTo), exist_ok=True)
            copyfile(f, copyTo)
            filesCopyTo.append(copyTo)
        except OSError:
            if not args.skipInvalid:
                tmpP = os.sep.join([slugify(x) for x in tmpP.split(os.sep)])
                copyTo = os.path.join(args.toFolder, tmpP)
                os.makedirs(os.path.dirname(copyTo), exist_ok=True)
                copyfile(f, copyTo)
                filesCopyTo.append(copyTo)
            else:
                filesCopyTo.append(None)

    if args.fileList:
        with open(args.fileList, "w") as listF:
            for f, cp2 in zip(files, filesCopyTo):
                listF.write("\t ".join([os.path.abspath(f), "None" if cp2 is None else os.path.abspath(cp2)]))
                listF.write("\n")


if __name__ == '__main__':
    main()
