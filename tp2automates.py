#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * YES if word is recognized
 * NO if word is rejected
Determinises the automaton if it's non deterministic
"""

from typing import Set, List
from automaton import Automaton, EPSILON, State, error, warn
from tp1automates import is_deterministic as tp1_is_deterministic
from tp1automates import recognizes as tp1_recognizes

import sys
import pdb # for debugging

##################

def is_deterministic(a:Automaton)->bool:
  
  return tp1_is_deterministic(a)
  
##################
  
def recognizes(a:Automaton, word:str)->bool:
  if not is_deterministic(a):
    a = determinise(a)
  
  return tp1_recognizes(a)
  
##################

def determinise(a:Automaton):
  a_determinised = Automaton(a.name + '_determinised')
  for stateIndex in a.statesdict:
    for letter in a.statesdict[stateIndex].transitions:
      if '%' == letter:
        for TransState in list(a.statesdict[stateIndex].transitions['%']):
          for TransLetter in TransState.transitions:
            for TransState2 in list(TransState.transitions[TransLetter]):
              a_determinised.add_transition(stateIndex, TransLetter, TransState2)
      else:
        for index in list(a.statesdict[stateIndex].transitions[letter]):
          a_determinised.add_transition(stateIndex, letter, index.name)
    if a.statesdict[stateIndex].is_accept:
      a_determinised.statesdict[stateIndex].make_accept()

  return a_determinised
  
################## 

if __name__ == "__main__" :
  if len(sys.argv) != 3:
    usagestring = "Usage: {} <automaton-file.af> <word-to-recognize>"
    error(usagestring.format(sys.argv[0]))

  automatonfile = sys.argv[1]  
  word = sys.argv[2]

  a = Automaton("dummy")
  a.from_txtfile(automatonfile)
  if not is_deterministic(a) :
    determinise(a)
  if recognizes(a, word):
    print("YES")
  else:
    print("NO")
