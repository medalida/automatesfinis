#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * ERROR if non deterministic
 * YES if word is recognized
 * NO if word is rejected
"""

from automaton import Automaton, EPSILON, error, warn
import sys
import pdb # for debugging

##################

def is_deterministic(a:'Automaton')->bool:
  
  for stateIndex in a.statesdict:
    for letter in a.statesdict[stateIndex].transitions:
      if len(a.statesdict[stateIndex].transitions[letter]) > 1:
        return False
      elif '%' in a.statesdict[stateIndex].transitions and len(a.statesdict[stateIndex].transitions['%']) > 0:
        return False
        
  return True
    
  
##################
  
def recognizes(a:'Automaton', word:str)->bool:

  currentStateIndex = a.initial.name
  word = word.replace("%","")
  
  if word == "" and a.initial.is_accept:
    return True
  elif word == "" and not a.initial.is_accept:
    return False

  for letter in word:
    if letter not in a.statesdict[currentStateIndex].transitions.keys():
      return False
    currentStateIndex = list(a.statesdict[currentStateIndex].transitions[letter])[0].name
  
  if a.statesdict[currentStateIndex].is_accept:
    return True
  return False 

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
    print("ERROR")
  elif recognizes(a, word):
    print("YES")
  else:
    print("NO")

