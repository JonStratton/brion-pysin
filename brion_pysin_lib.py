#!/usr/bin/env python
__author__ = 'Jon Stratton'
import re, random
from collections import defaultdict

def cutup( in_string, frag_type, min_chunk, max_chunk, randomness ):
   shuffled_text = ''
   if frag_type == 'madlib':
      shuffled_text = madlib_cutup( in_string, randomness )
   else:
      shuffled_text = traditional_cutup( in_string, frag_type, min_chunk, max_chunk, randomness )

   return shuffled_text

# Normal Character/Word/Sentence/Line cut up
def traditional_cutup( in_string, frag_type, min_chunk, max_chunk, randomness ):
   split_frag, join_frag = '', ''
   if frag_type == 'sent':
      split_frag, join_frag = '[.!?,]+', '. '
   elif frag_type == 'word':
      split_frag, join_frag = '[ ]+', ' '
   elif frag_type == 'line':
      split_frag, join_frag = '\n', '\n'

   chunked_text = chunk_text( in_string, split_frag, min_chunk, max_chunk )
   shuffled_chunks = shuffle_chunks( chunked_text, randomness )
   shuffled_text = join_chunks( shuffled_chunks, join_frag )

   return shuffled_text

# Madlib cut up. This needs the nltk, which may not be installed. Load it the last moment.
def madlib_cutup( in_string, randomness ):
   from nltk.tokenize import sent_tokenize, word_tokenize
   from nltk.tag import pos_tag

   # Get a dict of words based on type, and an array of sentences with just the types instead of words (skeleton)
   type_to_words  = defaultdict(list)
   sent_skeletons = []
   for sent in sent_tokenize( in_string ):
      sent_skeleton = []
      for word, tag in pos_tag( word_tokenize( sent ) ):
         sent_skeleton.append( tag )
         type_to_words[tag].append( word )
      sent_skeletons.append( sent_skeleton )

   # Shuffle items in dict, and sentence skeleton
   shuffled_skeletons = shuffle_chunks( sent_skeletons, randomness )
   for tag in type_to_words:
      type_to_words[tag] = shuffle_chunks( type_to_words[tag], randomness )

   # Foreach sentence, foreach word, pull a word out of the hashmaps. Then join together and 
   out_text = []
   for skel in shuffled_skeletons:
      for tag in skel:
         out_text.append( type_to_words[tag].pop( 0 ) )

   return ' '.join( out_text )

# Breaks input text into chunks
def chunk_text( in_string, split_frag, min_chunk, max_chunk ):
   inOrderedChunks = []
   if split_frag:
      inOrderedChunks = re.split( split_frag, in_string );
   else:
      inOrderedChunks = list( in_string )

   # Randomize based on chunk size
   inOrderedChunksSized = []
   while len( inOrderedChunks ):
      # get a chunk size
      chunk_size = random.randint( min_chunk, max_chunk )
      left = len( inOrderedChunks );
      if chunk_size > left:
         chunk_size = left

      # Pull chunk off and add it to our array
      chunk = []
      for i in range( 0, ( chunk_size ) ):
         chunk.append( inOrderedChunks[0] )
         inOrderedChunks = inOrderedChunks[1:]
      inOrderedChunksSized.append( chunk )

   return inOrderedChunksSized

# Shuffles the first level of a matrix based on randomness
def shuffle_chunks( chunked_array, randomness ):
   indexes_to_shuffle = []
   chunks_to_shuffle  = []

   index = 0
   for chunk in chunked_array:
      if randomness >= random.randint( 0, 100 ):
         indexes_to_shuffle.append( index )
         chunks_to_shuffle.append( chunk )
      index = index + 1

   # Shuffle the subset
   random.shuffle( chunks_to_shuffle )

   # Fold those shuffled items back into chunked_array
   for index in indexes_to_shuffle:
      chunked_array[ index ] = chunks_to_shuffle.pop()
   return chunked_array

# Flattens matrix and joins off of input
def join_chunks( chunked_text, join_frag ):
   flat_chunks = [] 
   for chunk in chunked_text:
      for fragment in chunk:
         flat_chunks.append( fragment )
   return join_frag.join( flat_chunks )
