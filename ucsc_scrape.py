#/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import sys
import json

PAGE_SIZE=100

def get_dict():
    classes = dict()
    """
    {
        classname: {
            "url": "url goes here",
            "number": class number here"
            "units": Units goes here,
            "GE": "GE goes here",
            "capacity": cap,
            "enrolled": enrolled number,
            "waitlist": number on waitlist,
            "meeting":{
                "day": "Days here",
                "time": "Time here as str",
                "room": "Room here as stringz',
                "instructor": "Professor goes here",
            },
            "discussions": [
                {
                    "number": discussion_number: 
                    "day": "Days here",
                    "time": "Time here as str",
                    "room": "Room here as string,
                    "instructor": "Professor goes here",
                    "enrolled": "Number enrolled",
                    "capacity": "cap",
                    "waitlist": number on waitlist
                },
                ...
            ]
        },
        ...
    }
    """
    start_num = 0
    while start_num != -1:
        if start_num == 0:
            data = {
                'binds[:term]': '2210',
                'binds[:reg_status]': 'all',
                'action': 'results',
                'rec_start': '0',
                'rec_dur': '{}'.format(PAGE_SIZE)
            }
        else:
            data = {
                'binds[:term]': '2210',
                'binds[:reg_status]': 'all',
                'action': 'next',
                'rec_start': '{}'.format(start_num-PAGE_SIZE),
                'rec_dur': '{}'.format(PAGE_SIZE)
            }
        

        response = requests.post('https://pisa.ucsc.edu/class_search/index.php', data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        for i in range(0, PAGE_SIZE):
        #for i in range(0, 1):
            element = soup.find(id="rowpanel_{}".format(i))

            if element is None:
                start_num = -1
                break
            elif i == (PAGE_SIZE-1):
                start_num += PAGE_SIZE
            class_name = element.find("a").text.replace(u'\xa0', u' ')
            print(class_name)
            class_url = 'https://pisa.ucsc.edu/class_search/' + element.find("a").get('href')

            class_info = requests.get(class_url)
            class_soup = BeautifulSoup(class_info.text, 'html.parser')
            class_info_section = class_soup.find_all("dd")

            class_number = class_info_section[2].text
            class_units = int(class_info_section[4].text[:1])
            class_ge = class_info_section[5].text.replace(u'\xa0', u' ')
            class_capacity = int(class_info_section[8].text)
            class_enrolled = int(class_info_section[9].text)
            class_waitlist_enrolled = int(class_info_section[11].text)

            class_meeting_section = class_soup.find_all("div", {"class": "panel-body"})[-2]
            class_meeting_info = class_soup.find_all("td")

            if len(class_meeting_info) == 0 or class_meeting_info[0].text.strip() == "Class":
                class_day = "Combined"
                class_time = "Combined"
                class_room = "Combined"
                class_instructor = "Combined"
            else:
                if class_meeting_info[0].text.strip() == "Cancelled":
                    class_day = "Cancelled"
                    class_time = "Cancelled"
                else:
                    class_day = class_meeting_info[0].text.split(" ")[0]
                    class_time = class_meeting_info[0].text.split(" ")[1]
                class_room = class_meeting_info[1].text
                class_instructor = class_meeting_info[2].text
            meeting_dict = {
                "day":class_day,
                "time":class_time,
                "room":class_room,
                "instructor": class_instructor
            }

            discussion_arr = []

            class_discussion_sections = class_soup.find_all("div", {"class": "panel-body"})
            if len(class_discussion_sections) >= 6:
                class_discussions = class_discussion_sections[-1].find_all("div", {"class":"row row-striped"})
                for discussion in class_discussions:
                    curr_discussion_soup = discussion.find_all("div", {"class": "col-xs-6 col-sm-3"})
                    disc_num = int(curr_discussion_soup[0].text.split(" ")[0][1:])
                    disc_day = curr_discussion_soup[1].text.split(" ")[0]
                    disc_time = curr_discussion_soup[1].text.split(" ")[1]
                    disc_location = curr_discussion_soup[3].text[5:].strip()
                    disc_instructor = curr_discussion_soup[2].text.strip()
                    disc_enrolled = int(curr_discussion_soup[4].text.split(" ")[1])
                    disc_capacity = int(curr_discussion_soup[4].text.split(" ")[3])
                    disc_waitlist = int(curr_discussion_soup[5].text.split(" ")[1])
                    curr_discussion_info = {
                        "number": disc_num,
                        "day": disc_day,
                        "time": disc_time, 
                        "room": disc_location, 
                        "instructor": disc_instructor, 
                        "enrolled": disc_enrolled, 
                        "capacity": disc_capacity, 
                        "waitlist": disc_waitlist, 
                    }
                    discussion_arr.append(curr_discussion_info)
            classes[class_name] = {
                "url": class_url,
                "number": class_number,
                "units": class_units,
                "ge": class_ge,
                "capacity": class_capacity,
                "enrolled": class_enrolled,
                "waitlist": class_waitlist_enrolled,
                "meeting": meeting_dict,
                "discussions": discussion_arr,
            }
    
    return classes

def main():
    if len(sys.argv) < 2:
        print("Please specify the filename!", file=sys.stderr)
        exit(1)
    classes = get_dict()
    js = json.dumps(classes)
    f = open(sys.argv[1], "w")
    f.write(js)
    f.close()

if __name__ == '__main__':
    main()
