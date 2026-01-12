
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
        
        
        
        
