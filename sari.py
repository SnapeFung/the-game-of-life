import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# setting up the values for the grid
hp = 100  # Health People
vc = 180  # Virus Carriers
pd = 255  # Patients Diagnosed
space = 0  # Unoccupied Space
values = [hp, vc, pd, space]
N = 50


def random_vc(n):
    """return a grid of n^2 random values"""
    return np.random.choice(values, n * n, p=[0.19, 0.01, 0, 0.8]).reshape(n, n)


def get_id(grid):
    people_list = list()
    pid = 1
    for i in range(N):
        for j in range(N):
            if grid[i, j] == vc:
                people_list.append({'id': pid, 'loc': [i, j], 'state': vc, 'days': 1})
                pid += 1
            if grid[i, j] == hp:
                people_list.append({'id': pid, 'loc': [i, j], 'state': hp, 'days': 0})
                pid += 1
    return people_list


def update(people_list):
    infection_zone = []
    for i in people_list:
        if i['days'] >= 1:
            x, y = i['loc']
            infection_zone.append([x, y])
            infection_zone.append([x - 1, y])
            infection_zone.append([x, y - 1])
            infection_zone.append([x - 1, y - 1])
            infection_zone.append([x + 1, y + 1])
            infection_zone.append([x + 1, y])
            infection_zone.append([x, y + 1])
            infection_zone.append([x + 1, y - 1])
            infection_zone.append([x - 1, y + 1])
    for i in people_list:
        now_loc = i['loc']
        direction = np.random.randint(5)
        
        if now_loc[0] == 0 and direction == 0:
            direction = 2
        if now_loc[0] == N - 1 and direction == 2:
            direction = 0
        if now_loc[1] == 0 and direction == 1:
            direction = 3
        if now_loc[1] == N - 1 and direction == 3:
            direction = 1
        
        if direction == 0:  # go straight
            i['loc'][0] -= 1
        if direction == 1:  # go left
            i['loc'][1] -= 1
        if direction == 2:  # go down
            i['loc'][0] += 1
        if direction == 3:  # go right
            i['loc'][1] += 1
        
        if i['days'] >= 1:
            i['days'] += 1
        if i['loc'] in infection_zone and i['days'] == 0:
            i['days'] = 1
        if i['days'] >= 14:
            i['state'] = pd
    
    new_grid = np.zeros([N, N], dtype=int)
    for i in people_list:
        x, y = i['loc'][0], i['loc'][1]
        new_grid[x][y] = i['state']
    print(new_grid)
    print(people_list)
    return new_grid


def main():
    grid = random_vc(N)
    people_id = get_id(grid)
    data = []
    for i in range(150):
        data.append(update(people_id))
    
    fig, ax = plt.subplots()
    for i in range(len(data)):
        ax.cla()
        ax.imshow(data[i])
        ax.set_title("frame {}".format(i))
        # Note that using time.sleep does *not* work here!
        plt.pause(0.5)


if __name__ == '__main__':
    main()
