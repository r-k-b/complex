#!/usr/bin/env python
import numpy as np 
import random
import sys
from itertools import chain, izip, repeat, islice
#globals
testfile = open(sys.argv[1],'w+')
testrunner = open(sys.argv[2],'w+')

#helper functinos



def intersperse(delimiter, seq):
    return list(islice(chain.from_iterable(izip(repeat(delimiter), seq)), 1, None))


def argstring(listofargs):
    return ' '.join(intersperse(' ',map(str,listofargs)))

#write a test 
def test_write(name,elm_function, args, result ):
    print("{0} : Test\n{0} = test \"{0}\" (assert ((Basics.abs ((Complex.abs ({1} {2})) - (Complex.abs ({3})))) < 0.001))".format(name,elm_function,argstring(args),result))
    return(name)

def suite_write(name, nargs, nruns, elm_function, arg_gen, result_gen, type_transform):
    #names = map(lambda x: name + str(x), range(0,nruns))
    args_gen = lambda x: map(lambda x: arg_gen(-1000,1000), range(0,nargs))
    tnames = []
    for x in range(0,nruns):
        tname = name + str(x)
        py_args = args_gen(0)
        py_result = result_gen(*py_args)
        result = type_transform(py_result)
        args = map(type_transform,py_args)
        tnames.append(test_write(tname,elm_function,args,result))
    print("{0} : Test\n{0} = suite \"{0}\" {1}".format(name,tnames).replace('\'',''))
    return name


def testfile_write(names,nargss,nrunss,elm_functions,args_gens,result_gens,type_transforms,headers):
    print("module Tests where")
    for x in headers:
        print(x)
    all_tests = []
    for x in range(0,len(names)):
        all_tests.append(suite_write(names[x],nargss[x],nrunss[x],elm_functions[x],args_gens[x],result_gens[x],type_transforms[x]))

    print("allTests : Test\nallTests = suite \"All testing suites\" {0}".format(all_tests).replace('\'',''))



names = []
nargss = []
nrunss = []
elm_functions = []
args_gens = []
result_gens = []
type_transforms = []
headers = []

headers.append("import Complex")
headers.append("import ElmTest exposing (..)")

testRunnerScript = """
module Main where
--https://github.com/Bogdanp/elm-combine/blob/2.0.1/tests/TestRunner.elm testing structure
import ElmTest exposing (consoleRunner)
import Console exposing (IO, run)
import Task

import Tests


console : IO ()
console = consoleRunner Tests.allTests

port runner : Signal (Task.Task x ())
port runner = run console
"""

def run():
    temp = sys.stdout
    sys.stdout = testfile
    testfile_write(names,nargss,nrunss,elm_functions,args_gens,result_gens,type_transforms,headers)
    testfile.close()
    sys.stdout = testrunner
    print(testRunnerScript)
    testrunner.close()
    sys.stdout = temp
    


def random_complex(min,max):
    return np.complex(random.uniform(min,max),random.uniform(min,max))

def c_to_elm_type(c):
    return("(Complex.complex {0} {1})".format(np.real(c),np.imag(c)))



def add_unary_complex(name,runs,elm_function,result_gen):
    names.append(name)
    nargss.append(1)
    nrunss.append(runs)
    elm_functions.append(elm_function)
    args_gens.append(random_complex)
    result_gens.append(result_gen)
    type_transforms.append(c_to_elm_type)


def add_binary_complex(name,runs,elm_function,result_gen):
    names.append(name)
    nargss.append(2)
    nrunss.append(runs)
    elm_functions.append(elm_function)
    args_gens.append(random_complex)
    result_gens.append(result_gen)
    type_transforms.append(c_to_elm_type)


def cmult(a,b):
    return(a*b)

add_binary_complex("complex_mult",200,"Complex.mult",cmult)
add_unary_complex("complex_abs",200,"Complex.fromReal <| Complex.abs",np.abs)

run()
