
"""
Google level inverted index implementation
start building from this file FIRST

"""
import pickle
import struct
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import heapq
from collections import defaultdict


#A data class is a clean container for data
@dataclass
class Posting:
    #posting list entry with positions and payload
    doc_id: int
    term_freq: int
    positions: List[int]
    next__pointer: Optional[int] = None
    
    def __repr__(self):
        return f"posting(doc={self.doc_id}, tf={self.term_freq}, pos={self.positions})"

class InvertedIndex:
    """ 
    Complete Inverted Index wih:
    --Positional information
    --Skip pointers for fast intersection
    --Compression support
    --Persistnece of disk
    
    """
    def __init__(self, compression: str = 'varbyte'):
        
        self.index = {} #term -> {df, postings, skip_pointers}
        self.doc_metadata = {} #doc-id -> {length, url, title}
        self.total_docs = 0  #Corpus size for idf
        self.total_terms = 0 #Vocabulary size
        self.compression = compression #Posting list compression method
    
        #statistics for ranking
        self.avg_doc_length = 0
        self.doc_lengths: Dict[int, int] = {}
        
        
    def add_document(self, doc_id:int, text: str, metadata: Dict = None):
        """
        Add a document to the index
        This is where the magic happens !
        --Actually  it Tokenize, build posting list, update stats
        
        Args:
            doc_id (int): Unique document ID
            text (str): Document text
            metadata (Dict, optional): Additional info
        
        """
        #Tokenize text
        tokens = self._tokenize(text)
        self.total_terms += len(tokens)
        
        #Store document metadata
        self.doc_metadata[doc_id] = metadata or {}
        self.doc_lengths[doc_id] = len(tokens)
        self.total_docs += 1
        
        #Process each token with its positon
        for position, token in enumerate(tokens):
            if token not in self.index:
                self.index[token] = {
                    'df': 0,
                    'postings': [],
                    'skip_pointers': []
                }
                
            # Retrieve all documents (postings list) where this token appears
            postings = self.index[token]['postings']
            
            # Check if we need to add to existing posting or create new
            if not postings or postings[-1].doc_id != doc_id:
                # New posting for this document
                posting = Posting(
                    doc_id=doc_id,
                    term_freq=1,
                    positions=[position]
                )
                postings.append(posting)
                self.index[token]['doc_freq'] += 1
            else:
                # Update existing posting
                last_posting = postings[-1]
                last_posting.term_freq += 1
                last_posting.positions.append(position)
      
    def _tokenize(self, text:str):
        #Basic tokenizer - I will enhance this later
        
        #convert to lowercase
        text = text.lower()
        
        #Simple splitting(I will add better tokenication)
        tokens = text.split()
        current_token = []
        
        for char in text:
            if char.isalnum():
                current_token.append(char)
            
            elif current_token:
                #End of token
                tokens.append(''.join(current_token))
                current_token = []
        
        #Handle last token   
        if current_token:
            tokens.append(''.join(current_token))
          
        #return the list of tokens  
        return tokens
    
    def _add_skip_pointers(self, term:str):
        '''
        --add skip pointers to a posting list for a given term
        Skip pointers allow faster intersection of posting lists
        --or Add skip pointers to posting list
        skip every sqrt(n)th posting for o(sqrt(n)) intersection
        
        Args:
            term (str): Term to add skip pointers to
        '''
        postings = self.index[term]['postings']
        n = len(postings)
        skip_every = max(1, int(math.sqrt(n)))
        
        skip_pointers = {} #position -> skip pointer
        for i in range(0, n, skip_every):
            if i + skip_every < n:
                skip_pointers[i] = i + skip_every
            else:
                #Last pointer points to end
                skip_pointers[i] = n - 1
        
        #Update index with skip pointers
        self.index[term]['skip_pointers'] = skip_pointers
        
    def intersect(self, term1: str, term2: str) -> List[int]:
        """
        Intersect two posting lists using skip pointers
        This is the CORE algorithm you need to master
        """
        if term1 not in self.index or term2 not in self.index:
            return []
        
        result = []
        p1 = self.index[term1]['postings']
        p2 = self.index[term2]['postings']
        
        i = j = 0
        skip1 = self.index[term1]['skip_pointers']
        skip2 = self.index[term2]['skip_pointers']
        
        while i < len(p1) and j < len(p2):
            doc1 = p1[i].doc_id
            doc2 = p2[j].doc_id
            
            if doc1 == doc2:
                result.append(doc1)
                i += 1
                j += 1
            elif doc1 < doc2:
                # Use skip pointer if available and beneficial
                if i in skip1 and p1[skip1[i]].doc_id <= doc2:
                    i = skip1[i]
                else:
                    i += 1
            else:
                if j in skip2 and p2[skip2[j]].doc_id <= doc1:
                    j = skip2[j]
                else:
                    j += 1
        
        return result
        
                
                  
        
        
        
        
        
        
        
        
