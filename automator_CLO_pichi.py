import os
import csv
import time
import subprocess
import pyautogui as pg

prescroll = 0
sizegroup = ["S", "M", "L"]
positions = {
                "avatar": {
                    "tall": { "x": 678, "y": 268, "scroll": 0 },
                    "chest": { "x": 690, "y": 295, "scroll": 0 },
                    "under": { "x": 575, "y": 727, "scroll": 1 },
                    "waist": { "x": 575, "y": 689, "scroll": 2 },
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
                    "S": { "x": 1283, "y": 204 },
                    "M": { "x": 1283, "y": 227 },
                    "L": { "x": 1283, "y": 246 },
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


def choose_cloth_size(cloth_size):
    print("Choose "+cloth_size)
    pg.click(
        x=positions["cloth"][cloth_size]["x"],
        y=positions["cloth"][cloth_size]["y"],
        pause=5.0,
        clicks=1,
        interval=0,
        button='left'
    )
    time.sleep(5)


def simulation():
    print('Start Simulation...')
    pg.hotkey('ctrl', 'r', pause=1.0)
    pg.hotkey('space', pause=1.0)
    time.sleep(10)
    pg.hotkey('space', pause=1.0)
    time.sleep(3)


def save_zprj(basename, directory, pr, is_torso=False):
    print("Save file")
    if is_torso:
        pg.hotkey('shift','a', pause=1.0*pr)
        filepath = basename+'-torso'
    else:
        filepath = basename
    # save
    pg.hotkey('shift','command','s', pause=4.0*pr)
    pg.click(
        x=positions["save"]["x"],
        y=positions["save"]["y"],
        pause=5.0*pr,
        clicks=4,
        interval=0,
        button='left'
    )
    pg.hotkey('delete', pause=2.0*pr)
    pg.typewrite(filepath, interval=0.2, pause=2.0*pr)
    pg.hotkey('enter', pause=2.0*pr)
    print("File Saved " + filepath)

    time.sleep(5*pr)
    if is_torso:
        pg.hotkey('shift', 'a', pause=1.0*pr)
    # Remove zprj file
    command = "rm " + os.path.abspath(directory) + os.sep + filepath +".Zprj"
    subprocess.run(command, shell=True, check=True)


def get_size_dataset(csv_path, is_mm):
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        l = []
        for row in reader:
            if is_mm:
                func = lambda x: (x[0], float(x[1])*10.0)
            else:
                func = lambda x: (x[0], float(x[1]))
            l.append(list(map(func, row.items())))
        return l

def get_cloth_size(val, mm):
    if mm:
        val = val / 10.0

    if val >= 75.0 and val < 95.0:
        return sizegroup[0]
    elif val >= 95.0 and val < 110.0:
        return sizegroup[1]
    else:
        return sizegroup[2]

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--dir', type=str, help='directory')
    parser.add_argument('--pr', default=1.0, type=float, help='pause rate')
    parser.add_argument('--name', default='', type=str, help='data name')
    parser.add_argument('--sizedataset', default='sample.csv', type=str, help='size chart (csv)')
    parser.add_argument('--mm', action='store_true', help='mm mode')
    args = parser.parse_args()
    size_dataset = get_size_dataset(args.sizedataset, args.mm)

    # GUI Automation
    init()
    for i, size_data in enumerate(size_dataset):
        # Edit Avatar Size
        open_avatar_size()
        for key, val in size_data:
            if key == 'chest':
                cloth_size = get_cloth_size(val, args.mm)
            edit_avatar_size(key, str(val), args.pr)
        close_avatar_size()
        # Edit Cloth Size
        choose_cloth_size(cloth_size) # choose
        simulation() # Draping
        save_zprj(str(i).zfill(3), args.dir, args.pr, is_torso=False) #Save File
