from haversine import haversine
import pandas as pd
from tqdm import tqdm

NORTH_POLE = (90, 0)
SLEIGH_CAPACITY_KG = 1000
SLEIGH_WEIGHT = 10

# From all the gifts, it creates a load that the sleigh can carry, up to 1000 Kg.
def make_current_gift_load(gifts):
    current_load_gifts = []
    current_load_weight_kg = 0
    while current_load_weight_kg + gifts[0][3] <= SLEIGH_CAPACITY_KG:
        current_gift = gifts.pop(0)
        current_load_gifts.append(current_gift)
        current_load_weight_kg += current_gift[3]
        if len(gifts) == 0:
            break
    return current_load_gifts

# Sorts the found load based on weariness.
def find_gift_to_deliver(current_load_gifts, current_location):
    total_weight_for_weariness = 0
    current_load_gifts_with_distance = []
    for gift in current_load_gifts:
        gift_weight = gift[3]
        gift_location = (gift[1], gift[2])
        distance = haversine(current_location, gift_location)
        current_load_gifts_with_distance.append((gift, distance))
        total_weight_for_weariness += gift_weight

    sorted_clgww = sorted(current_load_gifts_with_distance, key=lambda x: x[1])
    gift_to_deliver = sorted_clgww[0][0]
    gift_to_deliver_distance = sorted_clgww[0][1]
    gift_to_deliver_weariness = gift_to_deliver_distance * (total_weight_for_weariness + SLEIGH_WEIGHT)
    return gift_to_deliver, gift_to_deliver_weariness

total_weariness = 0

df = pd.read_csv(r"gifts.csv")
df = df.sort_values(by='Weight', ascending=[False])
gifts = df.to_numpy().tolist()

current_location = NORTH_POLE

# makes a cool progress bar ;) 
pbar = tqdm(total=len(gifts))

submission = pd.DataFrame(columns=["GiftId", "TripId"])
trip_id = 0

while len(gifts) > 0:
    current_location = NORTH_POLE
    
    current_load_gifts = make_current_gift_load(gifts)
    # for the progress bar
    pbar.update(len(current_load_gifts))
    
    for current_load_gift in current_load_gifts:
        submission = submission.append({'GiftId': current_load_gift[0], 'TripId': trip_id}, ignore_index=True)
    trip_id += 1

    last_gift_location = (0, 0)
    while len(current_load_gifts) > 0:
        gift_to_deliver, gift_to_deliver_weariness = find_gift_to_deliver(current_load_gifts, current_location)
        total_weariness += gift_to_deliver_weariness
        current_location = (gift_to_deliver[1], gift_to_deliver[2])
        gift_delivered = gift_to_deliver
        index_of_gift_delivered = current_load_gifts.index(gift_delivered)
        # after the gift is delivered, it needs to be removed from the gifts list.
        current_load_gifts.pop(index_of_gift_delivered)
        last_gift_location = current_location
    distance_back_to_pole = haversine(last_gift_location, NORTH_POLE)
    total_weariness += distance_back_to_pole * (SLEIGH_WEIGHT)

submission.to_csv("submission_nn_approach.csv", index=False)
print(total_weariness)
