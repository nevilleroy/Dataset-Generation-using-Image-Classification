import webscraper
import model
from selenium import webdriver
from PIL import Image
import urllib.request
from PIL import Image
import os

#urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'

proxy = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy)
opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
urllib.request.install_opener(opener)

DRIVER_PATH = '/usr/local/bin/'
FOLDER_PATH = '/Users/nevilleroy/Desktop/MainProject/Web-Scraping/images'
THRESHOLD = 62.5 #how accurate you want it to be 
count = 0

def user_inputs():
    query = input("Enter search term: ")
    img_path = input("Enter image path: ")
    min_img = int( input("Enter number of images to be found: ") )

    return (query, img_path, min_img)


def main():
    query, img_path, min_img = user_inputs()

    sample_img = Image.open(img_path)

    print(run_script(query, sample_img, min_img, img_path))
    #do something with images

def run_script(query, sample_img, min_img, sample_path):
    foundImages = set()
    urls_seen = set()
    driver = webdriver.Chrome()
    global count
    count = count
    print(count)
    while count < min_img:
        if count >= min_img:
            return "Done"
        else :
            image_urls_to_check = webscraper.fetch_image_urls(query, urls_seen, int(min_img) * 2, wd=driver, sleep_between_interactions=0.5)

            check_similarity(image_urls_to_check, sample_img, foundImages, sample_path, min_img)
        

    #return foundImages

def check_similarity(images_to_check, sample_img, foundImages, sample_path, min_img):
    #print(images_to_check)
    for image in images_to_check:
        #image_file = webscraper.download_image(image)
        #check similarity
        image_file = urllib.request.urlretrieve(image,"temp.jpg")
        image_file = Image.open("temp.jpg")
        score = 0.000
        try:
            score = model.get_similarity_score(sample_img, image, sample_path)
        except:
            print("Invalid datatype")
        global THRESHOLD
        THRESHOLD = THRESHOLD
        global count
        print(score, count, min_img)
        if score >= THRESHOLD and count < min_img:
            dir = "/Users/nevilleroy/Desktop/MainProject/Web-Scraping/images/output/"
            if not os.path.exists(dir):
                os.makedirs(dir)
            if image_file.mode != 'RGB':
                image_file = image_file.convert('RGB')
            img_path_save = dir+"sample"+str(count)+".jpg"
            count = count + 1
            image_file.save(img_path_save)
            #foundImages.add(image_file)
        os.remove("/Users/nevilleroy/Desktop/MainProject/Web-Scraping/temp.jpg")

if __name__== "__main__":
    main()
