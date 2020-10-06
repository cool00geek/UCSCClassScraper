# UCSC Class scraper

A tool designed to scrape the [UCSC class search page](https://pisa.ucsc.edu/class_search/) and store the info as a JSON. This can be helpful to archive class schedules, search by ways not allowed on the standard site and more.

This was initially designed by me to have a way to search for in person/hybrid classes, if the school decided to offer such classes, during the COVID-19 pandemic.

## Requirements

- Beautifulsoup4
- requests

I'll get around to creating a `requirements.json` eventually....

## Usage

Run the main script, `ucsc_scrape.py`, with the argument being the filename you would like to save the class dump to.

Example: `python3 ucsc_scrape.py fall2020.json`

## Scripts

The `ucsc_scrape.py` file itself does not provide any analysis on the classes offered. In order to do that, you will need a different script that can parse the class JSON and give you relevant information. I will be adding any scripts I use to the `scripts/` directory in this repository. Look at the README there for more information.

If you ever write a script using the JSON, submit a PR to get the script added in!

## Class files

I plan on storing class listings in the `classes/` directory as long as I use them. This will reduce load on the UCSC servers since the scraper will make ~1500 requests to scrape all the information.

All the files will be follow the naming convention: `[year][quarter]-YYYY-mm-dd.json`

Where `year` and `quarter` will be the quarter in the specified year.

`YYYY-mm-dd` will be the date the snapshot was taken.

If you want to look at the data in the files for some reason, the JSON format is listed below.

Alternatively, [This website](http://jsonviewer.stack.hu/) has done a great job of allowing me to look through the JSON.

## JSON Format

```json
{
    classname: {
        "url": "url here",
        "number": "class number here as int",
        "units": "Units here as int",
        "ge": "GE here",
        "capacity": "class capacity as int",
        "enrolled": "enrolled number as int",
        "waitlist": "number on waitlist as int",
        "meeting":{
            "day": "Days, such as TuTh",
            "time": "Time here as str",
            "room": "Room here as string",
            "instructor": "Professor goes here",
        },
        "discussions": [
            {
                "number": "discussion_number as int",
                "day": "Days here, such as TuTh",
                "time": "Time here as str",
                "room": "Room here as string",
                "instructor": "Professor here",
                "enrolled": "Number enrolled as int",
                "capacity": "Capacity as int",
                "waitlist": "number on waitlist as int"
            },
            ...
        ]
    },
    ...
}
```

## Known Bugs

- It doesn't work quite well with combined classes, such as CSE 185S and CSE185E. However, you can use the `combined.py` script to find these classes
