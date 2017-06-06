import pprint
import math
from collections import Counter
import os

def gather_data_from_training():
    users = []
    users.append([]) # This is to offset the indexing by one, allows us to just call users[user_id] without needing to
                     # subtract 1.
    train_user_averages = {}
    train_movie_averages = {}
    train_movie_non_zero_counts = {}
    with open('train.txt') as f:
        for index, line in enumerate(f):
            non_zero_ratings = 0
            split_line = line.split()
            users.append([-1])
            train_user_averages[index+1] = 0
            for count, rating in enumerate(split_line):
                if index == 0:
                    train_movie_averages[count+1] = 0
                    train_movie_non_zero_counts[count+1] = 0
                users[index+1].append(int(rating))
                if rating != '0':
                    train_movie_averages[count+1] += int(rating)
                    train_user_averages[index+1] += int(rating)
                    train_movie_non_zero_counts[count+1] += 1
                    non_zero_ratings += 1
            train_user_averages[index+1] = train_user_averages[index+1] / non_zero_ratings
    for movie_id, sum in train_movie_averages.items():
        den = train_movie_non_zero_counts[movie_id]
        if den == 0:
            train_movie_averages[movie_id] = 0
        else:
          train_movie_averages[movie_id] = sum / den
    return users, train_user_averages, train_movie_averages

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

def preprocess_datasets_items(test_users, test_movie_averages, train_users, train_movie_averages):
    # The goal here is to bring the data in these data structures to a base line
    # accomplished by subtracting out the average from each rating
    for user_id, user_data in enumerate(train_users):
        for movie_index, rating in enumerate(user_data):
            if movie_index == 0:
                continue
            elif rating != 0:
                user_data[movie_index] -= train_movie_averages[movie_index]
    for user_id, users in test_users.items():
        for movie_index, rating in users.items():
            test_users[user_id][movie_index] -= test_movie_averages[movie_index]
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
                similar_users[user_id][train_user] = generate_cosine_similarity(test_users, training_users, user_id, train_user)
    # Will get rid of any entry where there's no usable cosine similarity
    for user_id, movies_dict in test_users.items():
        similar_users[user_id]={k:v for k, v in similar_users[user_id].items() if v}
        top_k = Counter(similar_users[user_id]).most_common(14)
        similar_users[user_id] = {}
        for element in top_k:
            similar_users[user_id][element[0]] = element[1]
    return similar_users


def generate_rating_and_write_to_file(train_users, test_users, similar_users, movie_averages, test_averages, current_file):
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
                item_rating = generate_rating_for_movie_items(movie_id, train_users, user_id, movie_averages, similar_users)
                user_rating = generate_rating_for_movie_users(movie_id, train_users, user_id, test_averages, similar_users)
                rating = round(0.85 * user_rating + 0.15 * item_rating)
                print (rating)
                with open ('testestest.txt','a') as fo:
                    if line == last:
                        fo.write(str(user_id)+' ' +str(movie_id)+' '+ str(rating))
                    else:
                        fo.write(str(user_id)+' ' +str(movie_id)+' '+ str(rating)+ '\n')

            else:
                pass
    os.rename('testestest.txt', current_file)


def generate_rating_for_movie_items(movie_id, train_users, test_user_id, movie_averages, similar_users):
    numerator = 0
    denominator = 0
    for test_user, similarity_dict in similar_users.items():
        for similar_user, similarity in similarity_dict.items():
            if train_users[int(similar_user)][int(movie_id)] == 0:
                continue
            else:
                rating = train_users[int(similar_user)][int(movie_id)]
                numerator += (rating * similarity)
                denominator += similarity
    add_back_in_rating = movie_averages[test_user_id]
    if denominator == 0:
        return 1
    final_prediction = round(numerator/denominator + add_back_in_rating)
    if final_prediction <= 0:
        return 1
    if final_prediction > 5:
        return 5
    return final_prediction

def generate_rating_for_movie_users(movie_id, train_users, test_user_id, test_averages, similar_users):
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
                numerator += (rating * similarity)
                denominator += similarity
    # print (numerator/denominator)
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
    files = ['test5.txt', 'test10.txt','test20.txt']
    for file in files:
        test_users, test_user_averages = collect_user_preliminary_data(file)
        train_users, train_user_averages, train_movies_averages = gather_data_from_training()
        test_users, train_users = preprocess_datasets_items(test_users,train_movies_averages,train_users,train_movies_averages)
        users_with_movie_ratings = find_users_with_movie_ratings_and_compute_cosine_similarity(test_users, train_users)
        generate_rating_and_write_to_file(train_users, test_users, users_with_movie_ratings, train_movies_averages, test_user_averages,
                                          file)

main_loop()