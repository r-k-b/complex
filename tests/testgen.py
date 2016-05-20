#!/usr/bin/env python
import numpy as np 
#np.set_printoptions(precision=32)
#np.set_printoptions(formatter={'float': lambda x: "{0:0.32f}".format(x)})

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
    print("{0} : Test\n{0} = test \"{0}\" (assert ((Basics.abs ((Complex.abs ({1} {2})) - (Complex.abs ({3})))) < 0.0001))".format(name,elm_function,argstring(args),result))
    return(name)

def suite_write(name, nargs, nruns, elm_function, arg_gen, result_gen, type_transform):
    #names = map(lambda x: name + str(x), range(0,nruns))
    args_gen = lambda x: map(lambda x: arg_gen(-10,10), range(0,nargs))
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
    print("module Tests exposing (allTests)")
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
-- https://github.com/elm-community/elm-test/tree/1.1.0#running-tests
import ElmTest exposing (runSuite)

import Tests

main =
    runSuite Tests.allTests
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
    a = ("{%0.32f}"%np.real(c)).replace('{','').replace('}','')
    b = ("{%0.32f}"%np.imag(c)).replace('{','').replace('}','')
    return("(Complex.complex {0} {1})".format(a,b))



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

def realsin(a):
    return (np.sin(np.real(a)))

def multlog(a,b):
    return(b*np.log(a))

def newexp(a,b):
    return(np.exp(b*np.log(a)))

add_binary_complex("complex_mult",200,"Complex.mult",cmult)
add_binary_complex("complex_div",200,"Complex.div",lambda x,y: x/y)
add_unary_complex("complex_abs",200,"Complex.fromReal <| Complex.abs",np.abs)
add_unary_complex("complex_sign",200,"Complex.fromReal <| Complex.sgn",np.sign)
add_unary_complex("complex_sqrt",200,"Complex.sqrt",np.sqrt)
add_unary_complex("complex_arg",200,"Complex.fromReal <| Complex.arg",np.angle)
add_unary_complex("complex_ln",200," Complex.ln",np.log)
add_unary_complex("complex_exp",200,"Complex.exp",np.exp)
add_binary_complex("complex_pow",200,"Complex.pow",np.power)
add_unary_complex("complex_cos",200,"Complex.cos",np.cos)
add_unary_complex("complex_sin",200,"Complex.sin",np.sin)
add_unary_complex("complex_tan",200,"Complex.tan",np.tan)
add_unary_complex("complex_asin",200,"Complex.asin",np.arcsin)
add_unary_complex("complex_acos",200,"Complex.acos",np.arccos)
add_unary_complex("complex_atan",200,"Complex.atan",np.arctan)
#add_binary_complex("complex_mult_log",200,"(\z w -> Complex.mult w (Complex.ln z))",multlog )
#add_binary_complex("new_pow",200,"Complex.pow",newexp)
#add_unary_complex("realsine", 1000, "Complex.fromReal <| sin <| Complex.real", realsin )
run()
