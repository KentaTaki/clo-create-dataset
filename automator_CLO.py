import os
import csv
import time
import subprocess
import pyautogui as pg

prescroll = 0
sizegroup = ["XS", "S", "M", "L", "XL"]
positions = {
                "avatar": {
                    "tall": { "x": 678, "y": 268, "scroll": 0 },
                    "chest": { "x": 690, "y": 295, "scroll": 0 },
                    "under": { "x": 575, "y": 727, "scroll": 1 },
                    "waist": { "x": 575, "y": 689, "scroll": 2 },
                    "uehip": { "x": 911, "y": 413, "scroll": 1 },
                    "hip": { "x": 905, "y": 433, "scroll": 1 },
                    "yukitake": { "x": 905, "y": 644, "scroll": 1 },
                    "kata": { "x": 575, "y": 499, "scroll": 1 },
                    "mata": { "x": 905, "y": 503, "scroll": 1 },
                    "momo": { "x": 905, "y": 522, "scroll": 1 },
                    },
                "grading": {
                    "button": { "x": 1307, "y": 116 },
                    "right": { "x": 1433, "y": 116 },
                    },
                "cloth": {
                    "XS": { "x": 1283, "y": 204 },
                    "S": { "x": 1283, "y": 227 },
                    "M": { "x": 1283, "y": 246 },
                    "L": { "x": 1283, "y": 271 },
                    "XL": { "x": 1283, "y": 296 },
                    "XXL": { "x": 1283, "y": 316 },
                    },
                "scroll": [
                    { "x": 1070, "y": 389},
                    { "x": 1070, "y": 721},
                    ],
                "save": { "x": 652, "y": 160}
            }

def init():
    print('Start GUI Automation...')
    pg.click(pause=1.0)
    pg.hotkey('ctrl', '1', pause=1.0) # Move on to Desktop1
    pg.click(pause=1.0)
    pg.hotkey('2', pause=1.0)

def open_avatar_size():
    print("Edit Size")
    pg.hotkey('ctrl', 'a', pause=1.0)
    time.sleep(10)

def edit_avatar_size(key, value, pr):
    global prescroll
    values = positions["avatar"][key]
    if values["scroll"] > 0 and values["scroll"] != prescroll:
        scroll = positions["scroll"][values["scroll"]-1]
        pg.click(
            x=scroll["x"],
            y=scroll["y"],
            pause=6.0*pr,
            clicks=1,
            interval=0,
            button='left'
        )
    prescroll = values["scroll"]
    pg.click(
        x=values["x"],
        y=values["y"],
        pause=6.0*pr,
        clicks=1,
        interval=0,
        button='left'
    )
    pg.hotkey('command', 'a', pause=1.0*pr)
    pg.typewrite(value, interval=0.2, pause=1.0*pr)
    pg.hotkey('enter', pause=3.0*pr)


def close_avatar_size():
    print("Closed")
    pg.hotkey('esc', pause=1.0)
    time.sleep(5)


def choose_cloth_size(cloth_size, pr):
    print("Choose "+cloth_size)
    pg.click(
        x=positions["cloth"][cloth_size]["x"],
        y=positions["cloth"][cloth_size]["y"],
        pause=5.0*pr,
        clicks=1,
        interval=0,
        button='left'
    )
    time.sleep(5*pr)


def simulation():
    print('Start Simulation...')
    pg.hotkey('ctrl', 'r', pause=1.0)
    pg.hotkey('space', pause=1.0)
    time.sleep(10)
    pg.hotkey('space', pause=1.0)
    time.sleep(3)


def save_zprj(zprj, basename, directory, pr, is_torso=False):
    '''
    if is_torso:
        pg.hotkey('shift','a', pause=1.0*pr)
        filepath = basename+'-torso'
    else:
    '''
    filepath = basename
    # save
    print("Save file")
    pg.hotkey('command', 's', pause=1.0*pr)
    print("File Saved")
    time.sleep(10*pr)
    '''
    # Torso Mode
    if is_torso:
        pg.hotkey('shift', 'a', pause=1.0*pr)
    '''
    # Remove zprj file
    command = "mv "\
        + os.path.abspath(directory) + os.sep + os.path.splitext(os.path.basename(zprj))[0] +".png "\
        + os.path.abspath(directory) + os.sep + filepath +".png"
    # print(command)
    subprocess.run(command, shell=True, check=True)

def conv_func(x, is_mm):
    if x[0] == 'id':
        return (x[0], int(x[1]))
    else:
        if is_mm:
            return (x[0], float(x[1])*10.0)
        else:
            return (x[0], float(x[1]))

def get_size_dataset(csv_path, is_mm, start_idx):
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        l = []
        for i, row in enumerate(reader):
            if i < start_idx:
                continue
            func = lambda x: conv_func(x, is_mm)
            l.append(list(map(func, row.items())))
        return l

def isdifferent(preavatarsize, key, val):
    for prekey, preval in preavatarsize:
        if not prekey == key:
            continue
        return not(preval == val)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dir', type=str, help='directory')
    parser.add_argument('--pr', default=1.0, type=float, help='pause rate')
    parser.add_argument('--start_idx', type=int, default=0, help='mm mode')
    parser.add_argument('--name', default='', type=str, help='data name')
    parser.add_argument('--sizedataset', default='sample.csv', type=str, help='size chart (csv)')
    parser.add_argument('--img_path', default='sample_Tshirt.Zprj', type=str, help='size chart (csv)')
    parser.add_argument('--mm', action='store_true', help='mm mode')
    parser.add_argument('--clothtest', action='store_true', help='mm mode')
    args = parser.parse_args()
    size_dataset = get_size_dataset(args.sizedataset, args.mm, args.start_idx)
    print(size_dataset)
    if args.clothtest:
        name = 'test'
    else:
        name = args.name

    # GUI Automation
    init()
    preavatarsize = None
    for i, size_data in enumerate(size_dataset):
        print(size_data)
        # Edit Avatar Size
        if not args.clothtest:
            open_avatar_size()
            for key, val in size_data:
                if key == 'id':
                    idx = int(val)
                    continue
                # 同じ値なら編集しない
                if preavatarsize is None or isdifferent(preavatarsize, key, val):
                    edit_avatar_size(key, str(val), args.pr)
            preavatarsize = size_data
            close_avatar_size()
        # Edit Cloth Size
        for cloth_size in sizegroup:
            choose_cloth_size(cloth_size, args.pr) # choose
            simulation() # Draping
            save_zprj(args.img_path, name+str(idx).zfill(3)+'-'+cloth_size, args.dir, args.pr, is_torso=False) #Save File
