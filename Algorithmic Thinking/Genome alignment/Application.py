# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 14:30:53 2016

@author: Administrator
"""

"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2
import numpy as np


if DESKTOP:
    import matplotlib.pyplot as plt
    import functions as student
else:
    import simpleplot
    import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list
    
    
PAM50_SCORING_MATRIX= read_scoring_matrix(PAM50_URL)
HUMAN_EYLESS_PROTEIN = read_protein(HUMAN_EYELESS_URL)
FRUITFLY_EYELESS_PROTEIN = read_protein(FRUITFLY_EYELESS_URL)

ali_matrix = student.compute_alignment_matrix(HUMAN_EYLESS_PROTEIN,FRUITFLY_EYELESS_PROTEIN,PAM50_SCORING_MATRIX, False)
#print student.max_in_alig_matrix(ali_matrix)
#opt_local_ali = student.compute_local_alignment(HUMAN_EYELESS_PROTEIN,FRUITFLY_EYLESS_PROTEIN,PAM50_SCORING_MATRIX,ali_matrix)
#print opt_local_ali

RESULT_Q1 = (875, 'HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ', 'HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ')

CONCENSUS_PAX = read_protein(CONSENSUS_PAX_URL)

def delete_dash_complete(str1):
    '''
    delete dash from a str 
    '''
    output_str = ''
    for char in str1:
        if char != '-':
            output_str += char
    return output_str        

#test = 'abc--de' 
#print delete_dash_complete(test)       
        
def compute_global_and_percentage(str_list,consensus):
    '''
    compute each str in str_list global alignment with consensus and the percentage 
    similarity with consensus by characters 
    '''
    result = []
    for str_ele in str_list:
        temp_ele = delete_dash_complete(str_ele)
        temp_ali_matrix = student.compute_alignment_matrix(temp_ele,CONCENSUS_PAX,PAM50_SCORING_MATRIX, True)
        temp_global_ali = student.compute_global_alignment(temp_ele,CONCENSUS_PAX,PAM50_SCORING_MATRIX,temp_ali_matrix)
        temp_result_str_x = temp_global_ali[1]
        temp_result_str_y = temp_global_ali[2]
        match_len = 0
        for num_iter in range(len(temp_result_str_x)):
            if temp_result_str_x[num_iter] == temp_result_str_y[num_iter]:
                match_len += 1 
        temp_result = [float(match_len)/ len(temp_result_str_y)]      
        result += temp_result
    return result 
      
#print compute_global_and_percentage([RESULT_Q1[1],RESULT_Q1[2]],CONCENSUS_PAX)        


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    '''
    takes two str input 
    returns a dict that represents an unnormalized distribution generated by performing the following trials
    generate random permuataion rand_y 
    find the max score of the alignment of seq_x and rand_y
    bar plot the distribution 
    '''
    scoring_distribution = {}
    for trial_num in range(num_trials):
        print trial_num
        rand_y = student.shuffle_str(seq_y)
        temp_ali_matrix = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        (opt_local_score, _1, _2,) = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, temp_ali_matrix)
        if opt_local_score in scoring_distribution:
            scoring_distribution[opt_local_score] += 1 
        else:
            scoring_distribution[opt_local_score] = 1 
    return scoring_distribution

#trial_result = generate_null_distribution(HUMAN_EYLESS_PROTEIN, FRUITFLY_EYELESS_PROTEIN, PAM50_SCORING_MATRIX, 1000 )
#print trial_result 
TRIAL_RESULT = {39: 3, 40: 9, 41: 10, 42: 20, 43: 24, 44: 43, 45: 48, 46: 64, 47: 68, 48: 62, 49: 57, 50: 71, 51: 63, 52: 63, 53: 46, 54: 44, 55: 52, 56: 39, 57: 39, 58: 30, 59: 21, 60: 22, 61: 22, 62: 16, 63: 9, 64: 6, 65: 8, 66: 8, 67: 3, 68: 7, 69: 5, 70: 2, 71: 2, 72: 4, 73: 1, 74: 1, 75: 2, 77: 1, 78: 2, 83: 2, 85: 1}

def list_mean_std(dict1):
    '''
    calculate list_mean and std of the trial_result 
    '''
    total_num = 0
    total_score = 0
    for ele in dict1:
        total_score += dict1[ele]*ele
        total_num += dict1[ele]
    mean = total_score/ float(total_num)
    print total_num
    
    mean_sqr = 0
    for ele in dict1:
        mean_sqr += 1/float(total_num) * (dict1[ele]-mean)**2
    std = mean_sqr**(0.5)
    return [mean,std]     
        
[trial_mean, trial_std] = list_mean_std(TRIAL_RESULT)       
trial_z_score = (875 - trial_mean)/trial_std
print trial_z_score
#plt.bar(TRIAL_RESULT.keys(),TRIAL_RESULT.values(), )

word_list = read_words(WORD_LIST_URL)

def check_spelling(checked_word,dist,word_list):
    '''
    diag_score = 2, dash_score = 0, off_diag_score = 1 to build scoring matrix 
    '''
    alpha_temp = 'abcdefghijklmnopqrstuvwxyz'
    alpha = set([])
    word_check_len = len(checked_word)
    for char in alpha_temp:
        alpha.add(char)
    scoring_matrix = student.build_scoring_matrix(alpha,2,1,0)
    result_list = []
    for word in word_list:
        temp_ali_matrix = student.compute_alignment_matrix(checked_word, word, scoring_matrix, True)
        (temp_score, _1, _2) = student.compute_global_alignment(checked_word, word, scoring_matrix,temp_ali_matrix)
        temp_dist = len(word) + word_check_len - temp_score
        if temp_dist <= dist:
            result_list += [word]
    return result_list 

print check_spelling('humble',1,word_list)      
print check_spelling('firefly',2,word_list) 