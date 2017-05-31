import pprint
import math
import os

def gather_data_from_training():
    users = []
    users.append([]) # This is to offset the indexing by one, allows us to just call users[user_id] without needing to
                     # subtract 1.

    with open('train.txt') as f:
        for index, line in enumerate(f):
            split_line = line.split()
            users.append([-1])
            for count, rating in enumerate(split_line):
                users[index+1].append(int(rating))
    return users

def collect_user_preliminary_data(current_file):
    """
    sucking_dict_aint_gay = {
                                'user_id_1': {
                                                '145': 4,
                                                '256': 3,
                                                '465': 2
                                             }
                                'user_id_2': {
                                                '245': 5,
                                                '232':3
                                             }
                            }
    :returns:
        train_users: dictionary containing user info and ratings to base predictions off of
    """
    train_users = {}
    with open (current_file) as f:
        for line in f:
            split_line = line.split(' ')
            try:
                if split_line[2][0:1] != '0':
                    train_users[int(split_line[0])][int(split_line[1])] = int(split_line[2][0:1])
            except Exception as e:
                train_users[int(split_line[0])] = {}
                if split_line[2][0:1] != '0':
                    train_users[int(split_line[0])][int(split_line[1])] = int(split_line[2][0:1])
    return train_users

def generate_cosine_similarity(users, training_data, user_index, train_index):
    # users[user_index] = dictionary of all the ratings they have
    # ex: users[user_index] = {'237': 4, '306': 5, ... , '934': 5}
    train_user_ratings = []
    test_user_ratings  = []
    numerator = 0

    for movie, rating in users[user_index].items():
        train_rating = training_data[int(train_index)][int(movie)]
        if train_rating == 0:
            continue
        else:
            train_user_ratings.append(train_rating)
            test_user_ratings.append(rating)
            numerator += train_rating * rating

    train_den = 0
    test_den = 0
    for i in range(len(test_user_ratings)):
        train_den += train_user_ratings[i] ** 2
        test_den += test_user_ratings[i] ** 2
    if ((math.sqrt(train_den)) * (math.sqrt(test_den))) == 0:
        return 0
    else:
        # Gets rid of the situation where there's only one rating to compare in the cosine similarity process
        # adds 5 to make sure we don't have 0 denominators, also so that it has a lower weight compared to
        # situations where there are more ratings
        if len(train_user_ratings) == 1:
            return 1 / (abs(math.sqrt(train_den) - math.sqrt(test_den)) + 2)
        else:
            return numerator / ((math.sqrt(train_den)) * (math.sqrt(test_den)))

def find_similar_users(test_users, training_users):
    similar_users = {}
    # Similar Users will have the following structure (might be redundant):
    # similar_users = { 'user_id':
    #                       { 'user_with_rating_on_same_movie' : cosine_similarity(user_id, user_with_rating_on_same_movie),
#                             'another_one': cosine_similarity(user_id, another_one),
#                                           .
#                                           .
#                                           .
#                             'final_one' : cosine_similarity(user_id, final_one)
#                           },
#                       'another_real_user':{ etc ... }
#                       }
    for user_id, movies_dict in test_users.items():
        similar_users[user_id] = {}
        for movie, rating in movies_dict.items():
            for train_user_index in range(1,201):
                if training_users[train_user_index][int(movie)] != 0:
                    # Then we can consider their similarity, add them to the list of users who rated the same movies
                    similar_users[user_id][train_user_index] = .4
            for train_user in similar_users[user_id]:
                similar_users[user_id][train_user] = generate_cosine_similarity(test_users, training_users, user_id, train_user)
    # Will get rid of any entry where there's no usable cosine similarity
    for user_id, movies_dict in test_users.items():
        similar_users[user_id]={k:v for k, v in similar_users[user_id].items() if v}
    return similar_users

def traverse_and_write_to_file(train_users, test_users, similar_users, current_file):
    with open ('testestest.txt','w'):
        pass
    with open (current_file) as f:
        for line in f:
            split_line = line.split()
            if split_line[2] == '0':
                split_line[2] = str(generate_rating_for_movie(split_line[1], train_users,
                                                                         split_line[0], similar_users))
            else:
                pass
            with open ('testestest.txt','a') as fo:
                fo.write(str(split_line[0])+' ' +str(split_line[1])+' '+ str(split_line[2])+ '\n')
    os.rename('testestest.txt', current_file)


def generate_rating_for_movie(movie_id, train_users, test_user_id, similar_users):
    numerator = 0
    denominator = 0
    # print(similar_users)
    for test_user, similarity_dict in similar_users.items():
        for similar_user, similarity in similarity_dict.items():
            # print (train_users[int(similar_user)][int(movie_id)])
            if train_users[int(similar_user)][int(movie_id)] == 0:
                continue
            else:
                numerator += train_users[int(similar_user)][int(movie_id)] * similarity
                denominator += similarity
    # print (numerator/denominator)
    if denominator == 0 or int(numerator/denominator) == 0:
        return 1
    return int(numerator / denominator)

def main_loop():
    files = ['test5.txt', 'test10.txt', 'test20.txt']
    for file in files:
        test_users = collect_user_preliminary_data(file)
        train_users = gather_data_from_training()
        similar_users = find_similar_users(test_users, train_users)
        # pprint.pprint(similar_users)
        traverse_and_write_to_file(train_users, test_users, similar_users, file)

main_loop()