import unittest
from pathlib import Path
import os, sys
import json
import pandas as pd
from src.compile_word_counts import filter_pony, get_word_count,get_stopwords
from src.compute_pony_lang import get_word_used_by_num_ponies, get_tf_idf
# import src.compute_pony_lang
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        
        

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        df = pd.read_csv(self.mock_dialog)
        out_t1 = {}                                                       #this dictionary will contain ALL words, before <5 filter
        words = get_stopwords()
        ponies = ['twilight sparkle','applejack','rarity','pinkie pie','rainbow dash','fluttershy']                                                     
        for pony in ponies:
            try:
                filtered_df = filter_pony(df,'pony',pony)                 #filtering dataframe for each pony
                out_t1[pony] = {}                                         #creating an empty dictionary for each pony
                out_t1[pony] = get_word_count(filtered_df,words)          #storing returned dictionary from get_word_count method in the above empty dict
            except:
                out_t1[pony] = {}
        
        out_t1_json = json.dumps(out_t1)
        with open(self.true_word_counts) as f1:
            true_word_counts = json.load(f1)
        true_word_counts = json.dumps(true_word_counts)
        self.assertEqual(true_word_counts,out_t1_json)
        print("***Task 1 test passed!***")

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        ponies = ['twilight sparkle','applejack','rarity','pinkie pie','rainbow dash','fluttershy']
        with open(self.true_word_counts) as f1:
            true_word_counts = json.load(f1)
        true_word_counts = json.dumps(true_word_counts)

        df = pd.read_json(true_word_counts)
        df = df.fillna(0)
        df = get_word_used_by_num_ponies(df,ponies)
        tf_idf_output = get_tf_idf(df,ponies)
        tf_idf_output = json.dumps(tf_idf_output)

        with open(self.true_tf_idfs) as f2:
            true_tf_idfs = json.load(f2)
        true_tf_idfs = json.dumps(true_tf_idfs)


        self.assertEqual(true_tf_idfs,tf_idf_output)
        print("***Task 2 test passed!***")
        

if __name__ == '__main__':
    unittest.main()