import pprint
def gather_data_from_training():
    users = []
    with open('train.txt') as f:
        for index, line in enumerate(f):
            split_line = line.split()
            users.append([])
            for rating in split_line:
                users[index].append(int(rating))
    return users
# users = gather_data_from_training()
# print(users)

# Don't forget to rename that dictionary sometime
# For real tho
def collect_user_preliminary_data():
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
        sucking_dicts_aint_gay: dictionary containing user info and ratings to base predictions off of
    """
    sucking_dicts_aint_gay = {}
    

    with open ('test5.txt') as f:
        for line in f:
            split_line = line.split(' ')
            try:
                if split_line[2][0:1] != '0':
                    sucking_dicts_aint_gay[split_line[0]][split_line[1]] = int(split_line[2][0:1])
            except Exception as e:
                sucking_dicts_aint_gay[split_line[0]] = {}
                if split_line[2][0:1] != '0':
                    sucking_dicts_aint_gay[split_line[0]][split_line[1]] = int(split_line[2][0:1])
    return sucking_dicts_aint_gay

users = collect_user_preliminary_data()
train_users = gather_data_from_training()
# print (users)

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
            for index, train_user in enumerate(training_users):
                if train_user[int(movie)] != 0:
                    # Then we can consider their similarity, add them to the list of users who rated the same movies
                    similar_users[user_id][index] = train_user[int(movie)]
            # for train_user in similar_users:
            #     similar_users[train_user] = generate_cosine_similarity(test_users, training_users, user_id, train_user)
    print(similar_users)
    return similar_users

similar_users = find_similar_users(users, train_users)

def generate_cosine_similarity(users, training_data, user_index, train_index):
    # users[user_index] = dictionary of all the ratings they have
    # ex: users[user_index] = {'237': 4, '306': 5, ... , '934': 5}
    for movie, rating in users[user_index]:
        train_rating = training_data[train_index][movie]

    pass