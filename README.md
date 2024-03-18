# SAWA
An AI agents system to generate LRB article


## Installation


```shell
pip install -r requirements.txt
pip install -v -e .
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
## Gradio Demo
Run Gradio
```shell
python tools/gradio_demo.py
```


