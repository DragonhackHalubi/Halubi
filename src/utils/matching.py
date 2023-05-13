from math import radians, sin, cos, sqrt, atan2

def distance(lat1, long1, lat2, long2):
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])

    dlat = lat2 - lat1
    dlong = long2 - long1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    R = 6371 # Radius of the Earth in kilometers
    distance = R * c

    return distance

def calculate_user_compatibility(user1, user2):
    similarity = []
    for day in user1:
        if day in user2:
            dist = distance(user1[day][0], user1[day][1], user2[day][0], user2[day][1])
            # print(dist)
            if dist < 30:
                similarity.append(day)
    return similarity

u1 = {
    1: [46.04,14.5288766], #lj-kp
    2: [45.9728727,14.4879599], #lj-lj
    3: [45.9728727,14.4879599],
    4: [45.9728727,14.4879599],
    5: [46.04,14.5288766], #lj-kp
}

u2 = {
    1: [45.5524934,13.7460746], #lj-kp
    2: [46.0156763,14.6917757], #lj-lj
    66: [46.0156763,14.6917757],
    4: [46.0156763,14.6917757],
    5: [45.5524934,13.7460746], #lj-kp
}

# print(calculate_user_compatibility(u1,u2))