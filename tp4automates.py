#!/usr/bin/env python3
"""
Read a regular expression and returns:
 * YES if word is recognized
 * NO if word is rejected"""

from tp1automates import is_deterministic as tp1_is_deterministic, recognizes as tp1_recognizes
from tp3automates import kleene as tp3_kleene, concat as tp3_concat, union as tp3_union
from tp2automates import determinise as tp2_determinise
from typing import Set, List
from automaton import Automaton, EPSILON, State, error, warn, RegExpReader
import sys
import pdb # for debugging

##################

def is_deterministic(a:Automaton)->bool:
  # Copy-paste or import from previous TPs
  return tp1_is_deterministic(a)
  
##################
  
def recognizes(a:Automaton, word:str)->bool:
  # Copy-paste or import from previous TPs
  return tp1_recognizes(a, word)
  
##################

def determinise(a:Automaton):
  # Copy-paste or import from previous TPs
  tp2_determinise(a)
  try:
    re = a.name.replace('*','^')
    a.to_graphviz("test/L("+re+")_det.gv")
  except:
    print('error: graphviz may be not installed ):')

##################

def kleene(a1:Automaton)->Automaton:
  return tp3_kleene(a1)

##################

def concat(a1:Automaton, a2:Automaton)->Automaton:
  return tp3_concat(a1, a2)

##################

def union(a1:Automaton, a2:Automaton)->Automaton:
  return tp3_union(a1, a2)
  
##################
   
def regexp_to_automaton(re:str)->Automaton:
  """
  Moore's algorithm: regular expression `re` -> non-deterministic automaton
  """
  postfix = RegExpReader(re).to_postfix()
  stack:List[Automaton] = []
  
  for letter in postfix:
    if letter == '*':
      a = stack.pop()
      a = kleene(a)
      stack.append(a)
    elif letter == '+':
      b = stack.pop()
      a = stack.pop()
      a = union(a, b)
      stack.append(a)
    elif letter == '.':
      b = stack.pop()
      a = stack.pop()
      a = concat(a, b)
      stack.append(a)
    else:
      a = Automaton(letter)
      a.add_transition("0", letter, "1")
      a.make_accept("1")
      stack.append(a)

  a = stack[0]
  a.name = re
  re = re.replace('*','^')
  
  try:
    a.to_graphviz("test/L("+re+").gv")
  except:
    print('error: graphviz may be not installed ):')
  return stack[0]
  
##################

if __name__ == "__main__" :

  if len(sys.argv) != 3:
    usagestring = "Usage: {} <regular-expression> <word-to-recognize>"
    error(usagestring.format(sys.argv[0]))

  regexp = sys.argv[1]  
  word = sys.argv[2]

  a = regexp_to_automaton(regexp)
  determinise(a)
  if recognizes(a, word):
    print("YES")
  else:
    print("NO")

