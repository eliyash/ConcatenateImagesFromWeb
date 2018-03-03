from PIL import Image
import urllib2
import os
from threading import Thread
import math

class ProgInfo:
    def __init__(self,height_one,width_one,num_in_height,num_in_width,url_generator,
                 path_to_dirs="./",
                 download_dir="images/",
                 output_dir="output/",
                 num_of_threads=100,
                 num_of_trys_per_url=3):
        self.height_one = height_one
        self.width_one = width_one
        self.num_in_height = num_in_height
        self.num_in_width = num_in_width
        self.url_generator = url_generator
        self.path_to_output_dir = os.path.abspath(path_to_dirs+output_dir)
        self.path_to_download_dir = os.path.abspath(path_to_dirs+download_dir)
        self.num_of_threads = num_of_threads
        self.num_of_trys_per_url = num_of_trys_per_url

def downloader(url,path):
	request = urllib2.Request(url)
	request.add_header('User-agent', "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5." )
	opener = urllib2.build_opener()
	f = open(path,'wb')
	f.write(opener.open(request).read())
	f.close()

def handle_page(page,prog_info):
	path_to_download_file = os.path.join(prog_info.path_to_download_dir,("tempFile%d.jpg"%page))
    # os.path.abspath(path_to_dirs+download_dir+(temp_file_name%page))
	broken_images = []

	new_im = Image.new('RGB', (prog_info.width_one*prog_info.num_in_width,prog_info.height_one*prog_info.num_in_height))
	index_height = 0
	index_width = 0
	for i in range(0,prog_info.num_in_width):
		for j in range(0,prog_info.num_in_height):
			for tryNum in range(0,prog_info.num_of_trys_per_url):
				try:
					real_url = prog_info.url_generator(page,i,j)
					print "trying : page: %d , XY: %d,%d\n %s" % (page,i,j,real_url)

					downloader(real_url,path_to_download_file)
					break
				except Exception as e:
					print(e)
					if tryNum==prog_info.num_of_trys_per_url-1 :
						broken_images.append({page,i,j})
						# print "BrokenPage added, num %d in %s" % (tryNum,url % (page/100,page/10%10,page%10,i,j))
					else : print "error num %d" % (tryNum)
			else: break
			try:
				im=Image.open(path_to_download_file)
				index_height = j*prog_info.height_one-1
				index_width = i*prog_info.width_one-1
				new_im.paste(im,(index_width,index_height))
			except Exception as e:
				print(e)
				print "cant open image in %d %d %d" % (page,i,j)
				broken_images.append({page,i,j})
	# error_pages[page] = broken_images
	new_im.save(os.path.join(prog_info.path_to_output_dir,'Epage'+str(page)+'.jpg'))
	return broken_pages
	# os.remove(os.path.abspath(path_to_dirs+download_dir+temp_file_name))

def handle_several_pages(pages,prog_info):
    broken_pages = []
	for page in pages:
		new_broken_pages = handle_page(page,prog_info)
        broken_pages.append(new_broken_pages)
    print(broken_pages)

def run_simultinesly(num_of_threads,prog_info):
	num_of_pages = len(all_needed_pages)
	num_of_threads = min(num_of_pages,prog_info.num_of_threads)
	num_pages_per_thread = int(math.ceil(float(num_of_pages) / prog_info.num_of_threads))

	pages_per_thread = [all_needed_pages[i:min(i + num_pages_per_thread,num_of_pages-1)] for i in range(0, num_of_pages, num_pages_per_thread)]

	threads = []
	# error_pages = []
	for pages in pages_per_thread:
		try:
		    new_thread = Thread(target=handle_several_pages, args=(pages,prog_info, ))
		    new_thread.start()
		    threads.append(new_thread)
			# error_pages[page] = []
		except:
			print("Error: unable to start pages %d-%d thread"%(pages[0],pages[-1]))
			broken_pages.append(pages)

	# join all threads
	for single_thread in threads:
	    single_thread.join()

# TODO: move configuration to new file

# with open('special_pages.txt') as f:
#     lines = f.readlines()
# pairs = [line.split() for line in lines]
# all_needed_pages = [int(pair[0]) for pair in pairs]
# page_name_dict = { int(pair[0]): pair[1] for pair in pairs}
# url_generator = lambda page_num, index_width, index_height: (
# 	"https://digi.vatlib.it/pub/digit/MSS_Vat.ebr.60/iiif/Vat.ebr.60_%04u_fa_%s.jp2/%u,%u,512,512/512,/0/native.jpg" %
# 	(page_num+7,page_name_dict[page_num],index_width*512,index_height*512)
# 	)

all_needed_pages = range(0,360)

url_generator = lambda page_num, index_width, index_height: (
	"https://digi.vatlib.it/pub/digit/MSS_Vat.ebr.60/iiif/Vat.ebr.60_%04u_fa_%04d%s.jp2/%u,%u,512,512/512,/0/native.jpg" %
	(page_num+7,page_num/2+1,('r' if page_num%2 == 0 else 'v'),index_width*512,index_height*512)
	)


prog_info = ProgInfo(512,512,4,3,url_generator)
run_simultinesly(all_needed_pages,prog_info)
print("FINISHED!")
