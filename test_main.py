from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from time import sleep
import pyautogui
import allcitylist
import get_latitude_and_longitude
import re
import quickstart
all_city_list = allcitylist.get_all_cities()


hotel_count= 0



for city in all_city_list:
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://www.makemytrip.com/hotels/")
        
        try:
            accept_cookie_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class=\"cookiesModal__acceptCookiesBtn buttonCls btn__primary uppercase \"]")))
            accept_cookie_button.click()
        except:
            pass

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-cy=\"city\"]"))).click()

        search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder=\"Where do you want to stay?\"]")))
        search_input.send_keys(city)
        sleep(5)

        suggest_list = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li[class=\"react-autosuggest__suggestion react-autosuggest__suggestion--first\"]")))
        suggest_list.click()
        sleep(5)

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"DayPicker-NavButton DayPicker-NavButton--next\"]")))

        count = 2

        for _ in range(count):
            next_month = driver.find_element(By.CSS_SELECTOR, "span[class=\"DayPicker-NavButton DayPicker-NavButton--next\"]")
            next_month.click()
            sleep(1)

        datepicker_week = driver.find_elements(By.CSS_SELECTOR, "div[class=\"DayPicker-Week\"]")[1]
        datepicker_days = datepicker_week.find_elements(By.CSS_SELECTOR, "div[class=\"DayPicker-Day\"]")
        datepicker_days[3].click()
        sleep(1)
        datepicker_days[4].click()
        sleep(1)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class=\"primaryBtn btnApplyNew pushRight capText\"]"))).click()
        sleep(1)

            
        # pyautogui.click(10, 500)

        sleep(2)

        search_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-cy=\"submit\"]")))
        search_button.click()

        sleep(3)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"listingRowOuter hotelTileDt makeRelative \"]")))

        try:
            lowest_price_tab = driver.find_elements(By.CSS_SELECTOR, "span[class=\"srtByFltr__list--itemSubTitle\"]")[1]
            lowest_price_tab.click()
        except:
            pass

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"listingRowOuter hotelTileDt makeRelative \"]")))

        # Get the initial page height
        page_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            hotel_list = driver.find_elements(By.CSS_SELECTOR, "div[class=\"listingRowOuter hotelTileDt makeRelative \"]")
            sleep(0.3)

            try:
                end_contet = driver.find_element(By.CSS_SELECTOR, "p[class=\"appendTop20 appendBottom20 font22 latoBlack blackText textCenter\"]")
                if end_contet:
                    print(f"Scroll End", end_contet.text)
                    break
            except:
                continue

        hotel_list = driver.find_elements(By.CSS_SELECTOR, "div[class=\"listingRowOuter hotelTileDt makeRelative \"]")

        city_name = driver.find_element(By.CSS_SELECTOR, "input[id=\"city\"]").get_attribute('value')

        for index, hotel in enumerate(hotel_list):
            
            try:
                hotel_id = "Listing_hotel_" + str(index)
                scroll_content = driver.find_element(By.ID, hotel_id)
                
                driver.execute_script("arguments[0].scrollIntoView(false); window.scrollBy(0, 50);", scroll_content)
                print(f"index =", index)
                
                try:
                    location = hotel.find_element(By.CSS_SELECTOR, "span[class=\"blueText\"]").text
                except:
                    location = ""
                star_category = ""
                star_category_dom = None
                try:
                    try:
                        star_category_dom = hotel.find_element(By.CSS_SELECTOR, "span[id=\"hlistpg_hotel_star_rating\"]")
                        star_category = star_category_dom.get_attribute("data-content") + " Star"
                        # star_category = star_category[-6:]
                    except:
                        star_category = hotel.find_element(By.CSS_SELECTOR, "span[class=\"latoRegular darkText\"]").text + " Star"
                        # star_category = star_category[-6:]
                except:
                    pass
                
                try:
                    price = hotel.find_element(By.CSS_SELECTOR, "p[id=\"hlistpg_hotel_shown_price\"]").text
                except:
                    price = ""
                try:
                    couple_friendly_text = hotel.find_element(By.CSS_SELECTOR, "div[class=\"persuasion__item pc__hotelCategoryPerNew\"]").text
                    if couple_friendly_text == "Couple Friendly":
                        couple_friendly = "Allowed"
                except:
                    couple_friendly = "NO"
                    
                try:
                    hotel_name = hotel.find_element(By.CSS_SELECTOR, "span[class=\"wordBreak appendRight10\"]").text
                except:
                    hotel_name = ""
                
                try:
                    error_hotel = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, hotel_id)))
                    error_hotel.click()
                    print(f"index = ", hotel_id)
                except:
                    continue
                
                sleep(3)
                window_handles = driver.window_handles
                driver.switch_to.window(window_handles[1])
                sleep(3)
                
                url = driver.current_url    
                url_without_question_mark = url[url.find("?") + 1:]
                url_units = re.split("&", url_without_question_mark)
                hotel_id_unit = url_units[0]
                hotel_id = hotel_id_unit[hotel_id_unit.find("hotelId=") + 8:]
                lat_unit = url_units[6]
                lng_unit = url_units[7]
                lat = lat_unit[lat_unit.find("lat=") + 4:]
                lng = lng_unit[lng_unit.find("lat=") + 5:]
                print(f'Hotel ID is ', hotel_id)
                
                mmt_value="NA"
                try:
                    try:
                        mmt_luxe = driver.find_element(By.CSS_SELECTOR, "p[class=\"prmum__header--hotelPersuasion\"]")
                        try:
                            mmt_luxe_img = mmt_luxe.find_element(By.TAG_NAME, "img")
                            mmt_value = "MMT LUXE"
                        except:
                            pass
                    except:
                        mmt_value_stay = driver.find_element(By.CSS_SELECTOR, "div[class=\"appendBottom16\"]")
                        try:
                            mmt_value_img = mmt_value_stay.find_element(By.TAG_NAME, "img")
                            mmt_value = "MMT ValueStays"
                        except:
                            pass
                except:
                    pass
                
                driver.execute_script("window.scrollTo(0, 0)")
                sleep(2)
                
                try:
                    # driver.find_element(By.CSS_SELECTOR, "div[class=\"accoDtlHdr__left--info\"]").click()
                    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"accoDtlHdr__left--info\"]"))).click()
                except:
                    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id=\"detpg_headerleft_view_photos\"]"))).click()
                    
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"sprite icGridDefault\"]"))).click()
                sleep(5)
                
                image_listing = driver.find_element(By.CSS_SELECTOR, "ul[class=\"imageListing\"]")
                image_items = image_listing.find_elements(By.TAG_NAME, "li")
                number_of_property_photos = len(image_items)
                
                def get_img_urls(text):
                    words = text.split(' ')
                    if len(words) == 1:
                        modify_text = text[0] + text[1:].lower()
                    else:
                        modify_text = words[0][0] + words[0][1:].lower()+ " " + ' '.join(word.capitalize() for word in words[1:])

                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[text()='" + modify_text + "']"))).click()
                    image_listing = driver.find_element(By.CSS_SELECTOR, "ul[class=\"imageListing\"]")
                    image_items = image_listing.find_elements(By.TAG_NAME, "li")
                    img_urls = []
                    for image_item in image_items:
                        img = image_item.find_element(By.TAG_NAME, "img")
                        url = img.get_attribute("src")
                        img_urls.append(url)
                    return ",".join(img_urls)
                
                room_photos = ""
                outdors_photos = ""
                reception_photos = ""
                entrance_photos = ""
                washroom_photos = ""
                interior_photos = ""
                restaurant_photos = ""
                swimmingpool_photos = ""
                
                image_detail_container = driver.find_element(By.CSS_SELECTOR, "ul[class=\"hotelTags font12 latoBold whiteText\"]")
                image_detail_list = image_detail_container.find_elements(By.TAG_NAME, "li")
                
                for img_list in image_detail_list:
                    sleep(2)
                    if "room" in img_list.text.lower():
                        room_photos = get_img_urls(img_list.text)
                        sleep(2)
                    if  "outdoors" in img_list.text.lower():
                        outdors_photos = get_img_urls(img_list.text)
                        sleep(2)
                    if  "reception" in img_list.text.lower():
                        reception_photos = get_img_urls(img_list.text)
                        sleep(2)
                    if "entrance" in img_list.text.lower():
                        entrance_photos = get_img_urls(img_list.text)
                        sleep(2)
                    if "washroom" in img_list.text.lower():
                        washroom_photos = get_img_urls(img_list.text)
                        sleep(2)
                    if "interior" in img_list.text.lower():
                        interior_photos = get_img_urls(img_list.text)
                        sleep(2)
                    if "restaurant" in img_list.text.lower():
                        restaurant_photos = get_img_urls(img_list.text)
                        sleep(2)
                    if "swimming pool" in img_list.text.lower():
                        swimmingpool_photos = get_img_urls(img_list.text)
                        sleep(2)  

                
                
                gallary_layout = driver.find_element(By.CSS_SELECTOR, "div[class=\"phtGallry__header--right\"]")
                close_gallary = gallary_layout.find_element(By.CSS_SELECTOR, "a[class=\"closeBtn\"]")
                close_gallary.click()
                sleep(1)
                    
                room_size = ""
                view_type = "NA"
                bed_type = ""
                number_of_people = ""
                work_desk = "NA"
                free_cancelation = "NA"
                room_only = "NA"
                breakfast = "NA"
                lunch_include = "NA"
                dinner_include = "NA"
                lunch_dinner_include = "NA"
                mini_refrigerator = "NA"
                smoke_detector = "NA"
                smoke_allowed = "NA"
                air_conditioning = "NA"
                in_room_safe = "NA"
                tv = "NA"
                balcony_terrace = "NA"
                air_purifier = "NA"
                minearal_water = "NA"
                iron_board = "NA"
                toiletries = "NA"
                hair_dryer = "NA"
                dental_kit = "NA"
                towel = "NA"
                ceiling_fun = "NA"
                room_amenities = ""
                
                room_section = driver.find_elements(By.CSS_SELECTOR, "section[class=\"page__section appendBottom35\"]")[0]    
                
                try:
                    room_data_conatiner = driver.find_element(By.CSS_SELECTOR, "div[class=\"rmSelect__card--wrap\"]")
                    room_data_lists = room_data_conatiner.find_elements(By.CSS_SELECTOR, "div[class=\"rmSelect__card--wrapRow\"]")

                    all_room_data = []
                    for room_list in room_data_lists:
                        room_data = {
                            'room_name': "",
                            'room_size': "",
                            "free_cancelation": "NA",
                            'view_type':"NA",
                            'bed_type': "",
                            "number_of_people": "",
                            "work_desk": "NA",
                            "room_only": "NA",
                            "breakfast": "NA",
                            "lunch_include": "NA",
                            "dinner_include": "NA",
                            "lunch_dinner_include": "NA",
                            "mini_refrigerator": "NA",
                            "smoke_detector": "NA",
                            "smoke_allowed": "NA",
                            "air_conditioning": "NA",
                            "in_room_safe": "NA",
                            "tv": "NA",
                            "balcony_terrace": "NA",
                            "air_purifier": "NA",
                            "minearal_water": "NA",
                            "iron_board": "NA",
                            "toiletries": "NA",
                            "hair_dryer": "NA",
                            "dental_kit": "NA",
                            "towel": "NA",
                            "ceiling_fun": "NA",
                            "room_amenities": ""
                        }
                        try:
                            room_data['room_name'] = room_list.find_element(By.CSS_SELECTOR, "h2[class=\"rmType__roomName\"]").text
                        except:
                            room_data['room_name'] = ""
                        try:
                            number_of_people = room_list.find_element(By.CSS_SELECTOR, "ul[class=\"exact_room_occupancy appendBottom20\"]")
                            room_data['number_of_people'] = number_of_people.find_element(By.TAG_NAME, "p").text
                        except:
                            room_data['number_of_people'] = ""
                        try:
                            detail_button = room_list.find_element(By.CSS_SELECTOR,  "a[class=\"latoBlack font14 capText\"]")
                            detail_button.click()
                            sleep(1)
                            try:
                                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class=\"rmDtl__amenities--listMore\"]")))
                            except:
                                pass
                            try:
                                more_buttons = driver.find_elements(By.CSS_SELECTOR, "span[class=\"rmDtl__amenities--listMore\"]")
                                if len(more_buttons) != 0:
                                    for more in more_buttons:
                                        more.click()
                                try:
                                    room_amenities_elements = driver.find_elements(By.CSS_SELECTOR, "li[class=\"lineHight20 makeFlex\"]")
                                    room_amenities_array = []
                                    for element in room_amenities_elements:
                                        room_amenities_array.append(element.text)
                                        
                                    room_amenities = ', '.join(room_amenities_array)
                                    room_data['room_amenities'] = room_amenities
                                except:
                                    pass
                                
                                try:
                                    side_bed_view_container = driver.find_element(By.CSS_SELECTOR, "ul[class=\"rmDtlPop__featuresList appendTop20\"]")
                                    size_bed_view = side_bed_view_container.find_elements(By.TAG_NAME, 'li')
                                    for item in size_bed_view:
                                        if "sq.ft" in item.text:
                                            room_data['room_size'] = item.text
                                        if "bed" in item.text.lower():
                                            room_data['bed_type'] = item.text
                                        if "view" in item.text.lower():
                                            room_data['view_type'] = item.text
                                            
                                except:
                                    pass
                                try:
                                    room_facility_container = driver.find_element(By.CSS_SELECTOR, "div[class=\"rmDtlPop__amenities appendTop30\"]")
                                    room_facility_lists_1 = room_facility_container.find_elements(By.CSS_SELECTOR, "span[class=\"font14 latoBlack\"]")
                                    for list_1 in room_facility_lists_1:
                                        if "Work Desk" in list_1.text:
                                            room_data['work_desk'] = "Yes"
                                        if "Air Purifier" in list_1.text:
                                            room_data["air_purifier"] = "Yes"
                                            
                                    room_facility_lists_2 = room_facility_container.find_elements(By.CSS_SELECTOR, "span[class=\"font14 \"]")
                                    for list in room_facility_lists_2:
                                        if "Smoke Alarm" in list.text:
                                            room_data['smoke_detector'] = "Yes"
                                        if "Refrigerator" in list.text:
                                            room_data['mini_refrigerator'] = "Yes"
                                        if "Smoking Room" in list.text:
                                            room_data['smoke_allowed'] = "Yes"
                                        if "Air Conditioning" in list.text:
                                            room_data['air_conditioning'] = "Yes"
                                        if "In Room Safe" in list.text:
                                            room_data["in_room_safe"] = "Yes"
                                        if "TV" in list.text:
                                            room_data["tv"] = "Yes"
                                        if  "Balcony/Terrace" in list.text:
                                            room_data["balcony_terrace"] = "Yes"
                                        if "Mineral Water" in list.text:
                                            room_data['minearal_water'] = "Yes"
                                        if "Iron/Ironing Board" in list.text:
                                            room_data['iron_board'] = "Yes"
                                        if "Toiletries" in list.text:
                                            room_data['toiletries'] = "Yes"
                                        if "Hairdryer" in list.text:
                                            room_data['hair_dryer'] = "Yes"
                                        if "Dental Kit" in list.text:
                                            room_data['dental_kit'] = "Yes"
                                        if "Towel" in list.text:
                                            room_data["towel"] = "Yes"
                                        if "Fan" in list.text:
                                            room_data['ceiling_fun'] = "Yes"
                                        if "Work Desk" in list.text:
                                            room_data['work_desk'] = "Yes"
                                        if "Air Purifier" in list.text:
                                            room_data["air_purifier"] = "Yes"
                                except:
                                    pass
                                
                                try: 
                                    room_plan_container = room_list.find_element(By.CSS_SELECTOR, "div[class=\"rmSelect__card--right\"]")
                                    room_plan_lists = room_plan_container.find_elements(By.CSS_SELECTOR, "div[class=\"rmSelect__card--row \"]")
                                    for list in room_plan_lists:
                                        text_list = list.text
                                        if "Free Cancellation" in text_list:
                                            room_data['free_cancelation'] = "Yes"
                                        if "Room Only" in text_list:
                                            room_data['room_only'] = "Yes"
                                        if "Breakfast" in text_list:
                                            room_data['breakfast'] = "Yes"
                                        if "Lunch" in text_list:
                                            room_data['lunch_include'] = "Yes"
                                        if "Dinner" in text_list:
                                            room_data['dinner_include'] = "Yes"
                                        if "Lunch/Dinner" in text_list:
                                            room_data['lunch_dinner_include'] = "Yes"
                                except:
                                    pass
                            except:
                                pass
                            
                        except:
                            pass
                        all_room_data.append(room_data)
                        sleep(3)
                        try:
                            driver.find_element(By.CSS_SELECTOR, "span[class=\"cm__modalClose \"]").click()
                        except:
                            pass
                except:
                    pass
                
                try:
                    number_of_room_text = driver.find_element(By.CSS_SELECTOR, "h4[class=\"rmTypeDropDown__heading\"]").text
                    number_of_rooms = re.findall(r'\d+', number_of_room_text)[0]
                except:
                    number_of_rooms = 1
                try:
                    description_section = driver.find_element(By.CSS_SELECTOR, "section[class=\"page__section appendBottom35\"]")
                    description = description_section.find_elements(By.TAG_NAME, "div")[1].text
                    try:
                        read_more_button_parent = description_section.find_elements(By.TAG_NAME, "div")[1]
                        read_more_button = read_more_button_parent.find_element(By.CSS_SELECTOR, "a[class=\"latoBold\"]")
                        driver.execute_script("arguments[0].scrollIntoView(false);", read_more_button)
                        read_more_button.click()
                        sleep(2)
                        description = driver.find_element(By.CSS_SELECTOR, "div[class=\"propDetailsModal__desc\"]").text
                        
                        driver.find_element(By.CSS_SELECTOR, "span[class=\"propDetails__close\"]").click()
                    except:
                        pass
                    phrases_to_remove = ["Food and Dining", "Location & Surroundings", "Property Highlights", "Room Details & Amenities", "Activities & Nearby Attractions", "How to Reach the Property"]
                    for phrase in phrases_to_remove:
                        description = description.replace(phrase, "")
                    description = description.rstrip("\n")
                except:
                    description = ""
                food_and_dining = ""
                location_and_surroundings = ""
                property_highlights = ""
                room_details_and_amenities = ""
                sleep(3)
                try:
                    try:
                        detail_ul_element = driver.find_element(By.CSS_SELECTOR, "ul[class=\"abpp__bottom--links\"]")
                    except:
                        detail_ul_element = driver.find_element(By.CSS_SELECTOR, "ul[class=\"abtPptDtlsTags\"]")
                        
                    driver.execute_script("arguments[0].scrollIntoView(false);", detail_ul_element)
                    sleep(2)
                    detail_ul_element.find_element(By.TAG_NAME, "li").click()
                    
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class=\"prptModal__contentSection\"]")))
                    
                    detail_sections = driver.find_elements(By.CSS_SELECTOR, "div[class=\"prptModal__contentSection\"]")

                    if len(detail_sections) == 3:
                        property_highlights = detail_sections[0].text
                        def remove_previous_next(string):
                            if string.endswith("Next"):
                                return string[:-13]  # Remove "Previous" and the preceding space
                            else:
                                return string
                        property_highlights = remove_previous_next(property_highlights)

                        room_details_and_amenities = detail_sections[1].text + "\n\n" + detail_sections[2].text
                    else:
                        food_and_dining = detail_sections[0].text
                        location_and_surroundings = detail_sections[1].text
                        property_highlights = detail_sections[2].text
                        def remove_previous_next(string):
                            if string.endswith("Next"):
                                return string[:-13]  # Remove "Previous" and the preceding space
                            else:
                                return string
                        property_highlights = remove_previous_next(property_highlights)
                        
                        room_details_and_amenities = detail_sections[3].text + "\n\n" + detail_sections[4].text + "\n\n" + detail_sections[5].text
                except:
                    try:
                        food_and_dining = driver.find_element(By.CSS_SELECTOR, "div[class=\"fnd appendTop40\"]").text
                    except:
                        pass    
                try:
                    driver.find_element(By.CSS_SELECTOR, "span[class=\"prptModal__close\"]").click()
                except:
                    pass

                try:
                    if food_and_dining == "":
                        food_and_dining = driver.find_element(By.CSS_SELECTOR, "div[class=\"fnd appendTop40\"]").text
                except:
                    pass
                sleep(2)
                
                try:
                    check_in_time = driver.find_element(By.CSS_SELECTOR, "span[class=\"latoBlack appendRight5\"]").text
                except:
                    check_in_time = ""
                try:
                    check_out_time = driver.find_element(By.CSS_SELECTOR, "span[class=\"latoBlack appendLeft5\"]").text
                except:
                    check_out_time = ""

                cctv = "NA"
                security_guard = "NA"
                fire_extinguishers = "NA"
                first_aid_services = "NA"
                wake_up_call = "NA"
                luggage_assistance = "NA"
                reception = "NA"
                banquet = "NA"
                conference_room = "NA"
                spa = "NA"
                restaurant = "NA"
                indoor_games = "NA"
                _25_hour_roo_service = "NA"
                wheelchair = "NA"
                lounge = "NA"
                bar = "NA"
                cafe = "NA"
                steam_and_sauna = "NA"
                salon = "NA"
                yoga = "NA"
                kids_play_area = "NA"
                library = "NA"
                dry_cleaning_service = "NA"
                laundry_service = "NA"
                housekeeping = "NA"
                power_backup = "NA"
                elevator_lift = "NA"
                intercom = "NA"
                wi_fi = "NA"
                newspaper = "NA"
                parking = "NA"
                airport_transfer_available = "NA"
                vehicle_rentals = "NA"
                medical_services = "NA"
                atm = "NA"
                currency_excahnge = "NA"
                bonfire = "NA"
                all_amenities = ""

                facilities_section = driver.find_elements(By.CSS_SELECTOR, "section[class=\"page__section appendBottom35\"]")[2]
                try:
                    all_facilities_button = facilities_section.find_element(By.CSS_SELECTOR, "a[class=\"font14 latoBlack blueText\"]")
                    driver.execute_script("arguments[0].scrollIntoView();", facilities_section)
                    all_facilities_button.click()
                    sleep(1)
                    try:
                        more_buttons = facilities_section.find_elements(By.CSS_SELECTOR, "li[class=\"lineHight20 makeFlex pointer\"]")
                        for more in more_buttons:
                            more.click()
                        
                        elements = facilities_section.find_elements(By.CSS_SELECTOR, "li[class=\"lineHight20 makeFlex\"]")
                        array = []
                        for element in elements:
                            array.append(element.text)
                            
                        all_amenities = ', '.join(array)

                        for amenity in array:
                            if "CCTV" == amenity:
                                cctv = "Yes"
                            if "Security Guard" == amenity or "Safety and Security" == amenity or "Security alarms" == amenity or "24-hour Security" == amenity:
                                security_guard = "Yes"
                            if "Fire Extinguishers" == amenity:
                                fire_extinguishers = "Yes"
                            if "First-aid Services" == amenity:
                                first_aid_services = "Yes"
                            if "Wake-up Call" == amenity:
                                wake_up_call = "Yes"
                            if "Luggage Assistance" == amenity:
                                luggage_assistance = "Yes"
                            if "Reception" == amenity:
                                reception = "Yes"
                            if "Banquet" == amenity:
                                banquet = "Yes"
                            if "Conference Room" == amenity:
                                conference_room = "Yes"
                            if "Spa" == amenity:
                                spa = "Yes"
                            if "Restaurant" == amenity:
                                restaurant = "Yes"
                            if "Indoor Games" == amenity:
                                indoor_games = "Yes"
                            if "24-hour Room Service" == amenity:
                                _25_hour_roo_service = "Yes"
                            if "Wheelchair" == amenity:
                                wheelchair = "Yes"
                            if "Lounge" == amenity:
                                lounge = "Yes"
                            if "Bar" == amenity:
                                bar = "Yes"
                            if "Cafe" == amenity or "24-hour Cafe" == amenity:
                                cafe = "Yes"
                            if "Steam and Sauna" == amenity:
                                steam_and_sauna = "Yes"
                            if "Salon" == amenity:
                                salon = "Yes"
                            if "Yoga" == amenity:
                                yoga = "Yes"
                            if "Kids Play Area" == amenity:
                                kids_play_area = "Yes" 
                            if "Library" == amenity:
                                library = "Yes"
                            if "Dry Cleaning Service" == amenity:
                                dry_cleaning_service = "Yes" 
                            if "Laundry Service" == amenity:
                                laundry_service = "Yes"
                            if "Housekeeping" == amenity:
                                housekeeping = "Yes"
                            if "Power Backup" == amenity:
                                power_backup = "Yes"
                            if "Elevator/Lift" == amenity:
                                elevator_lift = "Yes"
                            if "Intercom" == amenity:
                                intercom = "Yes"
                            if "Wi-Fi" == amenity or "Free Wi-Fi" == amenity:
                                wi_fi = "Yes"
                            if "Newspaper" == amenity:
                                newspaper = "Yes"
                            if "Parking" == amenity or "Free Parking" == amenity or "Valet parking" == amenity or "Paid On-site Parking" == amenity or "Paid Valet Parking" == amenity:
                                parking = "Yes"
                            if "Airport Transfers" == amenity or "Paid Airport Transfers" == amenity:
                                airport_transfer_available = "Yes"
                            if "Vehicle Rentals" == amenity:
                                vehicle_rentals = "Yes"
                            if "Medical Services" == amenity:
                                medical_services = "Yes"
                            if "ATM" == amenity:
                                atm = "Yes" 
                            if "Currency Exchange" == amenity:
                                currency_excahnge = "Yes"
                            if "Bonfire" == amenity:
                                bonfire = "Yes"
                
                    except:
                        pass
                except:
                    pass
                
                sleep(3)
                try:
                    driver.find_element(By.CSS_SELECTOR, "span[class=\"cm__modalClose \"]").click()
                except:
                    pass
                
                sleep(3)
                
                pet_friendly = "NA"
                outside_food_allowed = "NA"
                smoking_allowed = "NA"
                all_property_rules_result = ""
                try:
                    all_property_rules = driver.find_element(By.CSS_SELECTOR, "a[class=\"htlRules__viewAllBtn inlineFlex capText\"]")
                    driver.execute_script("arguments[0].scrollIntoView(false); window.scrollBy(0, 100)", facilities_section)
                    all_property_rules.click()
                    sleep(2)
                    property_rules = driver.find_element(By.CSS_SELECTOR, "div[class=\"htlRules__popup--content\"]")
                    
                    property_rules_elements = driver.find_elements(By.CSS_SELECTOR, "li[class=\"htlRulesPopup__list--item\"]")
                    property_array = []
                    for element in property_rules_elements:
                        text = element.text
                        if text.endswith("."):
                            text =  text[:-1]
                        property_array.append(text)
                        
                    all_property_rules_result = ", ".join(property_array)
                    if "Pets are not allowed" in property_rules.text:
                        pet_friendly = "NO"
                    if "Pets are allowed" in property_rules.text:
                        pet_friendly = "Allowed"
                    if "Outside food is not allowed" in property_rules.text:
                        outside_food_allowed = "NO"
                    if "Outside food is allowed" in property_rules.text:
                        outside_food_allowed = "Allowed"
                    if "Smoking within the premises is allowed" in property_rules.text:
                        smoking_allowed = "Allowed"
                    if "Smoking within the premises is not allowed" in property_rules.text:
                        smoke_allowed = "NO"
                    if "Unmarried couples allowed" in property_rules.text:
                        couple_friendly = "Allowed"   
                        
                except:
                    pass

                try:
                    driver.find_element(By.CSS_SELECTOR, "span[class=\"cm__modalClose \"]").click()
                except:
                    pass
                
            
                driver.close()
                driver.switch_to.window(window_handles[0])

                quickstart.main()
                columnCount = quickstart.getColumnCount()
            
                results = []
                results.append(str(columnCount + 1))
                results.append(hotel_id)
                results.append(hotel_name)
                results.append(city_name)
                results.append(location)
                results.append(lat)
                results.append(lng)
                results.append(star_category)
                results.append(price)
                results.append(mmt_value)
                results.append(number_of_rooms)
                results.append(description)
                results.append(couple_friendly)
                results.append(pet_friendly)
                results.append(cctv)
                results.append(security_guard)
                results.append(fire_extinguishers)
                results.append(first_aid_services)
                results.append(wake_up_call)
                results.append(luggage_assistance)
                results.append(reception)
                results.append(banquet)
                results.append(conference_room)
                results.append(spa)
                results.append(restaurant)
                results.append(indoor_games)
                results.append(_25_hour_roo_service)
                results.append(wheelchair)
                results.append(lounge)
                results.append(bar)
                results.append(cafe)
                results.append(steam_and_sauna)
                results.append(salon)
                results.append(yoga)
                results.append(kids_play_area)
                results.append(library)
                results.append(dry_cleaning_service)
                results.append(laundry_service)
                results.append(housekeeping)
                results.append(power_backup)
                results.append(elevator_lift)
                results.append(intercom)
                results.append(wi_fi)
                results.append(newspaper)
                results.append(parking)
                results.append(airport_transfer_available)
                results.append(vehicle_rentals)
                results.append(medical_services)
                results.append(atm)
                results.append(currency_excahnge)
                results.append(bonfire)
                results.append(check_in_time)
                results.append(check_out_time)
                results.append(outside_food_allowed)
                results.append(smoking_allowed)
                results.append(number_of_property_photos)
                results.append(room_photos)
                results.append(outdors_photos)
                results.append(reception_photos)
                results.append(entrance_photos)
                results.append(washroom_photos)
                results.append(interior_photos)
                results.append(restaurant_photos)
                results.append(swimmingpool_photos)
                results.append(food_and_dining)
                results.append(location_and_surroundings)
                results.append(property_highlights)
                results.append(room_details_and_amenities)
                results.append(all_amenities)
                results.append(all_property_rules_result)

                for room in all_room_data:
                    results.append(room['room_name'])
                    results.append(room['room_size'])
                    results.append(room['free_cancelation'])
                    results.append(room['view_type'])
                    results.append(room['bed_type'])
                    results.append(room['number_of_people'])
                    results.append(room['work_desk'])
                    results.append(room['room_only'])
                    results.append(room['breakfast'])
                    results.append(room['lunch_include'])
                    results.append(room['dinner_include'])
                    results.append(room['lunch_dinner_include'])
                    results.append(room['mini_refrigerator'])
                    results.append(room['smoke_detector'])
                    results.append(room['smoke_allowed'])
                    results.append(room['air_conditioning'])
                    results.append(room['in_room_safe'])
                    results.append(room['tv'])
                    results.append(room['balcony_terrace'])
                    results.append(room['air_purifier'])
                    results.append(room['minearal_water'])
                    results.append(room['iron_board'])
                    results.append(room['toiletries'])
                    results.append(room['hair_dryer'])
                    results.append(room['dental_kit'])
                    results.append(room['towel'])
                    results.append(room['ceiling_fun'])
                    results.append(room['room_amenities'])

                if len(results) < 406:
                    # Calculate the number of empty strings needed
                    num_empty_strings = 406 - len(results)

                    # Append empty strings to the results array
                    results += [""] * num_empty_strings

                quickstart.main()
                columnCount = quickstart.getColumnCount()
                RANGE_DATA = f'makemytrip1!A{columnCount + 2}:OP'
                quickstart.insert_data(RANGE_DATA, results)
                hotel_count = hotel_count + 1
                print(f'Total Hotel Count = ', len(hotel_list))
                                        
                sleep(2)
            except:
                pass
            
        driver.quit()
        sleep(5)
    
    except:
        pass
        
        
    
