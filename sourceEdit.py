"""
Author: Chen Zhang (demi6od) <demi6d@gmail.com>
Date: 2013 Oct 21st
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import sys
import re
import argparse

def conToWriteIE(inFileName, outFileName):
    print '[+] Change console ' + inFileName + ' to writeIE ' + outFileName
    
    inFile = open(inFileName, 'r')
    src = inFile.read()
    outFile = open(outFileName, 'wb+')

    src = src.replace('console.log(', 'writeFileIE("e://fuzzlog.txt",')
    src = src.replace('Fuzz start\'', 'Fuzz start\', true')
    src = src.replace('IS_IE = false', 'IS_IE = true')
    src = src.replace('IS_IE = false', 'IS_DEBUG = true')

    outFile.write(src)
    inFile.close()
    outFile.close()

def conToWrite(inFileName, outFileName):
    print '[+] Change console ' + inFileName + ' to write ' + outFileName
    
    inFile = open(inFileName, 'r')
    src = inFile.read()
    outFile = open(outFileName, 'wb+')

    src = src.replace('console.log(', 'writeFileCM("fuzzlog",')
    src = src.replace('Fuzz finished\'', 'Fuzz finished\', true')

    outFile.write(src)
    inFile.close()
    outFile.close()

def conToLog(inFileName, outFileName):
    print '[+] Change console ' + inFileName + ' to log ' + outFileName
    
    inFile = open(inFileName, 'r')
    src = inFile.read()
    outFile = open(outFileName, 'wb+')

    src = re.sub(r' console(.*?\s*?.*?)\); *$', lambda m: ' logger' + m.group(1) + ', \'grind\', 1);', src, 0, re.M)
    src = re.sub(r'\(\'console(.*?\s*.*?)\);console(.*?{")\);', lambda m: '(\'logger' + m.group(1) \
        + ', "grind", 1);logger' + m.group(2) + ', "grind", 1);', src)

    src = re.sub(r'// (logger = new LOGGER)', lambda m: m.group(1), src)
    src = re.sub(r'// (logger\.starting)', lambda m: m.group(1), src)
    src = re.sub(r'// (logger\.finished)', lambda m: m.group(1), src)
    src = re.sub(r'// (window.location.href = window.location.protocol)', lambda m: m.group(1), src)
    src = re.sub(r'// (setTimeout\("window.location.href = window.location.protocol)', lambda m: m.group(1), src)
    src = re.sub(r'// (gc\(\))', lambda m: m.group(1), src)

    outFile.write(src)
    inFile.close()
    outFile.close()

def logToCon(inFileName, outFileName):
    print '[+] Change log ' + inFileName + ' to console ' + outFileName

    inFile = open(inFileName, 'r')
    src = inFile.read()
    outFile = open(outFileName, 'wb+')

    src = re.sub(r' logger(\.log\(.*?\s*?.*?), \'grind\', 1\); *$', lambda m: ' console' + m.group(1) + ');', src, 0, re.M)
    src = re.sub(r'\(\'logger(.*?\s*.*?), "grind", 1\);logger(.*?), "grind", 1\);', \
        lambda m: '(\'console' + m.group(1) + ');console' + m.group(2) + ');', src)

    src = re.sub(r' logger = new LOGGER', lambda m: ' //' + m.group(0), src)
    src = re.sub(r' logger\.starting', lambda m: ' //' + m.group(0), src)
    src = re.sub(r' logger\.finished', lambda m: ' //' + m.group(0), src)
    src = re.sub(r' window.location.href = window.location.protocol', lambda m: ' //' + m.group(0), src)
    src = re.sub(r' setTimeout("window.location.href = window.location.protocol', lambda m: ' //' + m.group(0), src)
    src = re.sub(r' gc\(\)', lambda m: ' //' + m.group(0), src)

    outFile.write(src)
    inFile.close()
    outFile.close()

def genLog(logType, version):
    inFile = open('demichromelog' + version + '.js', 'r')
    src = inFile.read()
    inFile.close()
    inFile = open('helplog.js', 'r')
    src += inFile.read()
    inFile.close()
    inFile = open('dict.js', 'r')
    src += inFile.read()
    inFile.close()
    inFile = open('logging.js', 'r')
    src += inFile.read()
    inFile.close()
    inFile = open('propdic.js', 'r')
    src += inFile.read()
    inFile.close()
    inFile = open('funcdic.js', 'r')
    src += inFile.read()
    inFile.close()
    inFile = open('styledic.js', 'r')
    src += inFile.read()

    if logType == '2':
        print '[+] Generate logging_grinder file, version ' + version

        outFile = open('logging_grinder v' + version + '.js', 'wb+')

        # IE
        print '[+] Generate logging_grinder_ie file, version ' + version
        srcIE = src.replace('IS_IE = false', 'IS_IE = true')
        srcIE = srcIE.replace('e.message', '""')
        srcIE = srcIE.replace('window.location.protocol + "//" + window.location.host + "/grinder"', '"http://127.0.0.1:8080/grinder"')

        outFileIE = open('logging_grinder_ie v' + version + '.js', 'wb+')
        outFileIE.write(srcIE)
        outFileIE.close()
    elif logType == '3':
        print '[+] Generate logging_grinder_crash file, version ' + version

        src = src.replace('window.location.href', 'testcase();//')
        src = src.replace('function clearAll() {', 'function clearAll() {return;')
        outFile = open('logging_grinder_crash v' + version + '.js', 'wb+')

    outFile.write(src)
    inFile.close()
    outFile.close()

def genBlackList(version):
    print '[+] Generate func black list'

    inFile = open('demichrome' + version + '.js', 'r')
    src = inFile.read()
    inFile.close()
    inFile = open('help.js', 'r')
    src += inFile.read()
    inFile.close()
    inFile = open('dict.js', 'r')
    src += inFile.read()
    inFile.close()
    inFile = open('logging.js', 'r')
    src += inFile.read()
    inFile.close()
    inFile = open('propdic.js', 'r')
    src += inFile.read()
    inFile.close()
    inFile = open('funcdic.js', 'r')
    funcDic = inFile.read()
    src += funcDic
    inFile.close()
    inFile = open('styledic.js', 'r')
    src += inFile.read()
    inFile.close()
    inFile = open('testcase.js', 'r')
    src += inFile.read()

    outFile = open('funcdic.js', 'wb+')

    funcList = re.findall(r'function (\w+)\(', src)
    funcList.append('testcase')
    funcList.append('testCase')
    blackList = "    "
    count = 0

    for func in funcList:
        count += 1
        if count % 6 == 0:
            blackList += '\n    '
        blackList += "'" + func + "', "

    src = re.sub(r'(// Auto func black list begin).*(// Auto func black list end)', \
        lambda m: m.group(1) + '\n' + blackList + '\n    ' + m.group(2), funcDic, 0 ,re.S)

    outFile.write(src)
    inFile.close()
    outFile.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help = 'inputFile')
    parser.add_argument('-o', help = 'outputFile')
    parser.add_argument('-v', help = 'demichrome version')
    parser.add_argument('-t', help = 'type: 0 - console to log, 1 - log to console, 2 - generate logging_grinder, '
        '3 - generate logging_grinder_crash, 4 - generate func black list, 5 - auto generate all')
    args = parser.parse_args()

    print "[+] Start"

    if args.t == '0':
        conToLog(args.i, args.o)
    elif args.t == '1':
        logToCon(args.i, args.o)
    elif args.t == '2' or args.t == '3':
        genLog(args.t, args.v)
    elif args.t == '4':
        genBlackList(args.v)
    elif args.t == '5':
        genBlackList(args.v)
        conToLog('demichrome' + args.v + '.js', 'demichromelog' + args.v + '.js')
        conToWrite('demichrome' + args.v + '.js', 'demichromewrite' + args.v + '.js')
        conToWriteIE('demichrome' + args.v + '.js', 'demichromewriteIE' + args.v + '.js')
        conToLog('help.js', 'helplog.js')
        genLog('2', args.v)
        genLog('3', args.v)

    print "[+] Finish"

if __name__ == "__main__":
    main()

#id[setEvtId][rEvt] = new Function('logger.log("//id_' + setEvtId + '[\'' + rEvt + '\'] = function()", "grind", 1);logger.log("/-{", "grind", 1);eventHandler();');
#logger.log('// Error: propMan: ' + e.message, 'grind', 1);

