import csv
import argparse
import json

list_to_tsv = []


def get_info(tweet):
    #dem_count = 0
    #rep_count = 0

    # change print statements to something meaningful to the project later
    text = tweet['text']
    words = text.split()
    punctuation = "!#$%&()*+,./:;<=>?@[\]^_`{|}~"
    table = str.maketrans('', '', punctuation)
    tokenized_text = [w.translate(table) for w in words]

    """
    political_party = ""
    if dem_count > rep_count:
        political_party = 'democrat'
    elif rep_count > dem_count:
        political_party = 'republican'
    else:
        political_party = 'neutral'
    """

    addition_list = []
    addition_list.append(tweet["user"]["id"])
    addition_list.append(tweet["user"]["friends_count"])
    #addition_list.append(dem_count)
    #addition_list.append(rep_count)
    addition_list.append(tweet["created_at"])
    #addition_list.append(political_party)
    addition_list.append(text)
    addition_list.append(tokenized_text)

    list_to_tsv.append(addition_list)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', type=str, help='The JSONL file with our tweets')
    parser.add_argument('-o', '--output', dest='output', type=str, help="The CSV we're outputting annotated tweets to")
    return parser.parse_args()


def read_jsonl(path):
    tweets = []
    with open(path, 'r') as jsonl_file:
        lines = jsonl_file.readlines()  # list of strings
        for line in lines:
            if line.strip() != '':
                tweet = json.loads(line)
                if 'delete' not in tweet:
                    tweets.append(tweet)
    return tweets


def write_tsv(path, contents):
    with open(path, mode='w') as tsv_file:
        writer = csv.writer(tsv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in contents:
            writer.writerow(line)


def main():
    args = parse_args()
    tweets = read_jsonl(args.input)
    for tweet in tweets:
        get_info(tweet)
    write_tsv(args.output, list_to_tsv)


if __name__ == '__main__':
    # We don't want to run code if we're importing this as a library. So, this block
    # will only run if this is the main file that we're running from
    main()
