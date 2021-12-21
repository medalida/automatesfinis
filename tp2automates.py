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

  #remove EPDILONS
  is_empty_word = True
  while(is_empty_word):
    is_empty_word = False
    for stateIndex in a.statesdict:
      for letter in a.statesdict[stateIndex].transitions.copy():
        if letter == EPSILON and bool(a.statesdict[stateIndex].transitions[EPSILON]):
          for TransState in a.statesdict[stateIndex].transitions[EPSILON].copy():
            is_empty_word = True
            a.remove_transition(stateIndex,EPSILON,TransState.name)
            
            for TransLetter in TransState.transitions:
              for TransState2 in list(TransState.transitions[TransLetter]):
                
                if (stateIndex, TransLetter, TransState2.name) not in a.transitions:
                  a.add_transition(stateIndex, TransLetter, TransState2.name)
                if TransState.is_accept:
                  a.statesdict[stateIndex].make_accept()
  a.remove_unreachable()
  
  # seconde step of determinisation

  det = a
  a = a.deepcopy()
  det.reset(det.name)
  accept = False
  new_states = [set([a.initial.name])]
  treated_sates = set()
  acceptstates = []
  while(bool(new_states)):
    if(str(new_states[0]) in treated_sates):
      new_states.remove(new_states[0])
    else:
      for letter in a.alphabet:
        new_state = set()
        for state in new_states[0]:
          if(a.statesdict[state].is_accept):
            accept = True
          if(letter in a.statesdict[state].transitions.keys()):
            for trans_state in list(a.statesdict[state].transitions[letter]):
              new_state.add(trans_state.name)
        if(accept):
            acceptstates.append(str(new_states[0]))
            accept = False
        if(bool(new_state)):
          det.add_transition(str(new_states[0]), letter, str(new_state))
          new_states.append(new_state)
      treated_sates.add(str(new_states[0]))
      new_states.remove(new_states[0])
  det.make_accept(acceptstates)
  a.remove_unreachable()

  #rename states
  #some line of code that assert that the initial state has index 0 and finales states have the big indexes

  endIndex = len(det.states) - 1
  startIndex = 1
  det.rename_state(det.initial.name, str(0))
  states = set(det.statesdict.copy().keys())
  states.remove(det.initial.name)
  for state in det.acceptstates:
    if state in states:
        det.rename_state(state, str(endIndex))
        states.remove(state)
        endIndex = endIndex - 1
  for letter in det.statesdict[det.initial.name].transitions:
    for state in det.statesdict[det.initial.name].transitions[letter]:
      name = state.name
      if state.name in states:
        det.rename_state(state.name, str(startIndex))
        states.remove(name)
        startIndex = startIndex + 1
  
  for state in states:
    det.rename_state(state, str(startIndex))
    startIndex = startIndex + 1


  
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
