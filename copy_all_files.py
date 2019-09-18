import os
import re
from threading import Thread

import utils

num_worker = 4


def tf_in_p(target_file, file_name):
    for tf in target_file:
        if re.search(tf, file_name) is not None:
            return True
    return False


def get_all_dirs_and_tf(cur_path, file):
    return ([os.path.join(cur_path, p) for p in os.listdir(cur_path) if os.path.isdir(os.path.join(cur_path, p))],
            [p for p in os.listdir(cur_path) if tf_in_p(file, p)])


def deep_search_thread(paths, file):
    for path in paths:
        deep_search(path, file)


def deep_search(cur_path, file):
    try:
        dirs, found_files = get_all_dirs_and_tf(cur_path, file)
    except PermissionError:
        return

    if len(found_files) > 0:
        Thread(target=utils.copy_all_to_usb, args=(cur_path, found_files)).start()
    # for d in dirs:
    #     deep_search(d, file)
    #     Thread(target=deep_search, args=(d, file)).start()

    if len(dirs) < num_worker:
        for d in dirs:
            Thread(target=deep_search, args=(d, file)).start()
    else:
        temp = int(len(dirs) / num_worker)
        for worker_i in range(num_worker - 1):
            Thread(target=deep_search_thread,
                   args=(dirs[0 + temp * worker_i: temp * (worker_i + 1)], file)).start()
        Thread(target=deep_search_thread, args=(dirs[temp * (num_worker - 1):], file)).start()


def main(file):
    for vol in utils.get_all_vol():
        print("正在查找%s" % vol)
        Thread(target=deep_search, args=(vol, file)).start()


if __name__ == '__main__':
    main((r"\.doc$", r"\.docx$"))
