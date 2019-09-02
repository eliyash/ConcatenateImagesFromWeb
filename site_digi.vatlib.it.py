from concate import ProgInfo, run_simultaneously


def url_generator(page_num, index_w, index_h):
    return ("https://digi.vatlib.it/pub/digit/MSS_Vat.ebr.60/iiif/Vat.ebr.60_%04u_fa_%04d%s.jp2/%u,%u,512,"
            "512/512,/0/native.jpg" %
            (page_num + 7, page_num / 2 + 1, ('r' if page_num % 2 == 0 else 'v'), index_w * 512, index_h * 512))


prog_info = ProgInfo(512, 512, 4, 3, url_generator)

all_needed_pages = range(0, 360)

run_simultaneously(all_needed_pages, prog_info)
print("FINISHED!")
