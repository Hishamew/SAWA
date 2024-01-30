import argparse
from utils.retrieval import Retrieval
from utils.prompt import Prompt
from utils.call_llm import LLM
def main(args):
    data_path = "data/toy_dataset.json"
    retrieval = Retrieval(args.keyword, data_path)
    example = retrieval.keyword_retrieval()
    prompt = Prompt(example, args.keyword)
    output = LLM(prompt)
    with open(args.output_path, "w", encoding='utf-8') as f:
        f.write(str(output))
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", type=str, default="留学")
    parser.add_argument("--output_path", type=str, default="./output.txt")
    args = parser.parse_args()

    main(args)