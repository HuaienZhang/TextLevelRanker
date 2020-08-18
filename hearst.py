
from __future__ import print_function
import sys
import os.path, os
import argparse
import nltk
import hp

# these NLTK resources are not automatically included when nltk is
# installed. If they are not found, try downloading them now
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

# default location for data
default_data_dir = "/Users/finin/Projects/ACCL/semeval18/converted_into_text/"

# default file for output
default_output_file = "hearst.out"

# default is use extended Hearsh patterns

def hearstify(source, extended=True):
    # returns iterable of hearst patterns in file or all files in
    # directory (recusively)
    h = hp.HearstPatterns(extended=extended)
    if os.path.isfile(source):
        return hearstify_file(h, source)
    elif os.path.isdir(source):
        return hearstify_directory(h, source)
    else:
        return hearstify_text(h, source)

def hearstify_directory(h, directory):
    results = []
    for dirName, subdirList, fileList in os.walk(directory):
        print(directory, dirName, fileList)
        for fname in fileList:
            # skip files that begin with a dot
            if fname[0] != '.':
                #results.extend(hearstify_file(h, os.path.join(directory, dirName, fname)))
                results.extend(hearstify_file(h, os.path.join(dirName, fname)))
    return results

def hearstify_file(h, infile):
    # returns iterable of hearst patterns in a file
    try:
        print("INFILE=" + str(infile))
        text = open(infile).read()
    except:
        print('Failed when reading file', infile, sys.exc_info()[0])
        return [ ]
    return h.find_hyponyms(text)

def hearstify_text(h, text):
    return h.find_hyponyms(text)    

def hearst_to_file(source, out, extended):
        # if output to file, open it
        if out != sys.stdout:
            out = open(out, 'w')
        if source == 'stdin':
            sys.stdout.write("enter textt, ending with ^D>> ")
            sys.stdout.flush()
            text = sys.stdin.read()
            h = hp.HearstPatterns(extended=extended)
            results = hearstify_text(h, text)
        else:
            results = hearstify(source, extended)
        for sentence, general, specific in results:
            out.write(sentence + "\n")
            out.write('({} | {})\n'.format(general, specific) + "\n")

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Extract hearst pattern pairs from a file or directory of files')
    p.add_argument('source', nargs="?", default='stdin', help='input text file or directory of files')
    p.add_argument('-o', '--outfile', nargs='?', default=sys.stdout, help='file for output, defaults to stdout')
    p.add_argument('-s', '--simple', default=False, action='store_true')
    a = p.parse_args()
    hearst_to_file(a.source, a.outfile, not a.simple)
