from __future__ import division
import os, sys
import json
import yaml
import csv
from numpy import array
import numpy as np
import json_to_csv
from sklearn import svm

def classify():
    #rosamericads = ['cla', 'hip', 'pop', 'roc', 'rhy', 'jaz', 'spe', 'dan']
    rosamericads = ['cla', 'hip', 'pop', 'roc','jaz']
    #gtzands =  ['cla', 'hip', 'pop', 'roc', 'reg', 'cou', 'met', 'jaz', 'blu', 'dis']
    gtzands = ['cla', 'hip', 'pop', 'roc', 'jaz']
    for root, dirs, files in os.walk('./newmodels/augmenteddataset/genre_tzanetakis/audio/22kmono'):
        for f in files:
            if root[-3:] not in gtzands:
                #output = './lowlevel/output/gtzan/%s' %(f.strip('.wav'))
                output = './newmodels/augmenteddataset/genre_tzanetakis/metadata/lowlevel/%s/%s' % (root[-3:], f.replace('.wav', ''))
                input = root+'/'+f
                #lowleveldata(input, output)
    for root, dirs, files in os.walk('./newmodels/augmenteddataset/genre_rosamerica/audio/mp3'):
        for f in files:
            #output = './lowlevel/output/rosamerica/%s' %(f.strip('.mp3'))
            output = './newmodels/augmenteddataset/genre_rosamerica/metadata/lowlevel/%s/%s' % (root[-3:], f.replace('.mp3', ''))
            input = root+'/'+f
            #lowleveldata(input, output)
    for root, dirs, files in os.walk('./newmodels/augmenteddataset/genre_rosamerica/metadata/lowlevel'):
        for f in files:
            output = './newmodels/augmenteddataset/genre_rosamerica/metadata/highlevel/%s/%s' %(root[-3:], f)
            input = root+'/'+f
            #print input
            #highleveldata(input, output, profile=True)

    for root, dirs, files in os.walk('./newmodels/datasets/genre_tzanetakis/metadata/lowlevel'):
        for f in files:
            if('.DS_Store' not in f):
                if('.sig' not in f):
                    output = './newmodels/datasets/genre_tzanetakis/metadata/jsontocsv/%s/%s.csv' % (root[-3:], f)
                    input = root+'/'+f
                    toignore = '*dmean* *dvar* *metadata.* *.min* *.max* *.cov* *tonal.thpcp* *lowlevel.spectral_energyband_high.* *lowlevel.silence_rate*'
                    command = './json_to_csv.py -i %s -o %s --ignore %s' %(input, output, toignore)
                    #os.system('{} {}'.format('python', command))

    for root, dirs, files in os.walk('./newmodels/datasets/genre_tzanetakis/metadata/jsontocsv'):
        for f in files:
            if ('.DS_Store' not in f):
                filepath = root+'/'+f
                fi = open(filepath)
                csv_f = csv.reader(fi)
                rownumber = 0
                for row in csv_f:
                    #if rownumber==1:
                        #featf = open(root+'/'+root[-3:]+'feature', "w+")
                        #str = ''.join(row)
                        #featf.write(str + "\n")
                    rownumber +=1


    for root, dirs, files in os.walk('./lowlevel/output/gtzan'):
        for f in files:
            output = './highlevel/output/gtzan/%s' %(f)
            input = root+'/'+f
            #highleveldata(input, output, profile=True)

        inputfile = '/Users/Vibhor/Documents/AcademicsAndCV/UPF/MIR/newmodels/datasets/genre_tzanetakis/metadata/filelist_jsontoyaml.yaml'
        #json_to_yaml(inputfile, 'gtzanresult')

    evaluate()
        #svmclassify()

def svmclassify():
    x = []
    y = []
    for root, dirs, files in os.walk('./newmodels/datasets/genre_tzanetakis/metadata/jsontocsv'):
        for f in files:
            if ('.DS_Store' not in f):
                if '.csv' in f:
                    filepath = root+'/'+f
                    fi = open(filepath)
                    csv_f = csv.reader(fi)
                    rownumber = 0
                    for row in csv_f:
                        if rownumber==1:
                            row = enumerateval(row)
                            a = array(row)
                            print f
                            print 'Size of the arrays are: ', a.size
                            x.append(a)
                            gen = enumerategenre(root[-3:])
                            y.append(gen)
                        rownumber +=1
    X = array(x)
    Y = array(y)
    trainsvm(X, Y)

def trainsvm(X, Y):
    a = [[0, 0], [1, 1]]
    b = [0, 1]
    clf = svm.SVC()
    clf.fit(X, Y)


def enumerategenre(genre):
    dictkey = {'blu': 1,
               'cla': 2,
               'roc': 3,
               'cou': 4,
               'hip': 5,
               'pop': 6,
               'jaz': 7,
               'met': 8,
               'reg': 9,
               'dis': 10,
               }
    return int(dictkey[genre])


def enumerateval(row):
    dictkey = {'C': 1,
               'C#': 2,
               'D': 3,
               'D#': 4,
               'E': 5,
               'F': 6,
               'F#': 7,
               'G': 8,
               'G#': 9,
               'A': 10,
               'A#': 11,
               'B': 12,
               }
    dictchord = {'minor': 1,
                 'major':2,
                 }
    for n, i in enumerate(row):
        if i in dictkey:
            row[n] = int(dictkey[i])
        if i in dictchord:
            row[n] = int(dictchord[i])

    return row


def json_to_yaml(input, output):
    command = '/Users/Vibhor/acousticbrainz-server/gaia/src/bindings/pygaia/scripts/classification/json_to_sig.py %s %s' % (input, output)
    #os.system(command)
    os.system('{} {}'.format('python', command))


def evaluate():
    estgenredict = {'pop': 0,
                    'cla': 0,
                    'roc': 0,
                    'hip': 0,
                    'spe': 0,
                    'jaz': 0,
                    'dan': 0,
                    'rhy': 0,
                      }
    confmatrix = {'blu': estgenredict.copy(),
                  'cla': estgenredict.copy(),
                  'met': estgenredict.copy(),
                  'roc': estgenredict.copy(),
                  'hip': estgenredict.copy(),
                  'pop': estgenredict.copy(),
                  'jaz': estgenredict.copy(),
                  'dis': estgenredict.copy(),
                  'cou': estgenredict.copy(),
                  'reg': estgenredict.copy(),
                  }
    for root, dirs, files in os.walk('./newmodels/augmenteddataset/genre_tzanetakis/metadata/highlevel'):
        for f in files:
            if '.DS_Store' not in f:
                filepath = os.path.join(root, f)
                with open(filepath) as data_file:
                    data = json.load(data_file)
                estimatedgenre = json.dumps(data['highlevel']['genre_rosamerica']['value'])
                confmatrix[root[-3:]][estimatedgenre.strip('"')] +=1
    sumall = 0
    correct = 0
    for key1 in confmatrix:
        if key1 in confmatrix[key1]:
            print key1
            print sum(confmatrix[key1].values())
            sumall += sum(confmatrix[key1].values())

    for key1 in confmatrix:
        if key1 in confmatrix[key1]:
            correct += confmatrix[key1][key1]

    print 'sumall:', sumall
    print 'correct: ', correct

    print 'Accuracy for Rosamerica dataset: ', correct/sumall


    print 'Genre estimation for GTZAN dataset using rosamerica classification file'
    for key1 in confmatrix:
        sumofgen = sum(confmatrix[key1].values())
        for key2 in confmatrix[key1]:
            if sumofgen is not 0:
                confmatrix[key1][key2] = confmatrix[key1][key2]/sumofgen


    for key in confmatrix:
        print key
        print confmatrix[key]
        print

    estgenredict = {'blu': 0,
                    'cla': 0,
                    'met': 0,
                    'roc': 0,
                    'hip': 0,
                    'pop': 0,
                    'jaz': 0,
                    'dis': 0,
                    'cou': 0,
                    'reg': 0,
                    }

    confmatrix = {'pop': estgenredict.copy(),
                  'cla': estgenredict.copy(),
                  'roc': estgenredict.copy(),
                  'hip': estgenredict.copy(),
                  'spe': estgenredict.copy(),
                  'jaz': estgenredict.copy(),
                  'dan': estgenredict.copy(),
                  'rhy': estgenredict.copy(),
                  }

    for root, dirs, files in os.walk('./newmodels/augmenteddataset/genre_rosamerica/metadata/highlevel'):
        for f in files:
            if '.DS_Store' not in f:
                filepath = os.path.join(root, f)
                with open(filepath) as data_file:
                    data = json.load(data_file)
                estimatedgenre = json.dumps(data['highlevel']['genre_tzanetakis']['value'])
                confmatrix[root[-3:]][estimatedgenre.strip('"')] +=1

    sumall = 0
    correct = 0
    for key1 in confmatrix:
        if key1 in confmatrix[key1]:
            sumall += sum(confmatrix[key1].values())
    for key1 in confmatrix:
        if key1 in confmatrix[key1]:
            correct += confmatrix[key1][key1]

    print 'sumall:', sumall
    print 'correct: ', correct

    print 'Accuracy for GTZAN dataset: ', correct / sumall

    for key1 in confmatrix:
        sumofgen = sum(confmatrix[key1].values())
        for key2 in confmatrix[key1]:
            if sumofgen is not 0:
                confmatrix[key1][key2] = confmatrix[key1][key2] / sumofgen


    print 'Genre estimation for rosamerica dataset using GTZAN classification file'
    for key in confmatrix:
        print key
        print confmatrix[key]
        print


def lowleveldata(inputfile, outputfile, profile=False):
    profilepath = ""
    if profile:
        profilepath = './lowlevel/profile'
    command = './lowlevel/streaming_extractor_music %s %s %s' %(inputfile, outputfile, profilepath)
    print command
    os.system(command)

def highleveldata(inpufile, outputfile, profile):
    profilepath = ""
    if profile:
        profilepath = './profile'
    command = './highlevel/essentia_streaming_extractor_music_svm %s %s %s' %(inpufile, outputfile, profilepath)
    os.system(command)

if __name__ == "__main__":
    classify()