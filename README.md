# SAWA
An AI agents system to generate LRB article

## Installation

Step 1:
Install torch following [official instruction](https://pytorch.org/)

Step 2:
Install dependencies
```shell
pip install -r requirements.txt
```

Step 3:
Install sawa
```
pip install -v -e .
```


## Prepare

To prepare embeddings for datasets
```shell
python tools/tokenizer.py PATH_TO_DATASET.csv
```

## Example
```shell 
python tools/user.py
```


