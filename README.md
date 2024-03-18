# SAWA
An AI agents system to generate LRB article


## Installation


```shell
pip install -r requirements.txt
pip install -v -e .
```

## Prepare

To prepare embeddings for datasets:

Crawl or collect your data in format csv which contain no more no less than 4 columns: **contents,keyword,title and likes**.

Then use following command line to transform article into embeddings and save it in format npy.

```shell
python tools/tokenizer.py PATH_TO_DATASET.csv
```
You should find .npy file in same folder than .csv file.

After that, add datasets and embeddings path in config file, which is in folder config *config/sawa.yaml* .

At last, get your openai api base and api key, and rewrite file *config/openai/openai.yaml* to use GPT as LLM.

We prepare two sample dataset to make exemples.

## Example
```shell 
python tools/user.py USER_QUERY
```
## Gradio Demo
Run Gradio
```shell
python tools/gradio_demo.py
```


