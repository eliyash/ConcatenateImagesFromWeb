from Concate import *

# with open('special_pages.txt') as f:
#     lines = f.readlines()
# pairs = [line.split() for line in lines]
# all_needed_pages = [int(pair[0]) for pair in pairs]
# page_name_dict = { int(pair[0]): pair[1] for pair in pairs}
# url_generator = lambda page_num, index_width, index_height: (
# 	"https://digi.vatlib.it/pub/digit/MSS_Vat.ebr.60/iiif/Vat.ebr.60_%04u_fa_%s.jp2/%u,%u,512,512/512,/0/native.jpg" %
# 	(page_num+7,page_name_dict[page_num],index_width*512,index_height*512)
# 	)


def url_generator(page_num, index_w, index_h):
    return ("https://digi.vatlib.it/pub/digit/MSS_Vat.ebr.60/iiif/Vat.ebr.60_%04u_fa_%04d%s.jp2/%u,%u,512,"
            "512/512,/0/native.jpg" %
            (page_num + 7, page_num / 2 + 1, ('r' if page_num % 2 == 0 else 'v'), index_w * 512, index_h * 512))


prog_info = ProgInfo(512, 512, 4, 3, url_generator)

all_needed_pages = range(0, 360)

run_simultaneously(all_needed_pages, prog_info)
print("FINISHED!")
