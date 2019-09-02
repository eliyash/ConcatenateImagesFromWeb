import urllib.request
from typing import List

from PIL import Image
import os
from threading import Thread
import math


class ProgInfo:
    def __init__(self, height_one, width_one, num_in_height, num_in_width, url_generator,
                 path_to_dirs="./",
                 download_dir="images/",
                 output_dir="output/",
                 num_of_threads=100,
                 num_of_tries_per_url=3):
        self.height_one = height_one
        self.width_one = width_one
        self.num_in_height = num_in_height
        self.num_in_width = num_in_width
        self.url_generator = url_generator
        self.path_to_output_dir = os.path.abspath(path_to_dirs + output_dir)
        self.path_to_download_dir = os.path.abspath(path_to_dirs + download_dir)
        self.num_of_threads = num_of_threads
        self.num_of_tries_per_url = num_of_tries_per_url


def downloader(url, path):
    urllib.request.urlretrieve(url, path)


def handle_page(page, info):
    path_to_download_file = os.path.join(info.path_to_download_dir, ("tempFileOfPage%d.jpg" % page))

    new_im = Image.new('RGB', (info.width_one * info.num_in_width, info.height_one * info.num_in_height))

    for i in range(0, info.num_in_width):
        for j in range(0, info.num_in_height):
            real_url = info.url_generator(page, i, j)
            problem_res = None
            for tryNum in range(0, info.num_of_tries_per_url):
                try:
                    downloader(real_url, path_to_download_file)
                    break
                except Exception as ex:
                    problem_res = ex
            else:
                # print('p:{} xy:{},{} failed, reason: {}, url-{}'.format(page, i, j, problem_res, real_url))
                return False

            try:
                im = Image.open(path_to_download_file)
                index_height = j * info.height_one - 1
                index_width = i * info.width_one - 1
                new_im.paste(im, (index_width, index_height))
            except Exception as ex:
                # print('cant open image in p:{} h:{} w:{}'.format(page, i, j, ex))
                return False

    new_im.save(os.path.join(info.path_to_output_dir, 'page' + str(page) + '.jpg'))
    # print "Success in page: {}".format(page)
    os.remove(path_to_download_file)
    return True


def handle_several_pages(pages, info, return_list):
    for page in pages:
        if handle_page(page, info):
            return_list["done"].append(page)
        else:
            return_list["broken"].append(page)

    # print('done pages: {}\n\n broken pages: {}'.format(done_pages, broken_pages))


def run_simultaneously(all_pages, info: ProgInfo):
    if not os.path.exists(info.path_to_output_dir):
        os.makedirs(info.path_to_output_dir)
    if not os.path.exists(info.path_to_download_dir):
        os.makedirs(info.path_to_download_dir)

    num_of_pages = len(all_pages)
    num_pages_per_thread = int(math.ceil(float(num_of_pages) / info.num_of_threads))

    pages_per_thread = [all_pages[i:min(i + num_pages_per_thread, num_of_pages - 1)] for i in
                        range(0, num_of_pages, num_pages_per_thread)]

    threads = []
    threads_ret_val = []
    for index, pages in enumerate(pages_per_thread):
        try:
            threads_ret_val += [{'broken': [], 'done': []}]
            new_thread = Thread(target=handle_several_pages, args=(pages, info, threads_ret_val[index]))
            new_thread.start()
            threads.append(new_thread)
        except Exception as ex:
            # print("Error: unable to start pages {}-{} thread, reason: {}".format(pages[0], pages[-1], ex))
            pass
    # join all threads
    for single_thread in threads:
        single_thread.join()

    all_broken_pages = [thread_res['broken'] for thread_res in threads_ret_val]

    print(all_broken_pages)
