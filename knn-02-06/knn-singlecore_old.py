#!/usr/bin/python
import datetime, argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-tr", "--train", required = True, help = "Is the training dataset path.")
ap.add_argument("-te", "--test", required = True, help = "Is the testing dataset path.")
ap.add_argument("-k", required = True, help = "Is K for the KNN algorithm.")
ap.add_argument("-lte", "--limit-test", required = False, help = "Sets a limit for how many testing sets must be used instead of the whole file.")
ap.add_argument("-ltr", "--limit-train", required = False, help = "Sets a limit for how many training sets must be used instead of the whole file.")

args = vars(ap.parse_args())

train_file_path = args["train"]
test_file_path = args["test"]
k_number = int(args["k"])

test_calculation_limit = False
test_calculation_limit_arg = args["limit_test"]
if (test_calculation_limit_arg):
    test_calculation_limit = int(test_calculation_limit_arg)
else:
    print "Be aware you didn't set a limit for the testing set. We are going to test all."

train_calculation_limit = False
train_calculation_limit_arg = args["limit_train"]
if (train_calculation_limit_arg):
    train_calculation_limit = int(train_calculation_limit_arg)
else:
    print "Be aware you didn't set a limit for the training set. We are going to use it all."

#RESULTS
result_error = 0
result_rejection = 0


def calc_distance(x, y):
    return np.sum((x-y)**2)

def check_rank(dictionary, current_ranking, feature_class, distance):
    # print "check_rank",feature_class

    if current_ranking.size >= k_number:
        dictionary.pop(current_ranking[k_number-1])
        current_ranking = np.delete(current_ranking, k_number-1, 0)

    current_ranking = np.append(current_ranking, distance)
    dictionary[distance] = feature_class
    current_ranking = np.sort(current_ranking)
    # print current_ranking, dictionary


    return dictionary, current_ranking
# def calc_distance(target, other):
#     return np.linalg.norm(target-other)


train_file = open(train_file_path, "r")

print "Reading file: ", train_file_path

header = train_file.readline().split(" ")
number_lines = int(header[0])
number_features = int(header[1])
classes = 10 #todo remove harded coded.

print "Lines {} | Features {}".format(number_lines, number_features)

train_features_dict = {}

train_processed_lines = 0
for features in train_file:
    if train_calculation_limit and train_processed_lines >= train_calculation_limit:
        break

    features = features.split(" ")
    features_class = features.pop(number_features)
    features = np.array(map(float, features))
    features_class = int(features_class.replace("\n",""))

    # print features_class, features
    train_features_dict[train_processed_lines] = {"class" : features_class, "features": features}

    train_processed_lines = train_processed_lines + 1

test_file = open(test_file_path, "r")

print "Reading file: ", test_file_path

header = test_file.readline().split(" ")
number_lines = int(header[0])
number_features = int(header[1])
print "Lines {} | Features {}".format(number_lines, number_features)
if test_calculation_limit:
    print "We are limiting to {} testing sets.".format(test_calculation_limit)

test_features_dict = {}

test_processed_lines = 0
for features in test_file:
    if test_calculation_limit and test_processed_lines >= test_calculation_limit:
        break

    features = features.split(" ")
    features_class = features.pop(number_features)
    features = np.array(map(float, features))
    features_class = int(features_class.replace("\n",""))

    # print features_class, features
    test_features_dict[test_processed_lines] = {"class" : features_class, "features": features, "guessed_class": -1}

    test_processed_lines = test_processed_lines + 1

confusion_matrix = np.zeros((classes,classes), dtype=np.int)
time_start = datetime.datetime.now()

for test_feature_index in test_features_dict:
    k_ranking_dict = {}
    k_ranking = np.zeros(0)

    for train_feature_index in train_features_dict:
        # print target_feature_index, other_feature_index

        distance = calc_distance(test_features_dict[test_feature_index]["features"], train_features_dict[train_feature_index]["features"])
        # print "Calculated test {} train {} distance {}".format(test_feature_index, train_feature_index, distance)
        k_ranking_dict, k_ranking = check_rank(k_ranking_dict, k_ranking, train_features_dict[train_feature_index]["class"], distance)

    to_count_array = []
    for key in k_ranking_dict:
        # print "k_ranking_dict[key]",k_ranking_dict[key]
        to_count_array.append(k_ranking_dict[key])

    counting = np.bincount(to_count_array)
    # print "counting", counting
    # print "argmax",np.argmax(counting)
    guessed_class = np.argmax(counting)
    # print "guessed_class",guessed_class
    guessed_counter = counting[guessed_class]
    # print "guessed_counter",guessed_counter
    # check if there is antoher class with same count. We should reject.
    counting = np.delete(counting, guessed_class)
    if guessed_counter in counting:
        # print "Rejecting"
        result_rejection = result_rejection + 1

    # print counting[np.argmax(counting)] in counting

    real_class = test_features_dict[test_feature_index]["class"]

    confusion_matrix[real_class,guessed_class] = confusion_matrix[real_class,guessed_class] + 1
    # print real_class, guessed_class

    if real_class != guessed_class:
        result_error = result_error + 1

valid_total = test_processed_lines - result_rejection

print "Tested {} | Error: {} | Rejection {} | Correct {}".format(test_processed_lines, result_error, result_rejection, (valid_total - result_error) * 100.0 / valid_total)
print confusion_matrix
time_end = datetime.datetime.now()
print "Executed in {}".format(time_end - time_start)
