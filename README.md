# backuper
Tiny tool for fast backup of files.

## Installation
The recommended approach is just to install the requirements:

    pip install -r requirements.txt
    
and use the:

    run.py
    
Alternatively, you can install the evaluation script as the python console application:

    pip install .
    
and run it with:

    evalhulth2003

## Usage
To copy all files of certain type (images) from a folder F (and all subfolders) to a folder T use:

    
    ./run.py -f F -t T --image
    

The folder structure remains from its origin.

You can also copy multiple types of files at once, let's say video and audio:

    ./run.py -f F -t T --video --audio
    

The type of a file is naively determined only by it's extension. The complete list of extensions for given file type can be
seen in [Types](#types) section.

If you want to see more arguments, please feel free to call:

    ./run.py -h

## Types
There is exhaustive list of all file types and assigned extensions.

* image

    - ai, bmp, gif, ico, jpg, jpeg, png, ps, psd, svg, tif, tiff, 3fr, ari, sr2, bay, cr2, eip, kdc, dng, erf, fff, mef, mos, mrw, nrw,orf, pef, pxn, R3D, raf, rw2, dng, rwz, raw, rwl, x3f

* video

    - 3g2, 3gp, avi, flv, 264, m4v, mkv, mov, mp4, mpg, mpeg, rm, swf, vob, wmv

* document
    - doc, docx, odt, pdf, rtf, tex, txt, wpd, ods, xls, xlsm, xlsx

* email

    - email, eml, emlx, msg, oft, ost, pst, vcf

* audio

    - aif, cda, midi, mp3, mpa, ogg, wav, wma, wpl

* database

    - csv, dat, dbf, log, mdb, sql, tar, xml

* compressed

    - 7z, arj, deb, pkg, rar, rpm, gz, zip