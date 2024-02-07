import unittest
from unittest.mock import patch
from dinamik_link import process_input, construct_url  # Replace 'your_script_name' with the actual name of your script
from urllib.parse import urlparse, parse_qs

def parse_url_query(url):
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query)

class TestScriptFunctions(unittest.TestCase):

    def setUp(self):
        self.data = {
                        "Daytime": {
                            "9-12": "late-morning",
                            "12-15": "afternoon",
                            "15-18": "late-afternoon",
                            "18-21": "evening",
                            "21-24": "ate-evening",
                            "0-3": "night",
                            "3-6": "late-night",
                            "6-9": "morning"
                        },
                        "Days": {
                            "Sun": "sun",
                            "Mon": "mon",
                            "Tre": "tre",
                            "Wed": "wed",
                            "Thu": "thu",
                            "Fri": "fri",
                            "Sat": "sat"
                        },
                        "Specialties": {
                            "Business English": "bus_gen%2Cconv_job%2Cen_prof%2Cjob_interview",
                            "IELTS": "testprep_ielts",
                            "Conversational English": "conv_gen",
                            "American English": "american_eng",
                            "English for kids": "en_gchi%2Ckids_jschool%2Ckids_newborn",
                            "Intensive English": "en_int",
                            "English for beginners": "english_zero",
                            "English for traveling": "conv_travel",
                            "For studying abroad": "english_study",
                            "English literature": "eng_lit"
                        },
                        # "Region accent": {
                        #     "British english": "british_eng",
                        #     "Canadian english": "canadian_eng",
                        #     "Australian english": "australian_eng"
                        # },
                        # "Test preparation": {
                        #     "TOEFL": "toefl",
                        #     "CAE": "cae",
                        #     "FCE": "en_fce",
                        #     "ESOL": "esol",
                        #     "ACT English": "english_act",
                        #     "SAT Writing": "writing_sat",
                        #     "AP English": "ap-english",
                        #     "GMAT": "gmat",
                        #     "Ap english language & composition": "ap-english-language-composition",
                        #     "TOEIC": "toeic",
                        #     "BEC": "testprep_bec",
                        #     "OET": "oet",
                        #     "PTE": "pte",
                        #     "CAEL": "cael",
                        #     "ICAS English": "english_icas"
                        # },
                        # "Learning disabilities": {
                        #     "English for ADHD students": "english-for-adhd-students",
                        #     "English for dyslexic students": "english-for-dyslexia-students",
                        #     "English for students with Asperge's syndrome": "english-for-aspergers-students"
                        # },
                        "Also speaks": {
                            "Albanian": "sq",
                            "Arabic": "ar",
                            "Armenia": "hy",
                            "Azerbaijani": "az",
                            "Basque": "eu",
                            "Bengali": "bn",
                            "Bulgarion": "bg",
                            "Catalan": "ca",
                            "Cebuano": "ceb",
                            "Chinese(Cantonese)": "yue",
                            "Chinese(Mandarin": "zh",
                            "Crimean Tatar": "crh",
                            "Croatian": "hr",
                            "Crech": "cs",
                            "Danish": "da",
                            "Dutch": "nl",
                            "English": "en",
                            "Estonian": "et",
                            "Farsi": "fa",
                            "Finnish": "fi",
                            "French": "fr",
                            "Galican": "gl",
                            "Georgian": "ka",
                            "German": "de",
                            "Greek": "el",
                            "Gujarati": "gu",
                            "Hebrew": "he",
                            "Hindi": "hi",
                            "Hungarian": "hu",
                            "Icelandic": "is",
                            "Indonesian": "id",
                            "Irish": "ga",
                            "Italian": "it",
                            "Japanese": "ja",
                            "Javanse": "jv",
                            "Kannada": "kn",
                            "Kazakh": "kk",
                            "Korean": "ko",
                            "Latin": "la"
                        },
                        "Only English native speakers": {
                            "YES": "native",
                            "NO": ""
                        },
                        "Only super tutors": {
                            "YES": "only_super_tutors",
                            "NO": ""
                        },
                        "Only professional tutors": {
                            "YES": "certified",
                            "NO": ""
                        },
                        "Sort by": {
                            "Popularity": "popularity",
                            "Price:highest first": "price_highest",
                            "Price:lowest first": "price_lowest",
                            "Number of reviews": "reviews",
                            "Best rating": "rating"
                        },
                        "Country": {
                        "Canada": "CA",
                        "USA": "US",
                        "United Kingdom": "GB",
                        "Australia": "AU"
                        },
                    }
        self.category_to_param = {
            "Also speaks": "tl",
            "Daytime": "time",
            "Sort by": "sort",
            "Specialties": "tags",
            "Region accent": "tags",  # Assuming this should be part of 'tags'
            "Test preparation": "tags",  # Assuming this should be part of 'tags'
            "Learning disabilities": "tags",  # Assuming this should be part of 'tags'
            "Only professional tutors": "additional",
            "Only English native speakers": "additional",
            "Only super tutors": "additional",
            "Days": "day",
            "Country": "CoB"
        }


        self.base_url = "https://preply.com/en/online/english-tutors"

    def test_process_input(self):
        user_input = "Canada, USA"
        options = self.data["Country"]
        expected_result = "CA%2CUS"
        self.assertEqual(process_input(user_input, options), expected_result)

    def test_construct_url(self):
        # user_inputs = {
        #     "Daytime": "9-12",  # Assuming the user selects "9-12"
        #     "Days": "Sun",  # Assuming the user selects "Sun"
        #     "Specialties": "Business English,For studying abroad",  # Assuming the user selects these options
        #     "Also speaks": "English",  # Assuming the user selects "English"
        #     "Only English native speakers": "YES",  # Assuming the user selects "YES"
        #     "Only super tutors": "YES",  # Assuming the user selects "YES"
        #     "Only professional tutors": "YES",  # Assuming the user selects "YES"
        #     "Sort by": "Price:highest first",
        #     "Country": "Canada"# Assuming the user selects "Price:highest first"
        # }
        user_inputs = {
            "Days": "Sun",  # Assuming the user selects "Sun"
            "Specialties": "Business English,For studying abroad",  # Assuming the user selects these options
            "Also speaks": "English",  # Assuming the user selects "English"
            "Country": "Turkey"# Assuming the user selects "Price:highest first"
        }


        constructed_url = construct_url(self.base_url, self.category_to_param, self.data, user_inputs)
        print(f"Constructed URL: {constructed_url}")  # Print the constructed URL for inspection

        expected_url = "https://preply.com/en/online/english-tutors?tl=en&time=late-morning&sort=price_highest&tags=bus_gen%2Cconv_job%2Cen_prof%2Cjob_interview%2Cenglish_study&additional=additional%3Dnative%2Cadditional%3Dcertified%2Cadditional%3Donly_super_tutors%2Ccertified%2Cnative%2Conly_super_tutors&day=sun&CoB=CA"
        constructed_query = parse_url_query(constructed_url)
        expected_query = parse_url_query(expected_url)


        self.assertEqual(constructed_query, expected_query)

if __name__ == '__main__':
    unittest.main()
