import os
import shutil
from pathlib import Path


def get_all_vol(usb_path=os.getcwd()):
    now_vol = usb_path[0]
    for i in range(91, 66, -1):
        vol = chr(i) + ':/'
        if os.path.isdir(vol) and now_vol != vol[0]:
            yield Path(vol)


def copy_to_usb(root, file):
    print("正在复制", file)
    shutil.copy(os.path.join(root, file), os.path.join(os.getcwd(), "doc", file))
    print("复制成功")


def copy_all_to_usb(cur_path, files):
    for f in files:
        copy_to_usb(cur_path, f)
