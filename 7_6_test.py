import csv
import argparse
import json
import io
from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')

list_to_csv = []

def get_nlp_info(tweet):
        #entities, parts of speech
        result = nlp.annotate(tweet['text'],
                              properties={
                                  'annotators': 'sentiment, ner, pos',
                                  'outputFormat': 'json',
                                  'timeout': 1000,
                              })
        entities = []
        pos = []
        s_exp = []

        index = 0

        if 'sentences' in tweet:
            for s in result['sentences']:
                for t in s['tokens']:
                    index += 1 #index starts with 1, not 0
                    if t['ner'] != 'O':
                        entities.append([t['ner'], index])

            for s in result['sentences']:
                for t in s['tokens']:
                    pos.append(t['pos'])

            for s in result['sentences']:
                s_exp.append(s['sentimentTree'])

        return entities, pos, s_exp

def get_text(tweet):
    if 'text' in tweet:
        raw_text = tweet['text']
        words = raw_text.split()
        punctuation = "!#$%&()*+,./:;<=>?@[\]^_`{|}~"
        table = str.maketrans('', '', punctuation)
        tokenized_text = [w.translate(table) for w in words]

    text = raw_text.encode(encoding = "UTF-8", errors = "ignore")
    return raw_text, tokenized_text

def get_party(tweet):
    all_dem = str(open("E:\\bipartisanship\\dem_combined.txt", 'r'))
    all_rep = str(open("E:\\bipartisanship\\rep_combined.txt", 'r'))
    dem_count = all_dem.count(str(tweet["user"]["id"]))
    rep_count = all_rep.count(str(tweet["user"]["id"]))

    party = ""
    if dem_count > rep_count:
        party = "democrat"
    elif rep_count > dem_count:
        party = "republican"
    else:
        party = "neutral"

    return party


def append_info(tweet):
    #Text, Tokenized Text, User ID, Following, Creation Date, Political Party, Entities [entity, index], Parts Of Speech, Sentiment Tree S-expression
    addition_list = []

    entities, pos, s_exp = get_nlp_info(tweet)
    text, tokenized_text = get_text(tweet)

    addition_list.append(text)
    addition_list.append(tokenized_text)
    addition_list.append(tweet["user"]["id"])
    addition_list.append(tweet["user"]["friends_count"])
    addition_list.append(tweet["created_at"])
    addition_list.append(get_party(tweet))
    addition_list.append(entities)
    addition_list.append(pos)
    addition_list.append(s_exp)

    list_to_csv.append(addition_list)


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
    with io.open(path, 'w', encoding = 'utf-8') as tsv_file:
        writer = csv.writer(tsv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for line in contents:
            writer.writerow(line)


def main():
    args = parse_args()
    tweets = read_jsonl(args.input)
    for tweet in tweets:
        append_info(tweet)
    write_tsv(args.output, list_to_csv)


if __name__ == '__main__':
    # We don't want to run code if we're importing this as a library. So, this block
    # will only run if this is the main file that we're running from
    main()
