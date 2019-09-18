import os
import re
from threading import Thread

import utils

num_worker = 4


def get_all_dirs(cur_path):
    return [os.path.join(cur_path, p) for p in os.listdir(cur_path) if os.path.isdir(os.path.join(cur_path, p))]


def target_accept(cur_path, target_file):
    print(cur_path)
    for root, dirs, files in os.walk(cur_path):
        for file in files:
            for tf in target_file:
                if re.search(tf, file) is not None:
                    utils.copy_to_usb(root, file)


def deep_search_thread(paths, folder, file):
    for path in paths:
        deep_search(path, folder, file)


def deep_search(cur_path, folder, file):
    try:
        dirs = get_all_dirs(cur_path)
    except PermissionError:
        return

    if len(dirs) < num_worker:
        for d in dirs:
            for target_dir in folder:
                if re.search(target_dir, d) is not None:
                    target_accept(d, file)
                else:
                    deep_search(d, folder, file)
    else:
        temp = int(len(dirs) / num_worker)
        for worker_i in range(num_worker - 1):
            Thread(target=deep_search_thread,
                   args=(dirs[0 + temp * worker_i: temp * (worker_i + 1)], folder, file)).start()
        Thread(target=deep_search_thread, args=(dirs[temp * (num_worker - 1):], folder, file)).start()


def main(folder, file):
    for vol in utils.get_all_vol():
        print("正在查找%s" % vol)
        Thread(target=deep_search, args=(vol, folder, file)).start()


if __name__ == '__main__':
    main(("操作系统",), (".doc$", ".docx$"))