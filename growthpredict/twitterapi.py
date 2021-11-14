import csv
import os

import requests
import json

# BEARER_TOKEN = os.getenv('BEARER_TOKEN')
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACY9UQEAAAAAkhiCN7skBcGtLcyfcMLhuTe82NE%3DFA3DMi5QzbKIW1IHKE0RJAnQilzXbQBLRjMKz6S6T4epT8D526"

headers = {
    'Authorization': f"Bearer {BEARER_TOKEN}",
}
max_result = 60
params = (
    ('max_results', f'{max_result}'),
    ('tweet.fields', 'public_metrics'),
    ('expansions', 'author_id,attachments.media_keys'),
    ('user.fields', 'username'),
    ('media.fields', 'public_metrics'),

)
params_get_foll = (
    ('user.fields', 'public_metrics'),

)

# print(get_followers)
# test_json = json.dumps(get_followers)
# print(test_json)

# pretty_json = json.loads(response.text)
# print (json.dumps(pretty_json, indent=4))


# response_wrong = requests.get('https://api.twitter.com/2/users/14872237/liked_tweets', headers=headers, params=params)
# pretty_json = json.loads(get_followers.text)
# print (json.dumps(pretty_json, indent=4))

header = ['retweet_count', 'reply_count', 'like_count', 'quote_count']
link_twitter = 'https://twitter.com/'
test_dict = {
    'username': '',
    'author_id': 0,
    'tweet_id': 0,
    'tweet_link': '',
    'view_count': 0,
    'retweet_count': 0,
    'reply_count': 0,
    'like_count': 0,
    'quote_count': 0,
    'followers': 0

}


def parse_id_and_foll_username(username):
    tmp_link = f'https://api.twitter.com/2/users/by/username/{username}'
    get_followers = requests.get(tmp_link, headers=headers, params=params_get_foll)
    with open("growthpredict/tmp/data_with_id_andfollowers.json", "w") as data_file:
        pretty_json = json.loads(get_followers.text)
        json.dump(pretty_json, data_file, indent=4)


def get_tweets_by_id(id):
    with open("growthpredict/tmp/filtered_data_file.json", "w") as data_file:
        response = requests.get(f'https://api.twitter.com/2/users/{id}/tweets', headers=headers, params=params)

        pretty_json2 = json.loads(response.text)

        json.dump(pretty_json2, data_file, indent=4)


def get_id_foll():
    with open('growthpredict/tmp/data_with_id_andfollowers.json', 'r') as f:
        json_obj = json.loads(f.read())
        followers = json_obj['data']['public_metrics']['followers_count']
        tweet_user_id = json_obj['data']['id']
    return tweet_user_id, followers


def write_csv(username):
    parse_id_and_foll_username(username)
    tweet_user_id, followers = get_id_foll()
    get_tweets_by_id(tweet_user_id)

    with open('growthpredict/tmp/filtered_data_file.json', 'r') as f:
        json_obj = json.loads(f.read())
        # df = pd.DataFrame(json_obj['data'])
        # print(df)
        # test = json_obj['data'][0]
        real_number_posts = json_obj['meta']['result_count']

        filename = username + "twitter" + ".csv"
        with open(filename, 'w') as csvfile:
            fieldnames = ['username', 'author_id', 'tweet_id', 'tweet_link', 'view_count', 'retweet_count',
                          'reply_count', 'like_count', 'quote_count', 'followers']
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            n = 0
            media_n = 0
            print("**********************************")
            try:
                while n < real_number_posts:
                    author_id = json_obj['data'][n]['author_id']
                    tweet_id = json_obj['data'][n]['id']
                    tweet_link = link_twitter + str(author_id) + "/status/" + str(tweet_id)
                    retweet_count = json_obj['data'][n]['public_metrics']['retweet_count']
                    reply_count = json_obj['data'][n]['public_metrics']['reply_count']
                    like_count = json_obj['data'][n]['public_metrics']['like_count']
                    quote_count = json_obj['data'][n]['public_metrics']['quote_count']
                    print(followers, author_id, tweet_id, tweet_link, retweet_count, reply_count, like_count,
                          quote_count)
                    try:
                        list_medias = json_obj['data'][n]['attachments']['media_keys']
                        print(list_medias)

                        for media in list_medias:

                            print(media)
                            # media_n = len(list_medias)
                            print(media_n)
                            # print(json_obj['includes']['media'].get(media_n))
                            if json_obj['includes']['media'][media_n]['type'] == 'video':
                                view_count = json_obj['includes']['media'][media_n]['public_metrics']['view_count']
                                print("this is video")
                                print(view_count)
                                print(media)
                            else:
                                view_count = 0
                                print(view_count)
                            media_n = media_n + 1
                            # print(view_count)

                    except:
                        view_count = 0

                    new_elem = {
                        'username': username,
                        'author_id': author_id,
                        'tweet_id': tweet_id,
                        'tweet_link': tweet_link,
                        'view_count': view_count,
                        'retweet_count': retweet_count,
                        'reply_count': reply_count,
                        'like_count': like_count,
                        'quote_count': quote_count,
                        'followers': followers
                    }
                    test_dict.update(new_elem)
                    writer.writerow(new_elem)
                    n = n + 1
                    print(n)

            except ValueError:
                "something went wrong"


def write_many(usernames, filename):
    with open(filename, 'w') as csvfile:
        fieldnames = ['username', 'author_id', 'tweet_id', 'tweet_link', 'view_count', 'retweet_count', 'reply_count',
                      'like_count', 'quote_count', 'followers']
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        n = 0
        media_n = 0
        for username in usernames:

            print(username)
            try:
                parse_id_and_foll_username(username)
            except:
                print('parse error. Can not parse id and foll')
            try:
                tweet_user_id, followers = get_id_foll()
                print(tweet_user_id)
            except:
                print('parse error. Can not parse id')
            try:
                get_tweets_by_id(tweet_user_id)
            except:
                print('parse error. Can not found tweets')

            print()

            with open('growthpredict/tmp/filtered_data_file.json', 'r') as f:
                json_obj = json.loads(f.read())
                real_number_posts = json_obj['meta']['result_count']

            try:
                while n < max_result - 10 and n < real_number_posts:
                    author_id = json_obj['data'][n]['author_id']
                    tweet_id = json_obj['data'][n]['id']
                    tweet_link = link_twitter + str(author_id) + "/status/" + str(tweet_id)
                    retweet_count = json_obj['data'][n]['public_metrics']['retweet_count']
                    reply_count = json_obj['data'][n]['public_metrics']['reply_count']
                    like_count = json_obj['data'][n]['public_metrics']['like_count']
                    quote_count = json_obj['data'][n]['public_metrics']['quote_count']
                    # print(followers,author_id,tweet_id,tweet_link,retweet_count,reply_count,like_count,quote_count)
                    try:
                        list_medias = json_obj['data'][n]['attachments']['media_keys']
                        # print(list_medias)

                        for media in list_medias:

                            # print(media)
                            # media_n = len(list_medias)
                            # print(media_n)
                            # print(json_obj['includes']['media'].get(media_n))
                            if json_obj['includes']['media'][media_n]['type'] == 'video':
                                view_count = json_obj['includes']['media'][media_n]['public_metrics']['view_count']
                                # print("this is video")
                                # print(view_count)
                                # print(media)
                            else:
                                view_count = 0
                                # print(view_count)
                            media_n = media_n + 1
                        # print(view_count)
                    except:
                        view_count = 0
                    new_elem = {
                        'username': username,
                        'author_id': author_id,
                        'tweet_id': tweet_id,
                        'tweet_link': tweet_link,
                        'view_count': view_count,
                        'retweet_count': retweet_count,
                        'reply_count': reply_count,
                        'like_count': like_count,
                        'quote_count': quote_count,
                        'followers': followers
                    }
                    test_dict.update(new_elem)
                    writer.writerow(new_elem)
                    n = n + 1
                    print(test_dict)
            except ValueError:
                "something went wrong"
            n = 0
        print(test_dict)


def read_from_file(filename):
    list_usernames = []
    with open(filename, 'r') as filehandle:
        for line in filehandle:
            current_username = line[:-1]
            list_usernames.append(current_username)
    return list_usernames

#usernames = read_from_file('twitter_eng_151_200.txt')
#write_many(usernames, 'twitter_eng_all_test4.csv')






# username = 'BNavrotsky'
# write_csv(username)


# write_csv('realmadrid')
# write_csv('LFC')
# test = df['public_metrics']
# test = test.to_dict()
# print(test)
# test = pd.DataFrame.from_dict(test, orient='index')
# print(test)
# test2 = test.DataFrame(json_obj['public_metrics'])
# print(test2)
# test.to_csv (r'test.csv', columns = header)
# with open('test.json', 'r') as f:
# json_obj = json.loads(f.read())
# df = pd.DataFrame(json_obj['data'])
# df.to_csv (r'test.csv')
# df.index.name = None

# 14872237
