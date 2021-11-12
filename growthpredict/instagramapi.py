from instagrapi import Client
import csv
import re
import math
from random import randint
from time import sleep


inst_url = "https://www.instagram.com/p/"
login = "dota2_fun_moments"
password = "test_pas_1"

username = "nba"
usernames = ["nba", "skysports", "atalantabc", "footballuablog", "uafukraine", "championsleague", "theukrfoot",
             "realmadrid"]

cl = Client()
cl.login(login, password)

pks = []
ids = []
codes = []
links = []
views = []
likers = []
commenters = []

number_medias = 50

data_dict = {
    'pk': 0,
    'id': 0,
    'code': 'test',
    'link': 'link',
    'views': 0,
    'likers': 0,
    'commenters': 0,
    'followers': 0
}


def get_following(username, filename):
    user_id = cl.user_id_from_username(username)
    dict_following = cl.user_following(user_id)
    # print(dict_following)
    usernames = []
    n = 0
    with open(filename, "w") as data_file:
        data_file.write(str(dict_following))
    # for name in dict_following:
    #    testname = cl.username_from_user_id(name)
    # print(name[username])
    #    print(testname)
    #    print(n)
    #    usernames.append(testname)
    #    n = n+1
    # usernames.append(name.username)
    # print(username)
    return dict_following


def read_usernames_by_following_id(filename):
    with open(filename, 'r') as readfile:
        # json_obj = json.loads(readfile.read())
        # followers = json_obj['data']['public_metrics']['followers_count']
        # tweet_user_id = json_obj['data']['id']

        total = readfile.read()
        print(total.count('username'))
        print("success")
        result1 = re.findall(r"username='\w+'", total)
        result2 = re.findall(r"username='\w+\.\w+'", total)
        result = result1 + result2
        usernames = []
        print(result2)
        # print(result.count(r"username='\w+'"))
        n = 0
        for user in result:
            # print(n)
            username = user[10:-1]
            usernames.append(username)
            # print(username)
            n = n + 1
        print(n)
    return usernames


# test = read_usernames_by_following_id('json_all_following.json')
# print(test)
def write_following_to_file(usernames, filename):
    with open(filename, 'w') as writefile:
        for item in usernames:
            writefile.write("%s\n" % item)


# test1 = get_following('fifaworldcup','json_all_following.json')
# print(test1)

# write_following_to_file(test,'test_from_world_cup.txt')
# print(f"Username is {username}")
# print(f"Count of follower is - {count_follow}")


def split_usernames(filename):
    list_usernames = []
    with open(filename, 'r') as filehandle:
        n = 0

        for line in filehandle:
            current_username = line[:-1]
            list_usernames.append(current_username)
            n = n + 1
        number_split = n / 100
        print(number_split)
        number_split = math.ceil(number_split)
        print(number_split)
        range_unmbersplit = range(0, number_split)
        print(range_unmbersplit)
        # while number_split>0:
        for number in range_unmbersplit:
            with open(f'test/filenames_split_{number}', 'w') as filewriter:
                for elem in list_usernames[number * 100 + 0:number * 100 + 100]:
                    filewriter.write("%s\n" % elem)

    return list_usernames


# split_usernames('test_from_world_cup.txt')


def write_csv_medias_info(username):
    user_id = cl.user_id_from_username(username)
    medias = cl.user_medias(user_id, 20)
    filename = username + ".csv"
    user_info = cl.user_info_by_username(username)
    count_follow = user_info.follower_count

    with open(filename, 'w') as csvfile:
        fieldnames = ['pk', 'id', 'code', 'link', 'views', 'likers', 'commenters', 'followers']
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()

        for media in medias:
            pks.append(media.pk)
            ids.append(media.id)
            codes.append(media.code)
            link = inst_url + media.code
            links.append(link)
            views.append(media.view_count)
            likers.append(media.like_count)
            commenters.append(media.comment_count)
            new_elem = {
                'pk': media.pk,
                'id': media.id,
                'code': media.code,
                'link': link,
                'views': media.view_count,
                'likers': media.like_count,
                'commenters': media.comment_count,
                'followers': count_follow
            }
            data_dict.update(new_elem)
            writer.writerow(new_elem)


def all_usernames(usernames):
    for username in usernames:
        write_csv_medias_info(username)
        print(f"Username {username} is completed")


def write_csv_medias_info_all(usernames, new_file_name):
    with open(new_file_name, 'w') as csvfile:

        fieldnames = ['username', 'pk', 'id', 'code', 'link', 'views', 'likers', 'commenters', 'followers']

        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        n = 0
        for username in usernames:
            sleep(randint(3, 11))
            # writer.writeheader()
            try:
                user_id = cl.user_id_from_username(username)
                medias = cl.user_medias(user_id, number_medias)
                # filename = username +".csv"
                user_info = cl.user_info_by_username(username)
                count_follow = user_info.follower_count
                media_number = 0
                for media in medias:
                    pks.append(media.pk)
                    ids.append(media.id)
                    codes.append(media.code)
                    link = inst_url + media.code
                    links.append(link)
                    views.append(media.view_count)
                    likers.append(media.like_count)
                    commenters.append(media.comment_count)
                    new_elem = {
                        'username': username,
                        'pk': media.pk,
                        'id': media.id,
                        'code': media.code,
                        'link': link,
                        'views': media.view_count,
                        'likers': media.like_count,
                        'commenters': media.comment_count,
                        'followers': count_follow
                    }
                    data_dict.update(new_elem)
                    writer.writerow(new_elem)
                    media_number = media_number + 1
                n = n + 1
                print(f"Username {username} is completed {n}/100 with {media_number} medias")
            except:
                print((f"Username {username} is not finded or not public"))


def read_from_file(filename):
    list_usernames = []
    with open(filename, 'r') as filehandle:
        for line in filehandle:
            current_username = line[:-1]
            list_usernames.append(current_username)
    return list_usernames

#split_n_0 = read_from_file("test/filenames_split_11")
#write_csv_medias_info_all(split_n_0, "split_n_11.csv")






# england_list = read_from_file("England.txt")
# germany_list = read_from_file("Germany.txt")
# italy_list = read_from_file("Italy.txt")
# spain_list = read_from_file("Spain.txt")
# others_list = read_from_file("others.txt")
# ukraine_list = read_from_file("Ukraine.txt")

# print(england_list)
# print(germany_list)
# print(italy_list)
# print(spain_list)

# all_usernames(england_list)


# print(data_dict)
# print(links)
# print(views)
# print(likers)
# print(commenters)

