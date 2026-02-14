"""
BM25 ranking Algorithm.
Implement this after my index is working 
"""

import math
from typing import List, Dict

class BM25:
    
    """
    Docstring for BM25
    BM25  algorithm for ranking documents based on query terms
    Attributes:
        k1 (float): Tuning parameter, controls term frequency normalization(typically 1.2-2.0)
        b (float): Tuning parameter, controls document length normalization(typically 0.75)
        index (InvertedIndex): Inverted index object
        avg_doc_length (float): Average document length in the corpus
        doc_lengths (Dict[int, int]): Document lengths
    """
    def __init__(self, k1:float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.avg_doc_length = 0
        self.doc_lengths: Dict[int, int] = {}
        self.total_docs = 0
        self.doc_freqs: Dict[str, int] = {}
        