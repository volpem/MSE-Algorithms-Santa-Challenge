"""
Nearest Neighbor Approach for MSE Santa Challenge
Without calculating the costs -> Check with provided Notebook
"""


from haversine import haversine
import pandas as pd
from tqdm import tqdm

NORTH_POLE = (90, 0)
SLEIGH_CAPACITY_KG = 1000
SLEIGH_WEIGHT = 10

# From all the gifts, it creates a load that the sleigh can carry, up to 990 Kg.
def make_current_gift_load(gifts):
    current_load_gifts = []
    current_load_weight_kg = 0
    prev_location = NORTH_POLE
    best_distance = float('inf')
    nearest_gift = []

    while current_load_weight_kg < SLEIGH_CAPACITY_KG:
        # find the closest gift
        for gift in gifts:
            gift_location = (gift[1], gift[2])
            new_distance  = haversine(prev_location, gift_location)
            if new_distance < best_distance:
                best_distance = new_distance
                nearest_gift = gift

        # append this gift to the current load
        current_load_gifts.append(nearest_gift)
        
        if (current_load_weight_kg + nearest_gift[3]) > SLEIGH_CAPACITY_KG:
            break

        current_load_weight_kg += nearest_gift[3]
        # reset variables
        best_distance = float('inf')
        prev_location = (nearest_gift[1], nearest_gift[2])
        gifts.remove(nearest_gift)
        nearest_gift = []

        if len(gifts) == 0:
            break

    print(" ", int(current_load_weight_kg), "\n")
    return current_load_gifts


total_weariness = 0

df = pd.read_csv(r"data/gifts.csv")
df = df.sort_values(by='Weight', ascending=[False])
gifts = df.to_numpy().tolist()

current_location = NORTH_POLE

# makes a cool progress bar ;) 
pbar = tqdm(total=len(gifts))

submission = pd.DataFrame(columns=["GiftId", "TripId"])
trip_id = 0


while len(gifts) > 0:
    current_load_gifts = make_current_gift_load(gifts)
    # for the progress bar
    pbar.update(len(current_load_gifts))
    
    for current_load_gift in current_load_gifts:
        submission = submission.append({'GiftId': current_load_gift[0], 'TripId': trip_id}, ignore_index=True)
    trip_id += 1


submission.to_csv("submission_nn_approach.csv", index=False)
print(total_weariness)
