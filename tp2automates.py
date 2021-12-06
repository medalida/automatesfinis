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

  return tp1_recognizes(a, word)
  
##################

def determinise(a:Automaton):
  
  for stateIndex in a.statesdict.copy().keys():
    for letter in a.statesdict[stateIndex].transitions:
      if '%' == letter:
        for TransState in list(a.statesdict[stateIndex].transitions['%']):
          for TransLetter in TransState.transitions:
            for TransState2 in list(TransState.transitions[TransLetter]):
              a.remove_transition(stateIndex,"%",TransState.name)
              a.add_transition(stateIndex, TransLetter, TransState2.name)
              if TransState.is_accept:
                a.statesdict[stateIndex].make_accept()

  not_determinise = True
  while(not_determinise):
    not_determinise = False
    for stateIndex in a.statesdict.copy().keys():
      for letter in a.statesdict[stateIndex].transitions:
        states = a.statesdict[stateIndex].transitions[letter].copy()
        if len(list(a.statesdict[stateIndex].transitions[letter])) > 1:
          not_determinise = True
          new_states = set()
          for state in list(states):
            new_states.add(state.name)
          

          for state in list(states):
            for trans_lettre in state.transitions:
              for trans_state in list(state.transitions[trans_lettre]):
                a.add_transition(str(new_states), trans_lettre, trans_state.name)
                if(state.is_accept):
                  a.make_accept(str(new_states))
          a.add_transition(stateIndex, letter, str(new_states))
          for state in states:
            print(a.alphabet)
            a.remove_transition(stateIndex, letter, state.name)
    a.remove_unreachable()

  
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
