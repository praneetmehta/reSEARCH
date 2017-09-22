# reSEARCH
Research Paper Information Retrieval System using Python.

Course Assignment for CS F469- Information Retrieval @ BITS Pilani, Hyderabad Campus.
**Done under the able guidance of Dr. Aruna Malapati, Assistant Professor, BITS Pilani, Hyderabad Campus.**

## Table of Contents
- [reSEARCH](#research)
        * [Running the scraper](#running-the-scraper)
        * [Starting the web server](#starting-the-web-server)
        * [Building and saving a new trie](#building-and-saving-a-new-trie)
        * [Loading a constructed trie](#loading-a-constructed-trie)
  * [Introduction](#introduction)
  * [Data](#data)
  * [Text Preprocessing](#text-preprocessing)
  * [Data Structures used](#data-structures-used)
  * [Time complexity of Inserting and Querying](#time-complexity-of-inserting-and-querying)
  * [Tf-Idf formulation](#tf-idf-formulation)
  * [Machine specs](#machine-specs-)
  * [Results](#results)
  * [Web client Documentation](#web-client-documentation)
  * [Further Scope](#further-scope)
  * [Members](#members)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


##### Running the scraper
```python
pip install clairvoyant
```

##### Starting the web server
```python
pip install clairvoyant
```

##### Building and saving a new trie
```python
pip install clairvoyant
```

##### Loading a constructed trie
```python
pip install clairvoyant
```

## Introduction
A tf-idf based Search Engine for research papers on Arxiv. The main purpose of this project is understand how vector space based retrieval models work.
*More on [Tf-Idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf).*

## Data
The data has been scraped from [Arxiv](https://arxiv.org). The scraper is present in *scraper.py* which can be found in the directory *scraper*.

We use the following data  of **16000** papers from all categories present on Arxiv:
1. Title
2. Abstract
3. Authors
4. Subjects
**Total terms in vocabulary = 38773.**
***Note**: Only Abstract data has been used for searching.*

The data is organized into directories as follows:
Data/
├── abstracts &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   # text files containing the abstract
├── authors     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# text files containing authors 
├── link       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; # text files containing link to the pdf of the paper
├── subject     &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# text files containing subjects
└── title       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# text files containing the title 


## Text Preprocessing
We processed the raw text scraped from Arxiv by applying the following operations-
1. Tokenization
2. Stemming
3. Lemmatization
4. Stopwords removal

## Data Structures used
We used a Trie to store words and their Term frequencies in the different Documents and their Document Frequencies. The Trie is also used to generate typing suggestions while querying.

## Time complexity of Inserting and Querying
The time complexity of querying and inserting an element into the Trie is **O(n)**.
*n* → *number of charcters in the query term*.

## Tf-Idf formulation
Tf-Idf score = tf*log(N/df)

tf &nbsp;→ &nbsp;Term frequency of the term in the current document
df → &nbsp;Document frequency of the term
N → &nbsp;Total number of documents in corpus

## Machine specs:
Processor: i7
Ram: 8 GB DDR4
OS: Ubuntu 16.04 LTS

## Results
Index building time: 76.97 s.
Memory usage: around 410 MB.
Average time of query search: 

## Web client Documentation
**Insert screenshots**

## Further Scope

## Members
[Shubham Jha](github.com/shubhamjha97)
[Praneet Mehta](github.com/praneetmehta)
[Abhinav Jain](github.com/abhinav1112)
[Papa](http://github.com/stgstg27)