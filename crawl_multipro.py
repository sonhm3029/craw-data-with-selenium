from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import multiprocessing as mp
import time
import pandas as pd
import csv


class Crawl_Feedback(object):

    #Using data frame from pandas lib to store crawled data
    data_frame = pd.DataFrame()
    with open('new1.csv','a',encoding="utf-8") as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(["Category","Feedback","Rate"])
    error_catching = 0
    
    #Define chrome driver to use
    driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')

    #####                               CLASS FUNCTION                              #####
    #Function to open shopee on chrome browser
    def openChrome(self):
        (self.driver).get("https://shopee.vn/")
        (self.driver).maximize_window()
        #Close pop up advertisement if found
        self.close_popup()
    
    #Function to close pop up ad
    def close_popup(self):
        try:
            #find element representing the close button
            close_ad = WebDriverWait(self.driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"shopee-popup__close-btn"))
            )
            #click button to close pop up ad
            close_ad.click()
        except:
            print("There's no pop up")

    #Fucntion to get category
    def get_category(self):
        #find all categories's element
        categories = WebDriverWait(self.driver,15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,"_13sfos"))  #find class name of categories
        )
        list_category = [] #array to store name of categories
        #Take category's name and store in a array to access in next step
        count = 0
        for category in categories:
            name_category = category.text
            list_category.append(name_category)
        number_of_category = len(list_category)
        
        return list_category
    
    #Function scroll down page 1
    def scroll_down1(self):
        time.sleep(5)
        (self.driver).execute_script("window.scrollBy(0,2000)","")
        time.sleep(4)
        (self.driver).execute_script("window.scrollBy(0,1000)","")
        time.sleep(4)
        (self.driver).execute_script("window.scrollBy(0,500)","")
        time.sleep(4)
        (self.driver).execute_script("window.scrollBy(0,1000)","")
        time.sleep(4)
    
    # Function scroll down page 2
    def scroll_down2(self):
        time.sleep(4)
        (self.driver).execute_script("window.scrollBy(0,1000)","")
        time.sleep(4)
        (self.driver).execute_script("window.scrollBy(0,1800)","")
        time.sleep(4)
    
    #Function to write data to csv file
    def write_dataCsv(self,type_product,list_comments,list_num_rating):
        dict = {'Category':type_product,'Feedback': list_comments,'Rate': list_num_rating}
        df = pd.DataFrame(dict)
        file_name = type_product+".csv"
        df.to_csv(file_name,mode= 'a',header = False, index = False)
        print('Write file Successfully !')

    #Function to crawl comments and rating star
    def take_feedback(self,list_comments,list_num_rating):
        try:
            comments = WebDriverWait(self.driver,3).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"shopee-product-rating__content"))
            )
            #Take number of rating stars
            for rating in (self.driver).find_elements_by_css_selector('.shopee-product-rating'):
                stars = rating.find_elements_by_css_selector('.icon-rating-solid')
                num = len(stars)
                list_num_rating.append(num)
                print("ok1")

            #Take customer comments
            for comment in comments:
                string = comment.text
                list_comments.append(string)
                print("oke2")

        except:
            self.error_catching =1
        
        return list_comments,list_num_rating



        

    # Main function to crawl data
    def crawl_data(self,type_product):
        self.openChrome()
        try:
            time.sleep(3)
            #Put an exception handle to close popup
            self.close_popup()
            #Find categỏies and Click to navigating to categories
            link_to_category = (self.driver).find_element_by_link_text(type_product)
            link_to_category.click()
            #Scroll down to load element and click in product
            self.scroll_down1()
            new_products = WebDriverWait(self.driver,10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"_35LNwy"))      #find classname of products
            )
            number_of_products = len(new_products)
            ################################################3
            #chose product 
            for i in range(1,number_of_products-45):
                y = str(i)      #index in xpath of product
                new_product = WebDriverWait(self.driver,10).until(
                    EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div/div[2]/div[2]/div[4]/div[2]/div/div[2]/div['+y+']'))
                )
                new_product.click()         #click to view comment of product
                #SCroll down to load the comment of customer
                self.scroll_down2()
                list_comments = []
                list_num_rating = []
                try:
                    #Go to comment page of 5-4-3-2-1 stars rating
                    for num_rate in range(2,7):
                        Overview_rating = WebDriverWait(self.driver,3).until(
                            EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div['+str(num_rate)+']'))
                        )
                        time.sleep(3)
                        Overview_rating.click()
                        self.error_catching = 0
                        #Take the feedback of customer

                        self.take_feedback(list_comments,list_num_rating)
                    #write csv file
                    self.write_dataCsv(type_product,list_comments,list_num_rating)
                except:
                    self.error_catching =1

                time.sleep(5)
                (self.driver).back()#back to category page to chose another product
                time.sleep(5)
            print("Success !")
        except:
            print("An error has occured !")
            (self.driver).quit()

    def multiprocess(self):
        self.openChrome()
        list_category = self.get_category()
        pool = mp.Pool()
        pool.map(self.crawl_data,list_category)

            


if __name__ == '__main__':
    crawl_machine = Crawl_Feedback()
    crawl_machine.multiprocess()
