from concate import ProgInfo, run_simultaneously


def url_generator(page_num, index_w, index_h):
    return 'http://www.e-codices.ch/loris/bge%2Fbge-cl0145%2Fbge-cl0145_{}.jp2/{},{},1024,1024/1024,/0/default.jpg'.format(format(page_num, '03d'), index_w*1024, index_h*1024)


prog_info = ProgInfo(1024, 1024, 7, 5, url_generator)

all_needed_pages = range(1, 680)

run_simultaneously(all_needed_pages, prog_info)
print("FINISHED!")
