from __future__ import division

__author__ = "Martin Potthast"
__email__ = "martin.potthast at uni-weimar dot de"
__version__ = "1.3"
__all__ = ["macro_avg_recall_and_precision", "micro_avg_recall_and_precision",
           "granularity", "plagdet_score", "Annotation"]

from collections import namedtuple
import getopt
import glob
import math
# from numpy import int8 as npint8
# from numpy.ma import zeros, sum as npsum
import os
import sys
import unittest
import xml.dom.minidom
import csv
from random import randint

TREF, TOFF, TLEN = 'this_reference', 'this_offset', 'this_length'
SREF, SOFF, SLEN = 'source_reference', 'source_offset', 'source_length'
EXT = 'is_external'
Annotation = namedtuple('Annotation', [TREF, TOFF, TLEN, SREF, SOFF, SLEN, EXT])
TREF, TOFF, TLEN, SREF, SOFF, SLEN, EXT = range(7)

NO_PLAGIARISM_CLASS = 0
DIRECT_PLAGIARISM_CLASS = 1
OBFUSCATED_PLAGIARISM_CLASS = 2

def getPlagiarismClassNameByClassId(classId):
    switcher = {
        NO_PLAGIARISM_CLASS: "NoPlagiarism",
        DIRECT_PLAGIARISM_CLASS: "DirectPlagiarism",
        OBFUSCATED_PLAGIARISM_CLASS: "ObfuscatedPlagiarism"
    }
    return switcher.get(classId, "Unknown")

def index_annotations(annotations, xref=TREF):
    """Returns an inverted index that maps references to annotation lists."""
    index = dict()
    for ann in annotations:
        index.setdefault(ann[xref], []).append(ann)
    return index


def extract_annotations_from_files(path, tagname):
    """Returns a set of plagiarism annotations from XML files below path."""
    if not os.path.exists(path):
        print "Path not accessible:", path
        sys.exit(2) 
    annotations = set()
    xmlfiles = glob.glob(os.path.join(path, '*.xml'))
    xmlfiles.extend(glob.glob(os.path.join(path, os.path.join('*', '*.xml'))))
    for xmlfile in xmlfiles:
        annotations.update(extract_annotations_from_file(xmlfile, tagname))
    return annotations


def extract_annotations_from_file(xmlfile, tagname):
    """Returns a set of plagiarism annotations from an XML file."""
    doc = xml.dom.minidom.parse(xmlfile)
    annotations = set()
    if not doc.documentElement.hasAttribute('reference'):
        return annotations
    t_ref = doc.documentElement.getAttribute('reference')
    for node in doc.documentElement.childNodes:
        if node.nodeType == xml.dom.Node.ELEMENT_NODE and \
           node.hasAttribute('name') and \
           node.getAttribute('name').endswith(tagname):
            ann = extract_annotation_from_node(node, t_ref)
            if ann:
                annotations.add(ann)
    return annotations


def extract_annotation_from_node(xmlnode, t_ref):
    """Returns a plagiarism annotation from an XML feature tag node."""
    if not (xmlnode.hasAttribute('this_offset') and \
            xmlnode.hasAttribute('this_length')):
        return False
    t_off = int(xmlnode.getAttribute('this_offset'))
    t_len = int(xmlnode.getAttribute('this_length'))
    s_ref, s_off, s_len, ext = '', 0, 0, False
    if xmlnode.hasAttribute('source_reference') and \
       xmlnode.hasAttribute('source_offset') and \
       xmlnode.hasAttribute('source_length'):
        s_ref = xmlnode.getAttribute('source_reference')
        s_off = int(xmlnode.getAttribute('source_offset'))
        s_len = int(xmlnode.getAttribute('source_length'))
        ext = True
    return Annotation(t_ref, t_off, t_len, s_ref, s_off, s_len, ext)

def extract_random_excerpts_from_pair_files(no_plag_path):
    annotations = set()
    with open(os.path.join(no_plag_path,"pairs"), 'r') as file_of_pairs_files:
        for line in file_of_pairs_files:
            suspicious_file_name, source_file_name = line.split()
            source_file = open(
                os.path.join("C:/plagiarism_detector_files_base/texts/src",source_file_name),
                'r')
            source_length = sum(len(line) for line in source_file)
            if(source_length < 500):
                source_excerpt_length = source_length
                source_excerpt_offset = 0
            else:
                source_excerpt_length = 500
                source_excerpt_offset = randint(0, source_length - source_excerpt_length)
            suspicious_file = open(
                os.path.join("C:/plagiarism_detector_files_base/texts/susp",suspicious_file_name),
                'r')
            suspicious_length = sum(len(line) for line in suspicious_file)
            if(suspicious_length < 500):
                suspicious_excerpt_length = suspicious_length
                suspicious_excerpt_offset = 0
            else:
                suspicious_excerpt_length = 500
                suspicious_excerpt_offset = randint(0, suspicious_length - suspicious_excerpt_length)
            external = True
            annotations.add(
                Annotation(suspicious_file_name, suspicious_excerpt_offset, 
                    suspicious_excerpt_length, source_file_name, source_excerpt_offset, 
                    source_excerpt_length, external))
    return annotations

class Excerpt():
    locationOfFile = ""
    offsetFromBegin = 0
    length = 0
    text = ""

    def __init__(self, _locationOfFile, _offsetFromBegin, _length, _text):
        self.locationOfFile = _locationOfFile 
        self.offsetFromBegin = _offsetFromBegin
        self.length = _length
        self.text = _text

class AnnotationEvidence():
    plagiarismClass = None
    excerptSuspicious = None
    excerptSource = None

    def ConvertAnnotationToAnnotationEvidence(self, annotation, _plagiarismClass):
        locationSuspicious = annotation[TREF]
        lengthSuspicious = annotation[TLEN]
        offsetSuspicious = annotation[TOFF]
        locationSource = annotation[SREF]
        lengthSource = annotation[SLEN]
        offsetSource = annotation[SOFF]
        fileSourceContent = ""
        with open(
            os.path.join("C:/plagiarism_detector_files_base/texts/src",locationSource),
            'r') as file:
            file.read(offsetSource)
            fileSourceContent = file.read(lengthSource)
        fileSuspiciousContent = ""
        with open(
            os.path.join("C:/plagiarism_detector_files_base/texts/susp",locationSuspicious),
            'r') as file:
            file.read(offsetSuspicious)
            fileSuspiciousContent = file.read(lengthSuspicious)
        self.excerptSuspicious = Excerpt(
            _locationOfFile = locationSuspicious,
            _offsetFromBegin = offsetSuspicious,
            _length = lengthSuspicious,
            _text = fileSuspiciousContent)
        self.excerptSource = Excerpt(
            _locationOfFile = locationSource,
            _offsetFromBegin = offsetSource,
            _length = lengthSource,
            _text = fileSourceContent)
        self.plagiarismClass = _plagiarismClass

    def toLinearObject(self):
        plagiarismClassName = getPlagiarismClassNameByClassId(self.plagiarismClass)
        
        return [
            self.plagiarismClass,
            plagiarismClassName,
            self.excerptSource.offsetFromBegin,
            self.excerptSource.length,
            self.excerptSource.text.replace("\n"," ").replace("\r"," "),
            self.excerptSource.locationOfFile,
            self.excerptSuspicious.offsetFromBegin,
            self.excerptSuspicious.length,
            self.excerptSuspicious.text.replace("\n"," ").replace("\r"," "),
            self.excerptSuspicious.locationOfFile
        ]
        

def ConvertAnnotationsToAnnotationEvidenceList(annotations, plagiarismClass):
    annotationEvidenceList = []
    for annotation in annotations:
        annotationEvidence = AnnotationEvidence()
        annotationEvidence.ConvertAnnotationToAnnotationEvidence(annotation, plagiarismClass)
        annotationEvidenceList.append(annotationEvidence)
    return annotationEvidenceList

class TestPerfMeasures(unittest.TestCase):
    """Unit tests for the plagiarism detection performance measures."""
    
    ann1 = Annotation('tref1', 0, 100, 'sref1', 0, 100, True)
    ann2 = Annotation('tref1', 0, 100, '', 0, 0, False)
    ann3 = Annotation('tref1', 100, 100, 'sref1', 100, 100, True)
    ann4 = Annotation('tref1', 0, 200, 'sref1', 0, 200, True)
    ann5 = Annotation('tref1', 0, 1, 'sref1', 0, 1, True)
    ann6 = Annotation('tref1', 99, 1, 'sref1', 99, 1, True)
    ann7 = Annotation('tref2', 0, 100, 'sref2', 0, 100, True)
    ann8 = Annotation('tref2', 0, 100, '', 0, 0, False)
    ann9 = Annotation('tref2', 50, 100, 'sref2', 50, 100, True)
    ann10 = Annotation('tref2', 25, 75, 'sref2', 25, 75, True)
    
    def test_index_annotations(self):
        index = index_annotations([self.ann1, self.ann7, self.ann2, self.ann8])
        self.assertEqual([self.ann1, self.ann2], index.get('tref1'))
        self.assertEqual([self.ann7, self.ann8], index.get('tref2'))


def usage():
    """Prints command line usage manual."""
    print """\
Usage: perfmeasures.py [options]

Options:
  -p, --plag-path  Path to the XML files with plagiarism annotations
  -n, --no-plag-path  Path to the PAIRS file with no-plagiarism list of files
  -o, --obfuscated-plag-path  Path to the XML file with obfuscated-plagiarism annotations
  -h, --help       Show this message
"""


def parse_options():
    """Parses the command line options."""
    try:
        long_options = ["plag-path=", "no-plag-path=", "obfuscated-plag-path=", "help"]
        opts, _ = getopt.getopt(sys.argv[1:], "p:n:o:h", long_options)
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    plag_path, no_plag_path, obfuscated_plag_path = "undefined", "undefined", "undefined"
    anyError = False
    for opt, arg in opts:
        if opt in ("-p", "--plag-path"):
            plag_path = arg
        elif opt in ("-n", "--no-plag-path"):
            no_plag_path = arg
        elif opt in ("-o", "--obfuscated-plag-path"):
            obfuscated_plag_path = arg
        elif opt in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            assert False, "Unknown option."
    if plag_path == "undefined":
        print "Plagiarism path undefined. Use option -p or --plag-path."
        anyError = True
    if no_plag_path == "undefined":
        print "No-Plagiarism path is undefined. Use option -n or --no-plag-path."
        anyError = True
    if obfuscated_plag_path == "undefined":
        print "Obfuscated-Plagiarism path is undefined. Use option -o or --obfuscated-plag-path."
        anyError = True
    if anyError:
        sys.exit()        
    return (plag_path, no_plag_path, obfuscated_plag_path)

def main(plag_path, no_plag_path, obfuscated_plag_path):
    """Main method of this module."""        
    print 'Reading reference pairs with direct plagiarism', plag_path
    direct_plagiarism_cases_annotations = extract_annotations_from_files(
        plag_path, tagname='plagiarism')
    print 'Recovering texts referenced'
    cases_with_the_evidences = ConvertAnnotationsToAnnotationEvidenceList(
        annotations = direct_plagiarism_cases_annotations, 
        plagiarismClass = DIRECT_PLAGIARISM_CLASS)
    
    print 'Reading reference pairs with obfuscated plagiarism', obfuscated_plag_path
    obfuscated_plagiarism_cases_annotations = extract_annotations_from_files(
        obfuscated_plag_path, tagname='plagiarism')
    print 'Recovering texts referenced'
    cases_with_the_evidences += ConvertAnnotationsToAnnotationEvidenceList(
        annotations = obfuscated_plagiarism_cases_annotations, 
        plagiarismClass = OBFUSCATED_PLAGIARISM_CLASS)

    print 'Reading reference pairs without plagiarism', no_plag_path
    no_plagiarism_cases_annotations = extract_random_excerpts_from_pair_files(
        no_plag_path)
    print 'Recovering texts referenced'
    cases_with_the_evidences += ConvertAnnotationsToAnnotationEvidenceList(
        annotations = no_plagiarism_cases_annotations, 
        plagiarismClass = NO_PLAGIARISM_CLASS)
    
    csv_object = [ 
        annotationEvidence.toLinearObject() 
        for annotationEvidence in cases_with_the_evidences ]
    with open(
        'C:/plagiarism_detector_files_base/'+'linearRegisters/annotations_evidences.csv',
        'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        fieldnames=[
            "plagiarismClass",
            "plagiarismClassName",
            "excerptSourceOffsetFromBegin",
            "excerptSourceLength",
            "excerptSourceText",
            "excerptSourceLocationOfFile",
            "excerptSuspiciousOffsetFromBegin",
            "excerptSuspiciousLength",
            "excerptSuspiciousText",
            "excerptSuspiciousLocationOfFile"
        ]
        spamwriter.writerow(fieldnames)
        spamwriter.writerows(csv_object)

if __name__ == '__main__':   
    main(*parse_options())


