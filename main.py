from copy import deepcopy
from ppadb.client import Client as AdbClient
from PIL import Image
from io import BytesIO
from time import sleep

client = AdbClient(host="127.0.0.1", port=5037)
device = client.devices()[0]

rows = 2
row_pos = [1085, 1760]
y_off = 100
border_col = (188, 188, 188, 255)


colors_per_vile = 4
level_viles = []
vile_positions = []

def extract_vile_content():
    screen = Image.open(BytesIO(device.screencap()))
    level_viles.clear()
    vile_positions.clear()
    number_of_colors = 0
    colors = {}
    for row in range(rows):
        inside_count = 0
        inside = False
        on_border = False
        for x in range(0, screen.width, 4):
            pixel = screen.getpixel((x,row_pos[row]))
            if inside_count == 13 and inside:
                vile_positions[-1] = (x, row_pos[row]-y_off*2)
                for col in range(colors_per_vile):
                    pixel = screen.getpixel((x,row_pos[row] - y_off * col))
                    if (pixel[0]+pixel[1]+pixel[2])/3 <50:
                        break
                    if pixel not in colors:
                        colors[pixel] = number_of_colors
                        number_of_colors += 1
                    level_viles[-1].append(colors[pixel])

            inside_count += 1
            if pixel == border_col:
                if not on_border:
                    inside_count = 0
                    inside = not inside
                    if inside:
                        level_viles.append([])
                        vile_positions.append([])
                on_border = True
            else:
                on_border = False

def is_move_useless(viles, move):
    copied_viles = deepcopy(viles)
    apply_move(copied_viles, move)

    if(len(copied_viles[move[0]]) == 0):
        return False
    return copied_viles[move[0]][-1] == viles[move[0]][-1]

def get_valid_moves(viles):
    moves = []
    for v1 in range(len(viles)):
        for v2 in range(len(viles)):
            if v2 != v1 and is_move_valid(viles, (v1, v2)):
                moves.append((v1, v2))
    return moves

def apply_move(viles, move):
    while is_move_valid(viles, move):
        viles[move[1]].append(viles[move[0]][-1])
        viles[move[0]].pop(-1)

def is_move_valid(viles, move):
    v1 = viles[move[0]]
    v2 = viles[move[1]]

    if(len(v2) >= colors_per_vile or len(v1) == 0):
        return False

    if(len(v2) == 0 or v2[-1] == v1[-1]):
        return True

    return False

def is_solved(viles):
    for i in range(len(viles)):
        if len(viles[i]) == 0:
            continue
        if len(viles[i]) != colors_per_vile:
            return False

        for j in range(colors_per_vile - 1):
            if viles[i][j] != viles[i][j+1]:
                return False
    return True

def solve_rec(viles, found_states, move_history = [], depth = 0):
    if is_solved(viles):
        return move_history
    moves = get_valid_moves(viles)
    for move in moves:
        if is_move_useless(viles, move):
            continue
        next_viles = deepcopy(viles)
        apply_move(next_viles, move)
        hashed_state = frozenset(str(next_viles[i]) for i in range(len(viles)))
        if hashed_state in found_states:
            continue
        found_states.add(hashed_state)
        next_move_history = move_history[:]
        next_move_history.append(move[:])
        solution = solve_rec(next_viles, found_states, next_move_history, depth+1)
        if solution:
            return solution
    return False

def solve(viles):
    found_states = set(frozenset(str(viles[i]) for i in range(len(viles))))
    return solve_rec(viles, found_states)

extract_vile_content()
print(level_viles)
moves = solve(level_viles)
print(len(moves), "moves:", moves)
for move in moves:
    apply_move(level_viles, move)
    device.shell('input tap ' + str(vile_positions[move[0]][0]) + ' ' + str(vile_positions[move[0]][1]))
    sleep(0.1)
    device.shell('input tap ' + str(vile_positions[move[1]][0]) + ' ' + str(vile_positions[move[1]][1]))
    sleep(2)
