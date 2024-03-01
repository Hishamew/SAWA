# SAWA
An AI agents system to generate LRB article


## Installation


```shell
pip install -r requirements.txt
pip install -v -e .
```
## Gradio Demo
本地运行gradio
```shell
python tools\gradio_demo.py
```

## Prepare

To prepare embeddings for datasets
```shell
python tools/tokenizer.py PATH_TO_DATASET.csv
```

## Example
```shell 
python tools/user.py USER_QUERY
```


## Developement Log

### v0.0.2
Build a base line to handle user query.

### v0.0.3 
Now use numpy instead of torch to do calculate.

### v0.0.4 
Complete prompt engineering, a common baseline is built.

