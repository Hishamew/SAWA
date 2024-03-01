import argparse
import yaml
from sawa import build_writer

def parse_args():
    parser = argparse.ArgumentParser(description = "a simple demo to use sawa")

    parser.add_argument("user_query",
                        type = str, 
                        help = "User demande on redbook article.")
    parser.add_argument("--config",default="config/sawa.yaml",
                        type = str,
                        help = "System config. Not Implemented by user.")

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    with open(args.config,'r') as f:
        config = yaml.safe_load(f)
    
    writer = build_writer(user_query = args.user_query, **config)
    article = writer.write()
    print(article)



if __name__ == "__main__":

    main()