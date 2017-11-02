#!/usr/bin/env python

# Modified for elm 0.18 and elm-community/elm-test

# Change test strategy to use relative tolerance
# Old strategy: assert(Basic.abs(Complex.abs(computed) - Complex.abs(expected)) < 0.0001)
# New strategy: assert(Basic.abs((Complex.abs(computed) - Complex.abs(expected)) / Complex.abs(expected)) < 0.0000000000001)

# Split up tests using individual test files to avoid stack overflow
# This script will generate all test files in one run resulting in:
#   tests/Abs.elm
#   tests/Acos.elm
#   tests/Asin.elm
#   tests/Atan.elm
#   tests/Cos.elm
#   tests/Div.elm
#   tests/Exp.elm
#   tests/Ln.elm
#   tests/Mult.elm
#   tests/Arg.elm
#   tests/Pow.elm
#   tests/Sign.elm
#   tests/Sin.elm
#   tests/Sqrt.elm
#   tests/Tan.elm

# Run tests from this directory:
# Example: elm-test tests/Mul.elm

# Run all tests with a simple loop:
# for t in *.elm; do elm-test $t; done

import numpy as np
#np.set_printoptions(precision=32)
#np.set_printoptions(formatter={'float': lambda x: "{0:0.32f}".format(x)})

import random
import sys
from itertools import chain, izip, repeat, islice

#globals
names = []
nargss = []
nrunss = []
elm_functions = []
args_gens = []
result_gens = []
type_transforms = []
headers = []

#helper functinos

def intersperse(delimiter, seq):
    return list(islice(chain.from_iterable(izip(repeat(delimiter), seq)), 1, None))

def argstring(listofargs):
    return ' '.join(intersperse(' ',map(str,listofargs)))

#write a test
def test_write(name,elm_function, args, result ):
    # absolute tolerance
    #print("{0} : Test\n{0} = test \"{0}\" <| \\_ -> (Expect.true \"test\" ((Basics.abs ((Complex.abs ({1} {2})) - (Complex.abs ({3})))) < 0.0001))".format(name,elm_function,argstring(args),result))
    # relative tolerance
    #print("{0} : Test\n{0} = test \"{0}\" <| \\_ -> (Expect.true \"test\" ((Basics.abs ((Complex.abs ({1} {2})) - (Complex.abs ({3}))) / (Complex.abs ({3}))) < 0.0000000000001))".format(name,elm_function,argstring(args),result))
    print("{0} : Test\n{0} = test \"{0}\" <| \\_ -> (Expect.true \"({1} {2}) ~ ({3})\" ((Basics.abs ((Complex.abs ({1} {2})) - (Complex.abs ({3}))) / (Complex.abs ({3}))) < 0.0000000000001))".format(name,elm_function,argstring(args),result))
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
    return name

def testfile_write(module,names,nargss,nrunss,elm_functions,args_gens,result_gens,type_transforms,headers):
    print("module "+module+" exposing(..)")
    for x in headers:
        print(x)
    all_tests = []
    for x in range(0,len(names)):
        all_tests.append(suite_write(names[x],nargss[x],nrunss[x],elm_functions[x],args_gens[x],result_gens[x],type_transforms[x]))

# reset all arrays except headers for next run
def reset():
    names[:]=[]
    nargss[:]=[]
    nrunss[:]=[]
    elm_functions[:]=[]
    args_gens[:]=[]
    result_gens[:]=[]
    type_transforms[:]=[]

headers.append("import Expect exposing (Expectation)")
headers.append("import Fuzz exposing (Fuzzer, int, list, string)")
headers.append("import Test exposing (..)")
headers.append("import Complex")

def run(module):
    testfile = open(module+".elm",'w+')
    temp = sys.stdout
    sys.stdout = testfile
    testfile_write(module,names,nargss,nrunss,elm_functions,args_gens,result_gens,type_transforms,headers)
    testfile.close()
    sys.stdout = temp
    reset()

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

def gentest_binary_complex(modulename,testname,numtests,funcname,function):
  add_binary_complex(testname,numtests,funcname,function)
  run(modulename)

def gentest_unary_complex(modulename,testname,numtests,funcname,function):
  add_unary_complex(testname,numtests,funcname,function)
  run(modulename)

gentest_binary_complex("Mult","complex_mult",200,"Complex.mult",cmult)
gentest_binary_complex("Div","complex_div",200,"Complex.div",lambda x,y: x/y)
gentest_unary_complex("Abs","complex_abs",200,"Complex.fromReal <| Complex.abs",np.abs)
gentest_unary_complex("Sign","complex_sign",200,"Complex.fromReal <| Complex.sgn",np.sign)
gentest_unary_complex("Sqrt","complex_sqrt",200,"Complex.sqrt",np.sqrt)
gentest_unary_complex("Arg","complex_arg",200,"Complex.fromReal <| Complex.arg",np.angle)
gentest_unary_complex("Ln","complex_ln",200," Complex.ln",np.log)
gentest_unary_complex("Exp","complex_exp",200,"Complex.exp",np.exp)
gentest_binary_complex("Pow","complex_pow",200,"Complex.pow",np.power)
gentest_unary_complex("Cos","complex_cos",200,"Complex.cos",np.cos)
gentest_unary_complex("Sin","complex_sin",200,"Complex.sin",np.sin)
gentest_unary_complex("Tan","complex_tan",200,"Complex.tan",np.tan)
gentest_unary_complex("Asin","complex_asin",200,"Complex.asin",np.arcsin)
gentest_unary_complex("Acos","complex_acos",200,"Complex.acos",np.arccos)
gentest_unary_complex("Atan","complex_atan",200,"Complex.atan",np.arctan)
#gentest_binary_complex("Multlog","complex_mult_log",200,"(\z w -> Complex.mult w (Complex.ln z))",multlog )
#gentest_binary_complex("Newpow","new_pow",200,"Complex.pow",newexp)
#gentest_unary_complex("Realsin","realsine", 1000, "Complex.fromReal <| sin <| Complex.real", realsin )
