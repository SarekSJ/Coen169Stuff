# Coen169Stuff
Rec Sys
Cosine Similarity should give error of .8
Files:
  Train.txt:
    - contains information in a table to use on predictions. 
      Basically, has a ton of users with ratings across films, can be used to find similar users 
      to the user you're trying to make predictions for.  
      Each row represents a user, each column represents a movie. The number in [user][movie]
      is the rating given by that user for that movie. 
  Test[5:20].txt:
    - files we have to calculate predictions for.
      These files have blocks of user data. Column 1 contains user IDs, column 2 contains movie ID, column 3 contains rating.
      
  Forreal/forreal.py:
    - Contains the actual code for doing the cool stuff (so far).
      
      gather_data_from_training(): 
        Collects all the info from train.txt and puts it into a 2d array named users.
        The structure is as follows: users[user_id][movie_id] = rating
      
      collect_user_preliminary_data():
        Collects info from current users to compare against users in train.txt
        Data structure here is a dictionary as follows:
          sucking_dicts_aint_gay = {
                                      'user_id': {
                                                    'movie_id': rating,
                                                    'movie_id2': rating2,
                                                            .
                                                            .
                                                            .
                                                    'movie_id_end':rating_end
                                                 },
                                      'next_user':{
                                                    'movie_id': rating,
                                                    'movie_id2': rating2,
                                                            .
                                                            .
                                                            .
                                                    'movie_id_end':rating_end
                                                  }
                                   }  
                                   
        find_similar_users():
          This will find any users in train.txt that rated the same movies that users in test[5:20].txt used.
          Also creates another dictionary to keep track cosine similarities:
            users = {
                      'user_id': {
                                    'user_id_from_train' : cosine_similarity,
                                    'user_2_from_train': another_cosine_similarity
                                 }
                      'user_2_id': {
                                    'user_id_from_train' : cosine_similarity,
                                    'user_2_from_train': another_cosine_similarity
                                   }
                    }
          The function will also call generate_cosine_similarity() to get those calculations.
        generate_cosine_similarity(users, training_data, user_index, train_index):
          returns a cosine similarity value for two users based on movies they both rated. 
  
