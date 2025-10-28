import json
import requests
import time

course_id = "U2VhcmNoQ291cnNlOmRlbHRhY29sbGVnZTpNakkyTXpwTlFWUklPakU9"

payload = {
    "courseStatus": "OpenAndFull"
}

# figure out how to get headers for any browser/os
headers = {
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://deltacollege.search.collegescheduler.com',
    'priority': 'u=1, i',
    'referer': 'https://deltacollege.search.collegescheduler.com/',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"', # likely vary from user to user
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36', # likely vary from user to user
}

# find appropriate count value
json_data = {
    'query': 'query CourseDetailsQuery_Query(\n  $environment: String!\n  $courseId: ID!\n  $count: Int\n  $cursor: String\n  $facets: [SearchFacetCriteria]\n  $includeFullCourses: Boolean\n  $registrationNumber: String\n  $freeTextbook: Boolean\n  $lowCostTextbook: Boolean\n  $instructor: String\n) {\n  environment(name: $environment) {\n    ...CourseDetailsContainer_environment_1G22uz\n    id\n  }\n}\n\nfragment CourseDetailsContainer_environment_1G22uz on Environment {\n  publicSettings {\n    sectionFieldTextSettings {\n      credits\n    }\n    id\n  }\n  ...SectionTableContainer_environment_1G22uz\n}\n\nfragment SectionTableContainer_environment_1G22uz on Environment {\n  publicSettings {\n    styleSettings {\n      primaryColor\n      freeTextbookFlagColor\n      lowCostTextbookFlagColor\n    }\n    courseSearchSettings {\n      sectionFields\n      dropDownOptionsLimit\n    }\n    filterSettings {\n      campusSelectionPrefixes\n    }\n    courseSettings {\n      flags {\n        key\n        text\n        sectionText\n        sectionTooltip\n        showOnSection\n      }\n    }\n    sectionFieldTextSettings {\n      campus\n      component\n      credits\n      dates\n      days\n      freeTextbookIndicated\n      lowCostTextbookIndicated\n      instructionMode\n      careers\n      partsOfTerm\n      instructorPlural\n      location\n      openSeats\n      registrationNumber\n      rooms\n      times\n    }\n    sectionSettings {\n      locationFormat\n    }\n    textSettings {\n      academicCareerPlural\n      mondayAbbr\n      tuesdayAbbr\n      wednesdayAbbr\n      thursdayAbbr\n      fridayAbbr\n      saturdayAbbr\n      sundayAbbr\n    }\n    id\n  }\n  getCourseSections(courseId: $courseId, first: $count, after: $cursor, facets: $facets, includeFullSections: $includeFullCourses, registrationNumber: $registrationNumber, freeTextbook: $freeTextbook, lowCostTextbook: $lowCostTextbook, instructor: $instructor) {\n    totalSections\n    pageInfo {\n      hasNextPage\n      endCursor\n    }\n    edges {\n      cursor\n      node {\n        id\n        registrationNumber\n        instructors\n        instructionMode\n        careers\n        openSeats\n        totalSeats\n        campus\n        location\n        component\n        freeTextbookAvailable\n        lowCostTextbookAvailable\n        meetings {\n          room\n          building\n          buildingCode\n          buildingDescription\n          days\n          startDate\n          endDate\n          startTime\n          endTime\n        }\n        __typename\n      }\n    }\n    ...SectionFacetsContainer_getCourseSections\n  }\n  ...FacetsSettingsContainer_environment\n}\n\nfragment SectionFacetsContainer_getCourseSections on SearchSectionConnection {\n  facetFieldResults {\n    facetField\n    facetFieldValueResults {\n      value\n      selected\n      sectionCount\n    }\n  }\n}\n\nfragment FacetsSettingsContainer_environment on Environment {\n  publicSettings {\n    textSettings {\n      campus\n      campusPlural\n      courseStatus\n      academicCareerPlural\n      freeTextbook\n      freeTextbookInstructions\n      partsOfTermPlural\n      sessionPlural\n      instructionModePlural\n      instructor\n      locationPlural\n    }\n    sectionFieldTextSettings {\n      registrationNumber\n    }\n    courseSearchSettings {\n      courseSearchFilters\n      dropDownOptionsLimit\n    }\n    filterSettings {\n      campusSelectionPrefixes\n    }\n    id\n  }\n}\n',
    'variables': {
        'environment': 'deltacollege',
        'courseId': course_id,
        'count': 99,
        'cursor': None,
        'facets': [],
        'includeFullCourses': True,
        'registrationNumber': None,
        'freeTextbook': None,
        'lowCostTextbook': None,
        'instructor': '',
    },
}

class Section:
    def __init__(self, json_text):
        self.section_number = json_text["registrationNumber"]
        self.instructors = json_text["instructors"]
        self.open_seats = json_text["openSeats"]
        self.total_seats = json_text["totalSeats"]

response = requests.post('https://api.collegescheduler.com/graphql', headers=headers, json=json_data)

for node in map(lambda x: x["node"], response.json()["data"]["environment"]["getCourseSections"]["edges"]):
    section = Section(node)
    if section.open_seats != 0:
        print(f"Section {section.section_number} taught by Professor {section.instructors[0]} has {section.open_seats} seats left.")