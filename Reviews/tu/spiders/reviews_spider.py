import scrapy
import time
# import sys
from tu.items import TuItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class QuotesSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ['expedia.com']

    def start_requests(self):
        self.driver = webdriver.Chrome()
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        yield scrapy.Request(url="http://www.example.com", callback=self.parse, headers = headers)


    def parse(self, response):
        self.driver.get('https://www.expedia.com')
        # --------------------config area--------------------#
        # specify city(area), checkin/out date, hotel star
        #destInput = "Los Angeles"
        #destInput = "San Francisco"
        destInput = "New York"
        checkInDateInput = "03/19/2020"
        checkOutDateInput = "03/20/2020"
        # Tip: set "345" to crawl 3/4/5 class, or just one "4" for 4 class only
        # for some unknown reason, expedia may not show 1 and 2 star filter for clickble
        # besides, if you choose 3 then 5, 4 will also be choosed and non-cancellable
        # set to 0 to not use any filter.
        hotelstar = "0"

        # set 1 to choose 1 adult for search, set 0 to use default 2 adults.
        oneP = 0

        # if it is a sponsored result, set 1 to save as usual(may cause duplicate later), set 0 to drop this result.        
        sponsorAval = 0

        # if zipcode info is unknown, set 1 to save it as 'null', set 0 to drop this hotel
        hasZip = 1

        # if size info is unknown, set 1 to save it as 'null', set 0 to drop this room info row
        # about 10%-35%(vary) result items is null, blame expedia        
        sizeUnknow = 0

        # size can be 0 or ?, set 1 to save as 0, set 0 to drop this room info row
        # Note2: in very rare condition, size may be 0
        sizeBezero = 0

        # if size like"275-350", set 0 to save as 275, set 1 to save as 312, set 2 save as "275-350" 
        # Note: items like this about 2%
        sizeAvg = 0

        # if rating info is unknown, set 1 to save it as 'null', set 0 to drop this hotel
        # Note: no rating is a rare condition
        ratingUnknow = 0

        # if bed info is unknown, set 1 to save it as 'null', set 0 to drop this room info row
        # Note: no bed info is a very rare condition
        bedUnknow = 1

        # if guests info is unknown, set 1 to save it as 'null', set 0 to drop this room info row
        # Note: no guests info is a very rare condition
        guestsUnknow = 1

        # --------------------below is the code--------------------#
        # get the start window handle
        mainwin = self.driver.current_window_handle

        # switch to hotel search container
        htBtn = self.driver.find_element_by_id('tab-hotel-tab-hp')
        htBtn.click()

        # get input objects
        dest = self.driver.find_element_by_id('hotel-destination-hp-hotel')
        checkInDate = self.driver.find_element_by_id('hotel-checkin-hp-hotel')
        checkOutDate = self.driver.find_element_by_id('hotel-checkout-hp-hotel')
        searchButton = self.driver.find_element_by_xpath("//*[@id='gcw-hotel-form-hp-hotel']/div[12]/label/button")
        #people = self.driver.find_element_by_xpath(".//*[@id='gcw-hotel-form-hp-hotel']/div[3]/div[4]/label/select/option[@value='1']")

        # clear and write value to input objects
        dest.clear()
        dest.send_keys(destInput)
        checkInDate.clear()
        checkInDate.send_keys(checkInDateInput)
        checkOutDate.clear()
        checkOutDate.send_keys(checkOutDateInput)
    
        if (int(oneP) == 1):
            people.click()
        time.sleep(3)

        
        # starting search
        searchButton.click()
        
        def killwin(mainWinHandle):           
            # wait for loading and get all window handles
            time.sleep(2)
            allwin = self.driver.window_handles

            # kill popup windows that is not what we want
            for win in allwin:
                if win != mainWinHandle:
                    self.driver.switch_to_window(win)
                    self.driver.close()
                    print win," is closed."                     
            # get back to main window and prepare to work        
            self.driver.switch_to_window(mainWinHandle)
            print "backed to the main window"
            #time.sleep(4)

        killwin(mainwin)


        sel = scrapy.Selector(text = self.driver.page_source);
        js="var q=document.documentElement.scrollTop=100000" 

        # # click the more button and load more pages
        # more_flag = 1
        # clickCount = 1
        # while(more_flag): 
        #     self.driver.execute_script(js)  
        #     time.sleep(1) 
        #     try:
        #         moreButton = self.driver.find_element_by_class_name("uitk-button.uitk-button-small.uitk-button-secondary")
        #         moreButton.click()
        #         clickCount += 1
        #         print('Loading the page ' + str(clickCount))
        #         time.sleep(3)
        #     except:
        #         more_flag = 0


        # # get the hotels' links on the result pages
        hotelreviews = TuItem()
        hotel = self.driver.find_element_by_class_name("listing__link.uitk-card-link").get_attribute("href")
        time.sleep(1)

        #enter a hotel page
        self.driver.get(hotel)
        #enter review page
        repageBtn = self.driver.find_element_by_class_name("uitk-button.uitk-button-small.uitk-button-secondary")
        repageBtn.click()
        #load more review
        more_review_flag = 1
        clickCount = 1
        while(more_review_flag):
            self.driver.execute_script(js) 
            time.sleep(1)

            try:
                morereviewBtn = self.driver.find_element_by_class_name("uitk-button.uitk-button-small.uitk-button-secondary.more-reviews-button")
                morereviewBtn.click()
                print('Review Page ' + str(clickCount))
                clickCount += 1
            except:
                more_review_flag = 0
            # if (clickCount == 10):
            #     more_review_flag = 0
        
        time.sleep(1)

        article_s = self.driver.find_elements_by_class_name("review-card.all-y-padding-six")
        for article_e in article_s:
            hotelreviews['response'] = article_e.text
            yield hotelreviews 

        # usr_name_s = self.driver.find_elements_by_class_name('pwa-theme--grey-700.uitk-type-heading-300')
        # rating_s = self.driver.find_elements_by_class_name('uitk-type-heading-500.all-b-padding-three')
        # liked_s = self.driver.find_elements_by_class_name('uitk-link.all-x-gutter-two.all-t-margin-two.all-cell-shrink.uitk-link-layout-default.uitk-type-300')
        # stay_duration_s = self.driver.find_elements_by_class_name('review-stay-duration.uitk-type-200.pwa-theme--grey-700.all-t-margin-two')
        # review_date_s = self.driver.find_elements_by_class_name('review-meta-date.uitk-type-300.pwa-theme--grey-700')
        # review_s = self.driver.find_elements_by_class_name('review-text-body')
        # response_s = self.driver.find_elements_by_class_name('mgr-response')
        

        # for usr_name_e , rating_e, liked_e, stay_duration_e, review_date_e, review_e, response_e in zip(usr_name_s , rating_s, liked_s, stay_duration_s, review_date_s, review_s, response_s):
        #     # hotelreviews['hotel_name'] = self.driver.find_elements_by_class_name("").extract_first()
        #     hotelreviews['usr_name'] = usr_name_e.text
        #     hotelreviews['rating'] = rating_e.text  
        #     hotelreviews['liked'] = liked_e.text
        #     hotelreviews['stay_duration'] = stay_duration_e.text  
        #     hotelreviews['review_date'] = review_date_e.text  
        #     hotelreviews['review'] = review_e.text
        #     hotelreviews['response'] = response_e.text  
        #     yield hotelreviews

        self.driver.close()

        self.driver.quit()
        
