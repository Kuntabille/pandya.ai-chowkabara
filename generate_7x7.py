def generate_p1_path():
    path = []
    # Ring 0
    curr = [3,6]
    directions = [(1,0), (0,-1), (-1,0), (0,1), (1,0)]
    for dx, dy in directions:
        while True:
            if [curr[0], curr[1]] not in path:
                path.append([curr[0], curr[1]])
            nx, ny = curr[0]+dx, curr[1]+dy
            if 0 <= nx <= 6 and 0 <= ny <= 6 and [nx, ny] not in path:
                if [nx, ny] == [2,6]:
                    path.append([nx, ny])
                    curr = [nx, ny]
                    break
                curr = [nx, ny]
            else:
                break
    
    # Ring 1
    curr = [2,5]
    for dx, dy in directions:
        while True:
            if [curr[0], curr[1]] not in path:
                path.append([curr[0], curr[1]])
            nx, ny = curr[0]+dx, curr[1]+dy
            if 1 <= nx <= 5 and 1 <= ny <= 5 and [nx, ny] not in path:
                if [nx, ny] == [1,5]:
                    path.append([nx, ny])
                    curr = [nx, ny]
                    break
                curr = [nx, ny]
            else:
                break

    # Ring 2
    curr = [2,4]
    for dx, dy in directions:
        while True:
            if [curr[0], curr[1]] not in path:
                path.append([curr[0], curr[1]])
            nx, ny = curr[0]+dx, curr[1]+dy
            if 2 <= nx <= 4 and 2 <= ny <= 4 and [nx, ny] not in path:
                if [nx, ny] == [2,3]:
                    path.append([nx, ny])
                    curr = [nx, ny]
                    break
                curr = [nx, ny]
            else:
                break

    # Center
    if [3,3] not in path:
        path.append([3,3])
    
    return path

p1 = generate_p1_path()
# P2 is top (starts at 3,0). Rotate P1 180 degrees. (6-x, 6-y)
p2 = [[6-x, 6-y] for x,y in p1]
# P3 is left (starts at 0,3). Rotate P1 90 degrees CW?
# P1 start is (3,6). P3 start is (0,3).
# x' = 6-y = 6-6 = 0. y' = x = 3. -> (6-y, x) gives (0,3).
p3 = [[6-y, x] for x,y in p1]
# P4 is right (starts at 6,3). Rotate P1 90 degrees CCW.
# x' = y = 6. y' = 6-x = 6-3 = 3. -> (y, 6-x) gives (6,3).
p4 = [[y, 6-x] for x,y in p1]

def format_path(p):
    return "{" + ",".join([f"{{{x},{y}}}" for x,y in p]) + "}"

print(f"local p1_path = {format_path(p1)}")
print(f"local p2_path = {format_path(p2)}")
print(f"local p3_path = {format_path(p3)}")
print(f"local p4_path = {format_path(p4)}")
