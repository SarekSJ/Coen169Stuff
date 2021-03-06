import pprint
from collections import Counter
import math
import os

def gather_data_from_training():
    users = []
    IUF_scores = [0] * 1001
    users.append([0])
    train_user_averages = {}
    with open('train.txt') as f:
        for index, line in enumerate(f):
            users.append([0]) # Add a new element to the array for each user
            non_zero_ratings = 0 # This will help us calculate our averages later
            split_line = line.split()
            train_user_averages[index+1] = 0
            # Traverse each movie rating for this user
            for count, rating in enumerate(split_line):
                users[index+1].append(int(rating))
                if rating != '0':
                    train_user_averages[index+1] += int(rating)
                    IUF_scores[count + 1] += 1
                    non_zero_ratings += 1
            train_user_averages[index+1] = train_user_averages[index+1] / non_zero_ratings
    for i in range(1001):
        if i == 0:
            continue
        else:
            num_ratings = IUF_scores[i]
            if (num_ratings == 0):
                num_ratings = 1
            IUF_scores[i] = math.log(200 / (num_ratings))
        # print ("Movie ID: " +str(i) + "Score: " + str(IUF_scores[i]))
    return users, train_user_averages, IUF_scores

def collect_user_preliminary_data(current_file):
    test_users = {}
    test_user_averages = {}
    with open (current_file) as f:
        for line in f:
            split_line = line.split(' ')
            user_id = int(split_line[0])
            movie_id = int(split_line[1])
            rating = int(split_line[2])
            try:
                if rating != 0:
                    test_users[user_id][movie_id] = rating
                    test_user_averages[user_id] += rating
            except Exception as e:
                test_users[user_id] = {}
                test_user_averages[user_id] = 0
                if rating != 0:
                    test_users[user_id][movie_id] = rating
                    test_user_averages[user_id] += rating
    for user, average_rating in test_user_averages.items():
        test_user_averages[user] = average_rating / len(test_users[user])
    return test_users, test_user_averages


def preprocess_datasets(test_users, test_user_averages, train_users, train_user_averages, IUF_scores):
    # The goal here is to bring the data in these data structures to a base line
    # accomplished by subtracting out the average from each rating
    for user_id, user_ratings in enumerate(train_users):
        for count, rating in enumerate(user_ratings):
            if rating != 0:
                user_ratings[count] *= IUF_scores[count]
                user_ratings[count] -= train_user_averages[user_id]
    for user, movies in test_users.items():
        for movie, rating in movies.items():
            test_users[user][movie] *= IUF_scores[movie]
            test_users[user][movie] -= test_user_averages[user]
    return test_users, train_users


def generate_cosine_similarity(users, training_data, user_index, train_index):
    # users[user_index] = dictionary of all the ratings they have
    # ex: users[user_index] = {'237': 4, '306': 5, ... , '934': 5}
    train_user_ratings = []
    test_user_ratings = []
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

    denom = math.sqrt(train_den) * math.sqrt(test_den)
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

def find_users_with_movie_ratings_and_compute_cosine_similarity(test_users, training_users):
    similar_users = {}
    for user_id, movies_dict in test_users.items():
        similar_users[user_id] = {}
        for movie, rating in movies_dict.items():
            for train_user_index in range(1,201):
                if training_users[train_user_index][int(movie)] != 0:
                    # Then we can consider their similarity, add them to the list of users who rated the same movies
                    similar_users[user_id][train_user_index] = 0
            for train_user in similar_users[user_id]:
                similar_users[user_id][train_user] = generate_cosine_similarity(test_users, training_users,
                                                                                user_id, train_user)
    # Will get rid of any entry where there's no usable cosine similarity
    for user_id, movies_dict in test_users.items():
        similar_users[user_id]={k:v for k, v in similar_users[user_id].items() if v}
        top_k = Counter(similar_users[user_id]).most_common(14)
        similar_users[user_id] = {}
        for element in top_k:
            similar_users[user_id][element[0]] = element[1]
    print(similar_users)
    return similar_users

def generate_rating_and_write_to_file(train_users, test_users, similar_users, test_averages, IUF_scores, current_file):
    with open ('testestest.txt','w'):
        pass
    with open (current_file) as f:
        file = f.readlines()
        last = file[-1]
        for index, line in enumerate(file):

            split_line = line.split()
            rating = int(split_line[2])
            movie_id = int(split_line[1])
            user_id = int(split_line[0])

            if rating == 0:
                rating = str(generate_rating_for_movie(movie_id, train_users, user_id, test_averages, similar_users, IUF_scores))
                with open ('testestest.txt','a') as fo:
                    if line == last:
                        fo.write(str(user_id)+' ' +str(movie_id)+' '+ str(rating))
                    else:
                        fo.write(str(user_id)+' ' +str(movie_id)+' '+ str(rating)+ '\n')

            else:
                pass
    os.rename('testestest.txt', current_file)


def generate_rating_for_movie(movie_id, train_users, test_user_id, test_averages, similar_users, IUF_scores):
    numerator = 0
    denominator = 0
    # print(similar_users)
    for test_user, similarity_dict in similar_users.items():
        for similar_user, similarity in similarity_dict.items():
            # print (train_users[int(similar_user)][int(movie_id)])
            if train_users[int(similar_user)][int(movie_id)] == 0:
                continue
            else:
                rating = train_users[int(similar_user)][int(movie_id)]
                new_weight = (similarity)
                new_weight = new_weight * (math.fabs(new_weight)) ** (2.5-1)
                numerator += (rating * new_weight)
                denominator += new_weight

    add_back_in_rating = test_averages[test_user_id]
    if denominator == 0:
        return 1
    final_prediction = round(numerator/denominator + add_back_in_rating)
    if final_prediction <= 0:
        return 1
    if final_prediction > 5:
        return 5
    return final_prediction


def main_loop():
    files = ['test5.txt', 'test10.txt', 'test20.txt']
    for file in files:
        test_users, test_users_averages = collect_user_preliminary_data(file)
        train_users, train_users_averages, IUF_scores = gather_data_from_training()
        test_users, train_users = preprocess_datasets(test_users,test_users_averages,train_users,train_users_averages, IUF_scores)
        users_with_movie_ratings = find_users_with_movie_ratings_and_compute_cosine_similarity(test_users, train_users)
        generate_rating_and_write_to_file(train_users, test_users, users_with_movie_ratings, test_users_averages, IUF_scores,
                                          file)

main_loop()