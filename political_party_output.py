import tweepy
import csv

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

t = {"created_at":"Mon Apr 06 07:30:47 +0000 2020","id":1247064193255137280,"id_str":"1247064193255137280","text":"\u53cb\u4eba\u3092\u6301\u3064\u3068\u3044\u3046\u3053\u3068\u306f\u3001\u5e78\u798f\u306a\u3053\u3068\u3060\u3002\n\n\uff08\u30ca\u30dd\u30ec\u30aa\u30f3\u30fb\u30dc\u30ca\u30d1\u30eb\u30c8\/\u30d5\u30e9\u30f3\u30b9\u306e\u8ecd\u4eba\uff65\u653f\u6cbb\u5bb6\uff65\u7687\u5e1d\uff09","source":"\u003ca href=\"http:\/\/twittbot.net\/\" rel=\"nofollow\"\u003etwittbot.net\u003c\/a\u003e","truncated":false,"in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":1472777335,"id_str":"1472777335","name":"\u596e\u3044\u7acb\u305f\u305b\u3066\u304f\u308c\u308b\u8a00\u8449_bot","screen_name":"meigen_009","location":null,"url":null,"description":"\u596e\u3044\u7acb\u305f\u305b\u3066\u304f\u308c\u308b\u8a00\u8449\u306ebot\u3067\u3059\u3002\r\nYouTube\u306b\u300c\u596e\u3044\u7acb\u305f\u305b\u3066\u304f\u308c\u308b\u8a00\u8449\u300d\u3082\u8f09\u305b\u3066\u3044\u307e\u3059\u3002\r\nhttps:\/\/www.youtube.com\/watch?v=pwoopZyCzzg","translator_type":"none","protected":false,"verified":false,"followers_count":359,"friends_count":552,"listed_count":7,"favourites_count":0,"statuses_count":52892,"created_at":"Fri May 31 18:12:04 +0000 2013","utc_offset":null,"time_zone":null,"geo_enabled":false,"lang":null,"contributors_enabled":false,"is_translator":false,"profile_background_color":"C0DEED","profile_background_image_url":"http:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png","profile_background_image_url_https":"https:\/\/abs.twimg.com\/images\/themes\/theme1\/bg.png","profile_background_tile":false,"profile_link_color":"1DA1F2","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"profile_image_url":"http:\/\/pbs.twimg.com\/profile_images\/3737220773\/a8b146a4c0e1ad0d91c96f76eda33ad7_normal.jpeg","profile_image_url_https":"https:\/\/pbs.twimg.com\/profile_images\/3737220773\/a8b146a4c0e1ad0d91c96f76eda33ad7_normal.jpeg","default_profile":true,"default_profile_image":false,"following":null,"follow_request_sent":null,"notifications":null},"geo":null,"coordinates":null,"place":null,"contributors":null,"is_quote_status":false,"quote_count":0,"reply_count":0,"retweet_count":0,"favorite_count":0,"entities":{"hashtags":[],"urls":[],"user_mentions":[],"symbols":[]},"favorited":false,"retweeted":false,"filter_level":"low","lang":"ja","timestamp_ms":"1586158247661"}


# file = open("tweet_corpus.txt", "r")   #tweet_corpus.txt isn't real, just an arbitrary file name or placeholer

print('step 2')


def political_leaning(tweet):
    dem_count = 0
    rep_count = 0

    username = tweet["user"]["screen_name"]
    user_follow_list = []
    # for loop: aid taken from 'jschnurr' (stackoverflow.com)
    print(username)
    i = 0
    for user in tweepy.Cursor(api.friends, screen_name=str(username), count = 200).items():
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
    text = tweet['text']
    words = text.split()
    punctuation = "!#$%&()*+,./:;<=>?@[\]^_`{|}~"
    table = str.maketrans('', '', punctuation)
    tokenized_text = [w.translate(table) for w in words]

    political_party = ""
    if dem_count > rep_count:
        political_party = 'democrat'
    elif rep_count > dem_count:
        political_party = 'republican'
    else:
        political_party = 'neutral'

    addition_list = []
    addition_list.append(tweet["user"]["id"])
    addition_list.append(tweet["user"]["friends_count"])
    addition_list.append(dem_count)
    addition_list.append(rep_count)
    addition_list.append(tweet["created_at"])
    addition_list.append(political_party)
    addition_list.append(text)
    addition_list.append(tokenized_text)



    list_to_tsv.append(addition_list)

print('step 3')

political_leaning(t)

print('step 4')
"""
with open('output6_11.tsv', 'wt') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    for i in range(len(list_to_tsv)):
        tsv_writer.writerow(list_to_tsv[i])
"""
print(list_to_tsv)
