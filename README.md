# PhenoBERT

 ![logo](https://github.com/EclipseCN/PhenoBERT/blob/main/phenobert/img/logo.jpg) 

A combined deep learning method for automated recognition of human phenotype ontology

📌 **Updated Training Pipeline**: See [PIPELINE.md](PIPELINE.md) for the latest training workflow.

[![Build Status](https://travis-ci.com/EclipseCN/PhenoBERT.svg?branch=main)](https://travis-ci.com/EclipseCN/PhenoBERT) ![Python](https://img.shields.io/badge/python->=3.6-blue)

### What is PhenoBERT?

PhenoBERT is a method that uses advanced deep learning methods (i.e. [convolutional neural networks](https://en.wikipedia.org/wiki/Convolutional_neural_network) and [BERT](https://en.wikipedia.org/wiki/BERT_(language_model))) to identify clinical disease phenotypes from free text. Currently, only English text is supported. Compared with other methods in the expert-annotated test data sets, PhenoBERT has reached SOTA effect.



### Citation:

Y. Feng, L. Qi and W. Tian, "PhenoBERT: a combined deep learning method for automated recognition of human phenotype ontology," in IEEE/ACM Transactions on Computational Biology and Bioinformatics, doi: 10.1109/TCBB.2022.3170301.



### How to install PhenoBERT

You can use PhenoBERT on your local machine, we have tested using docker. Due to some inevitable reason, the web version of PhenoBERT is not yet available.

#### From Source

1. Download total project from GitHub (You need install `git` first).

```shell
git clone https://github.com/EclipseCN/PhenoBERT.git
```

2. Enter the project main directory.

```she
cd PhenoBERT
```

3. Install dependencies in the current Python (>=3.6) environment (You need install `python>=3.6` first).

   Notice: we recommend using Python virtual environment (`venv`) to avoid confusion. 

```shell
pip install -r requirements.txt
python setup.py
```

4. Move the pretrained files into the corresponding folder.
```shell
# download files from Google Drive in advance
mv /path/to/download/embeddings/* phenobert/embeddings
mv /path/to/download/models/* phenobert/models
```

​       After step 4, file structure should like:

```shell
- phenobert/
    -- models/
         -- HPOModel_H/
         -- bert_model_max_triple.pkl
    -- embeddings/
         -- biobert_v1.1_pubmed/
         -- fasttext_pubmed.bin
```





### Pretrained embeddings and models

We have prepared pre-trained [fastText](https://en.wikipedia.org/wiki/FastText) and BERT embeddings and model files with .pkl suffix on [Google Drive](https://drive.google.com/) for downloading.

[click download link](https://drive.google.com/drive/folders/1jIqW19JJPzYuyUadxB5Mmfh-pWRiEopH?usp=sharing)

| Directory Name | File Name | Description |
| ---- | ------ | -------|
| models/ | [HPOModel_H/](https://drive.google.com/drive/folders/1NriTyBqh3kxUWv1lrnYjWBpYu0F0hrCh?usp=sharing) | CNN hierarchical model file |
|  | [bert_model_max_triple.pkl](https://drive.google.com/file/d/1AwRnaB5RruFUEdMkKohZmTlD4ILCkQ_z/view?usp=sharing) | BERT model file |
| embeddings/ | [biobert_v1.1_pubmed/](https://drive.google.com/drive/folders/10lko9BpToUl3PlUWrYbFmNyVHxDX1xby?usp=sharing) | BERT embedding obtained from [BioBERT](https://github.com/dmis-lab/biobert) |
| | [fasttext_pubmed.bin](https://drive.google.com/file/d/1GFB3I46B50sDUHcSpu84jZKqJnIjc--B/view?usp=sharing) | fastText embedding trained on [pubmed](https://en.wikipedia.org/wiki/PubMed) |

Once the download is complete, please put it in the corresponding folder for PhenoBERT to load.



### How to use PhenoBERT?

We provide three ways to use PhenoBERT. Due to this [issue](https://github.com/pytorch/pytorch/issues/18325), all calls need to be in the `phenobert/utils` path.

```shell
cd phenobert/utils
```



#### Annotate corpus folder

The most common usage is recognizing human clinical disease phenotype from free text. 

Giving a set of text files, PhenoBERT will then annotate each of the text files and generate an annotation file with the same name in the target folder.

Example use `annotate.py `:

```shell
python annotate.py -i DIR_IN -o DIR_OUT
```

Arguments: 

```shell
[Required]

 -i directory for storing text files
 -o directory for storing annotation files
 
[Optional]

 -p1 parameter for CNN model [0.8]
 -p2 parameter for CNN model [0.6]
 -p3 parameter for BERT model [0.9]
 -al flag for not filter overlapping concept
 -nb flag for not use BERT
 -t  cpu threads for calculation [10]
```



#### Related API

We also provide some APIs for other programs to integrate.

```python
from api import *
```

Running the above code will import related functions and related models, and temporarily store them as global variables for quick and repeated calls. Or you can simply use Python interactive shell.

Currently we have integrated the following functions:

1. annotate directly from String

```python
print(annotate_text("I have a headache"))
```

Output:

```shell
9       17      headache        HP:0002315        1.0
```

Notice: use `output = path/`can redirect output to specified file

2. get the approximate location of the disease

```python
print(get_L1_HPO_term(["cardiac hypertrophy", "renal disease"]))
```

Output:

```shell
[['cardiac hypertrophy', {'HP:0001626'}], ['renal disease', {'HP:0000119'}]]
```

3. get most similar HPO terms.

```python
print(get_most_related_HPO_term(["cardiac hypertrophy", "renal disease"]))
```

Output:

```shell
[['cardiac hypertrophy', 'None'], ['renal disease', 'HP:0000112']]
```

4. determine if two phrases match

```python
print(is_phrase_match_BERT("cardiac hypertrophy", "Ventricular hypertrophy"))
```

Output:

```shell
Match
```



#### GUI application

For users who are not familiar with command line tools, we also provide GUI annotation applications.

Simply use 

```shell
python gui.py
```

Then you will get a visual interactive interface as shown in the figure below, in which the yellow highlighted dialog box will display the running status.



![gui](https://github.com/EclipseCN/PhenoBERT/blob/main/phenobert/img/gui.gif)



### Dataset

We provide here two corpus with annotations used in the evaluation (`phenobert/data`), which are currently publicly available due to privacy processing.

| Dataset     | Num  | Description                                                  |
| ----------- | ---- | ------------------------------------------------------------ |
| GSC+        | 228  | Contains 228 abstracts of biomedical literature (Lobo et al., 2017) in raw format |
| ID-68       | 68   | Clinical description of 68 real cases in the intellectual disability study (Anazi et al., 2017) |
| GeneReviews | 10   | Contains 10 [GeneReviews](https://www.ncbi.nlm.nih.gov/books/NBK1116/) clinical cases and annotations |
| val         | 30   | Contains 30 disease research articles from the [OMIM database](https://www.omim.org/) to determine hyperparameters in our model |



### Train your own model

For the convenience of some users who cannot log in to Google Drive or who want to customize training process for their selves.

We provide the training Python script and training set used by PhenoBERT. Of course, the training set can be customized by the user to generate specific models for other purposes.

```shell
cd phenobert/utils

# produce trained models for CNN model
python train.py
python train_sub.py

# produce trained models for BERT model
python my_bert_match.py
```

