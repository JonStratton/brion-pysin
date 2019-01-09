#!/usr/bin/env python
__author__ = 'Jon Stratton'
import sys, json, brion_pysin_lib

###############
# Global Vars #
###############

in_string  = ''
frag_type  = 'word'
min_chunk  = 1
max_chunk  = 3
randomness = 75

# Do something with 'myjson' object

def main():
   result = {}
   try:
      params = json.load(sys.stdin)
      if params['in_string']:
         in_string = params['in_string']
      if params['frag_type']:
         frag_type = params['frag_type']
      if params['min_chunk']:
         min_chunk = int( params['min_chunk'] )
      if params['max_chunk']:
         max_chunk = int( params['max_chunk'] )
      if params['randomness']:
         randomness = int( params['randomness'] )
      cutup_text = brion_pysin_lib.cutup( in_string, frag_type, min_chunk, max_chunk, randomness )
      result = {'success':'true','text':cutup_text}
   except ImportError:
      result = {'success':'false','text':'Error, module missing dependencies.'}
   except:
      result = {'success':'false'}
   print 'Content-Type: application/json\n\n'
   print json.dumps(result)
   return 0
main()
