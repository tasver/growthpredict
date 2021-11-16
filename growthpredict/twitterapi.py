import csv
import os
from growthpredict import models,db
from growthpredict.models import Post_twit, TopicPosts_twit
from growthpredict.settings import engine
#from growthpredict.routes import add_topic

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


def write_csv(username,filename_main=None):
    parse_id_and_foll_username(username)
    tweet_user_id, followers = get_id_foll()
    get_tweets_by_id(tweet_user_id)
    #filename_main
    with open('growthpredict/tmp/filtered_data_file.json', 'r') as f:
        json_obj = json.loads(f.read())
        # df = pd.DataFrame(json_obj['data'])
        # print(df)
        # test = json_obj['data'][0]
        real_number_posts = json_obj['meta']['result_count']
        if filename_main:
            filename=filename_main
        else:
            filename = 'growthpredict/tmp/' + username + "twitter" + ".csv"

        with open(filename, 'w') as csvfile:
            fieldnames = ['username', 'author_id', 'tweet_id', 'tweet_link', 'view_count', 'retweet_count',
                          'reply_count', 'like_count', 'quote_count', 'followers']
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
            writer.writeheader()
            n = 0
            media_n = 0
            #print("**********************************")
            try:
                while n < real_number_posts:
                    author_id = json_obj['data'][n]['author_id']
                    tweet_id = json_obj['data'][n]['id']
                    tweet_link = link_twitter + str(author_id) + "/status/" + str(tweet_id)
                    retweet_count = json_obj['data'][n]['public_metrics']['retweet_count']
                    reply_count = json_obj['data'][n]['public_metrics']['reply_count']
                    like_count = json_obj['data'][n]['public_metrics']['like_count']
                    quote_count = json_obj['data'][n]['public_metrics']['quote_count']
                    #print(followers, author_id, tweet_id, tweet_link, retweet_count, reply_count, like_count,
                    #      quote_count)
                    try:
                        list_medias = json_obj['data'][n]['attachments']['media_keys']
                        #print(list_medias)

                        for media in list_medias:

                            #print(media)
                            # media_n = len(list_medias)
                            #print(media_n)
                            # print(json_obj['includes']['media'].get(media_n))
                            if json_obj['includes']['media'][media_n]['type'] == 'video':
                                view_count = json_obj['includes']['media'][media_n]['public_metrics']['view_count']
                                #print("this is video")
                                #print(view_count)
                                #print(media)
                            else:
                                view_count = 0
                                #print(view_count)
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
                    #print(n)

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
                    #print(test_dict)
            except ValueError:
                "something went wrong"
            n = 0
        #print(test_dict)


def read_from_file(filename):
    list_usernames = []
    with open(filename, 'r') as filehandle:
        for line in filehandle:
            current_username = line[:-1]
            list_usernames.append(current_username)
    return list_usernames


bd_dict = {
    'username': '',
    'avg_view': 0,
    'avg_like': 0,
    'avg_retwwet': 0,
    'avg_reply': 0,
    'avg_quote': 0,
    'media': 0,
    'avg_er': 0,
    'growth': 0,
    'followers': 0,
    'growth_predict': 0

}
filename = 'test1.csv'
import pandas as pd


def get_avg_without_media_growth(filename, obj_topic):
    data = pd.read_csv(filename)
    # print(data)
    average_data = data.groupby('username').mean()
    # print(average_data)
    # @av_data = average_data.transform(0)

    # print(av_data)
    for elem in average_data.iterrows():
        # print(elem)
        bd_dict_int = {
            'username': elem[0],
            'avg_view': int(round(elem[1][2])),
            'avg_like': int(round(elem[1][5])),
            'avg_retwwet': int(round(elem[1][3])),
            'avg_reply': int(round(elem[1][4])),
            'avg_quote': int(round(elem[1][6])),
            'media': 0,
            'avg_er': int(round((elem[1][5] + elem[1][3] + elem[1][4] + elem[1][6]) / elem[1][7] * 100)),
            'growth': 0,
            'followers': int(round(elem[1][7])),
            'growth_predict': 0
        }
        bd_dict1 = {
            'username': elem[0],
            'avg_view': elem[1][2],
            'avg_like': elem[1][5],
            'avg_retwwet': elem[1][3],
            'avg_reply': elem[1][4],
            'avg_quote': elem[1][6],
            'media': 0,
            'avg_er': (elem[1][5] + elem[1][3] + elem[1][4] + elem[1][6]) / elem[1][7] * 100,
            'growth': 0,
            'followers': elem[1][7],
            'growth_predict': 0
        }
        #print(bd_dict1)
        object_twit_elem = Post_twit(username=elem[0],
                                     avg_view_count=elem[1][2],
                                     avg_retweet_count = elem[1][3],
                                     avg_reply_count = elem[1][4],
                                     avg_like_count = elem[1][5],
                                     avg_quote_count = elem[1][6],
                                     media = 0,
                                     avg_er = (elem[1][5] + elem[1][3] + elem[1][4] + elem[1][6]) / elem[1][7] * 100,
                                     growth = 0,
                                     growth_predict = 0,
                                     followers = elem[1][7]
        )
        obj_topic.usernames.append(object_twit_elem)
        #db.session.add(object_twit_elem)

    db.session.add(obj_topic)
    db.session.commit()

def get_avg_without_media_growth_without_saving(filename):
    data = pd.read_csv(filename)
    average_data = data.groupby('username').mean()
    for elem in average_data.iterrows():

        bd_dict1 = {
            'username': elem[0],
            'RETWEETav': elem[1][3],
            'REPLYav': elem[1][4],
            'LIKEav': elem[1][5],
            'QUOTEav': elem[1][6],
            'followers': elem[1][7],
            'growth': 0,
        }
    return bd_dict1

def get_avg_with_media_gowth(filename):
    data = pd.read_csv(filename)
    # print(data)
    average_data = data.groupby('username').mean()
    # print(average_data)
    # @av_data = average_data.transform(0)

    # print(av_data)
    for elem in average_data.iterrows():
        # print(elem)
        bd_dict_int = {
            'username': elem[0],
            'avg_view': int(round(elem[1][2])),
            'avg_like': int(round(elem[1][5])),
            'avg_retwwet': int(round(elem[1][3])),
            'avg_reply': int(round(elem[1][4])),
            'avg_quote': int(round(elem[1][6])),
            'media': 0,
            'avg_er': int(round((elem[1][5] + elem[1][3] + elem[1][4] + elem[1][6]) / elem[1][7] * 100)),
            'growth': 0,
            'followers': int(round(elem[1][7])),
            'growth_predict': 0
        }
        bd_dict1 = {
            'username': elem[0],
            'avg_view': elem[1][2],
            'avg_like': elem[1][5],
            'avg_retwwet': elem[1][3],
            'avg_reply': elem[1][4],
            'avg_quote': elem[1][6],
            'media': 0,
            'avg_er': (elem[1][5] + elem[1][3] + elem[1][4] + elem[1][6]) / elem[1][7] * 100,
            'growth': 0,
            'followers': elem[1][7],
            'growth_predict': 0
        }
        print(bd_dict1)

from os import environ
from sqlalchemy import create_engine
#filename2 = 'test_twitter_file_for.csv'


def normalising_data_and_create_scale_from_file(filename):
    data = pd.read_csv(filename, encoding='unicode_escape')
    # print(data)
    # print(type(data.RETWEETav))
    data2 = data.drop(data.index[data['RETWEETav'] < 1])
    data2 = data2.drop(data2.index[data2['REPLYav'] < 1])
    data2 = data2.drop(data2.index[data2['LIKEav'] < 1])
    data2 = data2.drop(data2.index[data2['QUOTEav'] < 1])
    data2 = data2.drop(data2.index[data2['ERaverage'] < 0])
    data2 = data2.drop(data2.index[data2['growth'] < 1])
    # data2 = data2.drop(data2.index[data2['QUOTEav'] < 1])
    new_scale = data2.drop('REPLYav', axis=1)
    new_scale = new_scale.drop('LIKEav', axis=1)
    new_scale = new_scale.drop('QUOTEav', axis=1)
    new_scale = new_scale.drop('ERaverage', axis=1)
    new_scale = new_scale.drop('RETWEETav', axis=1)
    new_scale = new_scale.drop('media', axis=1)
    new_scale_growth_precent = new_scale['growth'] / new_scale['followers'] * 100
    new_scale_growth_precent = new_scale_growth_precent.sort_values()
    percent_to_delete = int(len(new_scale_growth_precent) - 0.05 * len(new_scale_growth_precent))
    print(percent_to_delete)
    print(new_scale_growth_precent)
    scale = new_scale_growth_precent[0:percent_to_delete - 1]
    print(scale)
    max_of_scale = scale.max()
    print(max_of_scale)
    # new_scale = new_scale.drop('followers', axis=1)
    # print(new_scale)
    # rint(data2)

    return data2, scale, max_of_scale


def normalising_data_and_create_scale_from_db(data):
    data = data
    # print(data)
    # print(type(data.RETWEETav))
    data2 = data.drop(data.index[data['RETWEETav'] < 1])
    data2 = data2.drop(data2.index[data2['REPLYav'] < 1])
    data2 = data2.drop(data2.index[data2['LIKEav'] < 1])
    data2 = data2.drop(data2.index[data2['QUOTEav'] < 1])
    data2 = data2.drop(data2.index[data2['ERaverage'] < 0])
    data2 = data2.drop(data2.index[data2['growth'] < 1])
    # data2 = data2.drop(data2.index[data2['QUOTEav'] < 1])
    new_scale = data2.drop('REPLYav', axis=1)
    new_scale = new_scale.drop('LIKEav', axis=1)
    new_scale = new_scale.drop('QUOTEav', axis=1)
    new_scale = new_scale.drop('ERaverage', axis=1)
    new_scale = new_scale.drop('RETWEETav', axis=1)
    new_scale = new_scale.drop('media', axis=1)
    new_scale_growth_precent = new_scale['growth'] / new_scale['followers'] * 100
    new_scale_growth_precent = new_scale_growth_precent.sort_values()
    percent_to_delete = int(len(new_scale_growth_precent) - 0.05 * len(new_scale_growth_precent))
    print(percent_to_delete)
    print(new_scale_growth_precent)
    scale = new_scale_growth_precent[0:percent_to_delete - 1]
    print(scale)
    max_of_scale = scale.max()
    print(max_of_scale)
    # new_scale = new_scale.drop('followers', axis=1)
    # print(new_scale)
    # rint(data2)

    return data2, scale, max_of_scale

#normalising_data_and_create_scale(filename2)

from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures


def create_poly2_model_from_file(filename):
    df = pd.read_csv(filename)
    #one_for_test = pd.read_csv('test_1twitter.csv')
    X = df.drop('growth', axis=1)
    X = X.drop('username', axis=1)
    # X = X.drop('RETWEETav',axis=1)
    X = X.drop('REPLYav', axis=1)
    # X = X.drop('LIKEav',axis=1)
    X = X.drop('QUOTEav', axis=1)
    #Y_one = one_for_test['growth']
    #X_one = one_for_test.drop('growth', axis=1)
    #X_one = X_one.drop('username', axis=1)
    #X_one = X_one.drop('REPLYav', axis=1)
    #X_one = X_one.drop('QUOTEav', axis=1)

    Y = df['growth']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=100)

    poly = PolynomialFeatures(2)

    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.fit_transform(X_test)

    #X_one_poly = poly.transform(X_one)
    X_ = poly.transform(X)

    model_with_poly = linear_model.LinearRegression()
    model_with_poly.fit(X_train_poly, Y_train)

    print(model_with_poly.score(X_,Y))
    print(model_with_poly.score(X_train_poly, Y_train))
    print(model_with_poly.score(X_test_poly, Y_test))

    print('success create')
    return model_with_poly, poly


def create_poly2_model_from_bd(data):
    df = data
    #one_for_test = pd.read_csv('test_1twitter.csv')
    X = df.drop('growth', axis=1)
    X = X.drop('username', axis=1)
    # X = X.drop('RETWEETav',axis=1)
    X = X.drop('REPLYav', axis=1)
    # X = X.drop('LIKEav',axis=1)
    X = X.drop('QUOTEav', axis=1)
    X = X.drop('media', axis=1)
    X = X.drop('ERaverage', axis=1)
    #Y_one = one_for_test['growth']
    #X_one = one_for_test.drop('growth', axis=1)
    #X_one = X_one.drop('username', axis=1)
    #X_one = X_one.drop('REPLYav', axis=1)
    #X_one = X_one.drop('QUOTEav', axis=1)

    Y = df['growth']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=100)

    poly = PolynomialFeatures(2)

    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.fit_transform(X_test)

    #X_one_poly = poly.transform(X_one)
    X_ = poly.transform(X)

    model_with_poly = linear_model.LinearRegression()
    model_with_poly.fit(X_train_poly, Y_train)
    print('success create')
    print(model_with_poly.score(X_, Y))
    print(model_with_poly.score(X_train_poly, Y_train))
    print(model_with_poly.score(X_test_poly, Y_test))

    return model_with_poly, poly

#test_model, test_poly = create_poly2_model("TWITTER_TEST_csv.csv")


def use_poly2_model(input, model, poly):
    one_for_test = pd.read_csv(input)
    Y_one = one_for_test['growth']
    X_one = one_for_test.drop('growth', axis=1)
    X_one = X_one.drop('username', axis=1)
    X_one = X_one.drop('REPLYav', axis=1)
    X_one = X_one.drop('QUOTEav', axis=1)
    print("i workedhere")
    X_one_poly = poly.transform(X_one)
    print("i worked here")
    test = model.predict(X_one_poly)
    print("i worked hereeeeee")
    return test


#print(use_poly2_model('test_1twitter.csv', test_model, test_poly))


def create_linear_model_from_file(filename):
    df = pd.read_csv(filename)
    #one_for_test = pd.read_csv('test_1twitter.csv')
    # delaney_descriptors_df = pd.read_csv('TWITTER_TEST_csv_0media.csv')
    # df.drop('media', axis=1)
    # df.drop('ERaverage', axis=1)

    X = df.drop('growth', axis=1)
    X = X.drop('username', axis=1)
    # X = X.drop('RETWEETav',axis=1)
    X = X.drop('REPLYav', axis=1)
    # X = X.drop('LIKEav',axis=1)
    X = X.drop('QUOTEav', axis=1)
    #Y_one = one_for_test['growth']
    #X_one = one_for_test.drop('growth', axis=1)
    #X_one = X_one.drop('username', axis=1)
    #X_one = X_one.drop('REPLYav', axis=1)
    #X_one = X_one.drop('QUOTEav', axis=1)
    Y = df['growth']

    corr = df.corr()
    #corr

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=100)

    model = linear_model.LinearRegression()
    model.fit(X_train, Y_train)

    Y_pred_train = model.predict(X_train)
    # print('Coefficients:', model.coef_)
    # print('Intercept:', model.intercept_)
    # print('Mean squared error (MSE): %.2f'
    #    % mean_squared_error(Y_train, Y_pred_train))
    print('Coefficient of determination (R^2): %.2f'
        % r2_score(Y_train, Y_pred_train))
    Y_pred_test = model.predict(X_test)
    # print('Coefficients:', model.coef_)
    # print('Intercept:', model.intercept_)
    # print('Mean squared error (MSE): %.2f'
    #    % mean_squared_error(Y_test, Y_pred_test))
    print('Coefficient of determination (R^2): %.2f'
        % r2_score(Y_test, Y_pred_test))
    print("linear model success created")
    return model

def create_linear_model_from_bd(data):
    df = data
    #one_for_test = pd.read_csv('test_1twitter.csv')

    X = df.drop('growth', axis=1)
    X = X.drop('username', axis=1)
    # X = X.drop('RETWEETav',axis=1)
    X = X.drop('REPLYav', axis=1)
    # X = X.drop('LIKEav',axis=1)
    X = X.drop('QUOTEav', axis=1)
    X = X.drop('media', axis=1)
    X = X.drop('ERaverage', axis=1)
    #Y_one = one_for_test['growth']
    #X_one = one_for_test.drop('growth', axis=1)
    #X_one = X_one.drop('username', axis=1)
    #X_one = X_one.drop('REPLYav', axis=1)
    #X_one = X_one.drop('QUOTEav', axis=1)
    Y = df['growth']

    corr = df.corr()
    #corr

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=100)

    model = linear_model.LinearRegression()
    model.fit(X_train, Y_train)

    Y_pred_train = model.predict(X_train)
    print('Coefficient of determination (R^2): %.2f'
          % r2_score(Y_train, Y_pred_train))
    Y_pred_test = model.predict(X_test)
    print('Coefficient of determination (R^2): %.2f'
          % r2_score(Y_test, Y_pred_test))

    print("linear model success created")
    return model
#test_linear_model = create_linear_model('TWITTER_TEST_csv.csv')


def use_linear_model(input, model):
    one_for_test = pd.read_csv(input)
    Y_one = one_for_test['growth']
    X_one = one_for_test.drop('growth', axis=1)
    X_one = X_one.drop('username', axis=1)
    X_one = X_one.drop('REPLYav', axis=1)
    X_one = X_one.drop('QUOTEav', axis=1)
    test = model.predict(X_one)
    return test



#print(use_linear_model('test_1twitter.csv', test_linear_model))


def create_scale_and_detecting_quality(max_of_scale,our_growth):
    quality = ''
    if our_growth >= max_of_scale:
        quality = "Fantastic growth"
        return quality
    elif our_growth >=0.618*max_of_scale and our_growth<max_of_scale:
        quality = "Very good growth"
        return quality
    elif our_growth >=0.382*max_of_scale and our_growth<max_of_scale*0.618:
        quality = "Good growth"
        return quality
    elif our_growth >=0.236*max_of_scale and our_growth<max_of_scale*0.382:
        quality = "Normal growth"
        return quality
    elif our_growth >=0.146*max_of_scale and our_growth<max_of_scale*0.236:
        quality = "Bad growth"
        return quality
    elif our_growth<max_of_scale*0.146:
        quality = "Very bad growth"
        return quality



"""
yintercept = '%.2f' % model.intercept_
growth = '%.4f * growth ' % model.coef_[0]
followers = '%.4f * followers' % model.coef_[1]
RETWEETav = '%.4f * RETWEETav' % model.coef_[2]
REPLYav = '%.4f * REPLYav' % model.coef_[3]
LIKEav = '%.4f * LIKEav' % model.coef_[4]
QUOTEav = '%.4f * QUOTEav' % model.coef_[4]

print('Predict_Linear_regeression = '  + 
      ' ' + 
      growth + 
      ' + ' + 
      followers + 
      ' + ' + 
      RETWEETav + 
      ' + ' + 
      REPLYav + 
      ' + ' +
      LIKEav +
      ' + ' +
      QUOTEav)
"""



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
