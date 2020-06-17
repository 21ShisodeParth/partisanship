import tweepy
import csv

with open('output6_11.tsv', 'wt') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow('hello')

list_to_tsv = []

access_token = "..."
access_token_secret = "..."
consumer_key = "..."
consumer_secret = "..."

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#aid from 'jschnurr' (stackoverflow.com)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

print('step 1')

true, false, null = True, False, None

dems_file = open("all_dems.txt", "r")
reps_file = open("all_reps.txt", "r")

dems = []
reps = []

for line in dems_file:
    element = line.strip()
    dems.append(element)

for line in reps_file:
    element = line.strip()
    reps.append(element)

t = open('tweet_sample.txt', 'r')

# file = open("tweet_corpus.txt", "r")   #tweet_corpus.txt isn't real, just an arbitrary file name or placeholer

print('step 2')


def political_leaning(tweet):
    dem_count = 0
    rep_count = 0

    username = tweet["user"]["screen_name"]
    user_follow_list = []
    add_list = []
    # for loop: aid taken from 'jschnurr' (stackoverflow.com)
    print(username)
    i = 0
    for user in tweepy.Cursor(api.friends, screen_name=str(username), count = 400).items():
        i += 1
        print(user.screen_name, i)
        user_follow_list.append(user.screen_name)
    print(user_follow_list)

    add_list.append(tweet['text'])

    for p in user_follow_list:
        for d in dems:
            if p == d:
                dem_count += 1
        for r in reps:
            if p == r:
                rep_count += 1

    # change print statements to something meaningful to the project later
    add_list = [tweet['text'], tweet["user"]["id"]]

    if dem_count > rep_count:
        add_list.append('democrat')
    elif rep_count > dem_count:
        add_list.append('republican')
    else:
        add_list.append('neutral')

    list_to_tsv.append(add_list)

print('step 3')

for line in t:
    l = t.readline()
    political_leaning(l)

print('step 4')

with open('output6_11.tsv', 'wt') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    for i in range(len(list_to_tsv)):
        tsv_writer.writerow(list_to_tsv[i])

print('finished')

#metadata: number followers, account created, tweet id
