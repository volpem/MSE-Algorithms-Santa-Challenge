'''

'''

from haversine import haversine
import pandas as pd

# globals
NORTH_POLE = (90, 0)
WEIGHT_LIMIT = 1000
SLEIGH_WEIGHT = 10

# read gifts.csv into panda frame
gifts = pd.read_csv('./data/gifts.csv')
# Use this to only read the first nrows -> shorter loading during implementation
# gifts = pd.read_csv('./data/gifts.csv', nrows=200)

# make sure numbers are not going to be treated as numbers not as string
gifts["GiftId"] = pd.to_numeric(gifts["GiftId"])
gifts["Latitude"] = pd.to_numeric(gifts["Latitude"])
gifts["Longitude"] = pd.to_numeric(gifts["Longitude"])
gifts["Weight"] = pd.to_numeric(gifts["Weight"])
# Zip Latiude and Longitude into Positions (Latitude, Longitude)
gifts['Position'] = list(zip(gifts['Latitude'],gifts['Longitude']))

gifts.head()

best_weighted_reindeer_weariness = float("inf")
submission = pd.DataFrame(columns=["GiftId", "TripId"])
submission_with_weights = pd.DataFrame(columns=["GiftId", "TripId", "Weight"])

n = 10
for trial in range(n):

    # ---- RANDOM APPROACH ----
    # shuffle dataframe rows
    gifts = gifts.sample(frac=1)
    # gifts.head()
    # counts the weight to check if < WEIGHT_LIMIT
    current_weight = 0
    # add column TripID
    gifts["TripId"] = 0

    # Assign TripID to every row with respect to the transportation weigth
    trip_id = 1  # trip_id has to start at 1!
    for index, row in gifts.iterrows():
        # check if more space in santas sledge is available
        if (current_weight + row['Weight']) < WEIGHT_LIMIT:  # weight limit excluding sleigh base weight
            # add gift weight to sum
            current_weight += row['Weight']
            # assign tripid
            gifts.at[index, 'TripId'] = trip_id

        else:
            # reset variables
            current_weight = 0  # empty sledges
            # assign new trip - increment trip id
            trip_id += 1
            # add trip_id and add weight
            current_weight += row['Weight']
            gifts.at[index, 'TripId'] = trip_id

    # show dataframe once
    if trial == 0:
        gifts.head()

    # ---- CALCULATE COSTS ----
    # now we have all the trips assigned and can we can calculate the wariness

    # start at nordpole
    previous_stop = NORTH_POLE
    # reset total costs
    weighted_reindeer_weariness = 0.0
    # group by ID to calculate weights
    gifts_weights = gifts.groupby(['TripId']).sum()
    weights_list = gifts_weights['Weight'].tolist()
    # control variable trip id
    trip_id = 1

    for index, row in gifts.iterrows():
        # still the same trip
        if row['TripId'] == trip_id:
            # calculate the cost for the location
            weighted_reindeer_weariness += haversine(row['Position'], previous_stop) * \
                        (weights_list[trip_id - 1] + SLEIGH_WEIGHT)  # +10 because of the sleigh weight
            # subtract hand out gift
            weights_list[trip_id - 1] -= row['Weight']
            # update previous stop
            previous_stop = row['Position']

        # go back to the northpole
        else:
            # check if sleigh is empty
            if weights_list[trip_id - 1] > 0.001:  # allow small error rounding error
                raise Exception("Sleigh has to be empty before going back to north-pole")
            # travel back to the northpole
            weighted_reindeer_weariness += haversine(NORTH_POLE, previous_stop) * SLEIGH_WEIGHT  # empty sleigh is 10 kg
            # assign next trip
            trip_id += 1
            weights_list[trip_id - 1] -= row['Weight']
            # start again from northpole
            previous_stop = NORTH_POLE

    print("weighted_reindeer_weariness", weighted_reindeer_weariness)

    # ---- UPDATE BEST CASE ----

    if weighted_reindeer_weariness < best_weighted_reindeer_weariness:
        # update new best costs
        best_weighted_reindeer_weariness = weighted_reindeer_weariness
        # assign GiftID and TripID
        submission = gifts[["GiftId", "TripId"]]
        submission_with_weights = gifts[["GiftId", "TripId", "Weight"]]

    # else run next random approach
    else:
        continue

print(f"The best wariness is {best_weighted_reindeer_weariness}!")
# for a direct view in excel
submission_with_weights.to_excel("test_check.xlsx")
# actual submission in csv format without pandas index
submission.to_csv("submission_random_approach.csv", index=False)
