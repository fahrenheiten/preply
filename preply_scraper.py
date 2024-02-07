import json

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
from googletrans import Translator, LANGUAGES
from urllib.parse import urlparse, parse_qs
from dinamik_link import construct_url,collect_inputs,process_input

def translate_text(text, dest_language='en'):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=dest_language)
        return translated.text
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return text  # В случае ошибки возвращаем исходный текст
def get_tutor_details(tutor_url, session):

    response = session.get(tutor_url)
    tutor_soup = BeautifulSoup(response.content, 'lxml')
    language_elements = tutor_soup.find_all('div',class_='khPkeq _2B2g-a _8nxFNH')
    filtered_details = []
    for element in language_elements:
        text = element.get_text(strip=True)
        if "TeachesEnglish lessons" not in text and "lessons taught" not in text:
            filtered_details.append(text)

    details_str = ', '.join(filtered_details)  # Преобразуем отфильтрованный список в строку

    return {
        'additional_detail': details_str
    }

def get_free_tutor(dynamic_url):
    cookies = {
        'uid': '90a253a8c56e8daab57a44321bfdf8f59508e268a5d3ff2cd318741087368bb7',
        'init_uid': '90a253a8c56e8daab57a44321bfdf8f59508e268a5d3ff2cd318741087368bb7',
        'currency_code': 'TRY',
        'SL_G_WPT_TO': 'ru',
        'SL_GWPT_Show_Hide_tmp': '1',
        'SL_wptGlobTipTmp': '1',
        'm_source': 'other',
        'm_source_landing': '/',
        'm_source_details': '',
        'is_source_set': 'yes',
        'source_page': '',
        'landing_page': 'https://preply.com/',
        'visit_time': '2023-12-21T09:02:18.446Z',
        'browserTimezone': 'Europe/Moscow',
        'csrftoken': 'hwFmueh8cfXKxe8TURctCKPYJ4uJNQnbe6ZQGJwYlrGtAYwCaem7vdejNvix7JYo',
        'sessionid': '0rqmu1ep8998iol8m0ph5umyhur6ncpj',
        '_gcl_au': '1.1.337694969.1703149354',
        'hj_first_visit_30days': '2023-12-21T09:02:34.530Z',
        'visitorsRetargetingExperiment': 'included',
        '__pdst': 'fdfc3ebfe1c14bd6b5d84afd7f46e4ff',
        '_tt_enable_cookie': '1',
        '_ttp': 'VCow8IvmCloF7bpopTzydZcUPSm',
        '_hjHasCachedUserAttributes': 'true',
        '_zitok': 'd78c3fea869b14e85e2b1703149355',
        '_hjSessionUser_641144': 'eyJpZCI6IjY2M2M3ZDhlLTM0MzUtNTY5MS04ZGEwLTU5ZjViOTZjMDQ0NiIsImNyZWF0ZWQiOjE3MDMxNDkzNTU2MDcsImV4aXN0aW5nIjp0cnVlfQ==',
        'pre_search_reason_answer': 'career',
        'student_goal_id': '7040600',
        'hubspotutk': 'efdff0cd3c2ee18a4295a34b9feb0968',
        '__hssrc': '1',
        '_tq_id.TV-8172186318-1.89eb': '704e6661b8323823.1703149356.0.1703754083..',
        'cookieyes-consent': 'consentid:czdESkZDNUZrNkl2S0dPeUtJMnRjNGFjMGVaU2VjSmc,consent:yes,action:no,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes,other:yes',
        'pre_search_used_subjects_str': 'en-es-de',
        '_gid': 'GA1.2.1811085026.1707112842',
        'prev_filter_for_subject_angliyskogo': 'time=late-morning&day=sun&CoB=CA',
        'source_page_last': '',
        'lastSearchSubj': 'english',
        'language_code': 'en',
        '_clck': 'cyqw6t%7C2%7Cfj1%7C0%7C1450',
        '_hjSession_641144': 'eyJpZCI6ImJjYTkzNjEyLWM3NzAtNGZjOC1hNDRhLTgxODI2OGY1NmU1NSIsImMiOjE3MDcyMDUzODA0MDIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        'recent-tutor-ids': '775082|2564131|3290728|626996|3475888|548739|326310|3614053|289156|127980',
        'AMP_TOKEN': '%24NOT_FOUND',
        '__hstc': '115815577.efdff0cd3c2ee18a4295a34b9feb0968.1703754069439.1707121919333.1707211139270.15',
        'pv_count': '129',
        '_rdt_uuid': '1703149354986.087b648d-6cdb-4a7f-8fd2-d7260d04f046',
        '_uetsid': 'dac2b980c3eb11eeb0ac71d6fe2ea171',
        '_uetvid': 'ae7d85609fdf11eeb8d4c3756bc03cab',
        '__hssc': '115815577.2.1707211139270',
        '_ga': 'GA1.2.241070452.1703149355',
        'prev_filter_for_subject_english': 'CoB=TR',
        '_clsk': 'hebjl4%7C1707211413589%7C105%7C0%7Cv.clarity.ms%2Fcollect',
        '_ga_BQH4D3BLSB': 'GS1.1.1707207561.40.1.1707211752.60.0.0',
        'landing_page_last': 'https://preply.com/en/online/english-tutors?',
        'visit_time_last': '2024-02-06T09:29:13.019Z',
        'lastSearchUrl': 'https://preply.com/en/online/english-tutors',
        '__cf_bm': '5AUMW4TUfdRI0gaw2OsfiDaXbZZw1DhtuEkrcpn67hk-1707211756-1-ARfJY9qzA5ojYl5L1Naao3Em29lrWuvTVAJ4RWC7wc6zTcG7coYCMuJOfLkWI2Pv34CPwVt/uq2Od/kiQjNIDdM=',
        '_cfuvid': 'RdBbUO07PrRlVKMrwLxwugxlEGDtiPMaGsZkiLO8BX8-1707211756989-0-604800000',
        '_dd_s': 'rum=0&expire=1707212656564',
    }

    headers = {
        'authority': 'preply.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': 'uid=90a253a8c56e8daab57a44321bfdf8f59508e268a5d3ff2cd318741087368bb7; init_uid=90a253a8c56e8daab57a44321bfdf8f59508e268a5d3ff2cd318741087368bb7; currency_code=TRY; SL_G_WPT_TO=ru; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; m_source=other; m_source_landing=/; m_source_details=; is_source_set=yes; source_page=; landing_page=https://preply.com/; visit_time=2023-12-21T09:02:18.446Z; browserTimezone=Europe/Moscow; csrftoken=hwFmueh8cfXKxe8TURctCKPYJ4uJNQnbe6ZQGJwYlrGtAYwCaem7vdejNvix7JYo; sessionid=0rqmu1ep8998iol8m0ph5umyhur6ncpj; _gcl_au=1.1.337694969.1703149354; hj_first_visit_30days=2023-12-21T09:02:34.530Z; visitorsRetargetingExperiment=included; __pdst=fdfc3ebfe1c14bd6b5d84afd7f46e4ff; _tt_enable_cookie=1; _ttp=VCow8IvmCloF7bpopTzydZcUPSm; _hjHasCachedUserAttributes=true; _zitok=d78c3fea869b14e85e2b1703149355; _hjSessionUser_641144=eyJpZCI6IjY2M2M3ZDhlLTM0MzUtNTY5MS04ZGEwLTU5ZjViOTZjMDQ0NiIsImNyZWF0ZWQiOjE3MDMxNDkzNTU2MDcsImV4aXN0aW5nIjp0cnVlfQ==; pre_search_reason_answer=career; student_goal_id=7040600; hubspotutk=efdff0cd3c2ee18a4295a34b9feb0968; __hssrc=1; _tq_id.TV-8172186318-1.89eb=704e6661b8323823.1703149356.0.1703754083..; cookieyes-consent=consentid:czdESkZDNUZrNkl2S0dPeUtJMnRjNGFjMGVaU2VjSmc,consent:yes,action:no,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes,other:yes; pre_search_used_subjects_str=en-es-de; _gid=GA1.2.1811085026.1707112842; prev_filter_for_subject_angliyskogo=time=late-morning&day=sun&CoB=CA; source_page_last=; lastSearchSubj=english; language_code=en; _clck=cyqw6t%7C2%7Cfj1%7C0%7C1450; _hjSession_641144=eyJpZCI6ImJjYTkzNjEyLWM3NzAtNGZjOC1hNDRhLTgxODI2OGY1NmU1NSIsImMiOjE3MDcyMDUzODA0MDIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; recent-tutor-ids=775082|2564131|3290728|626996|3475888|548739|326310|3614053|289156|127980; AMP_TOKEN=%24NOT_FOUND; __hstc=115815577.efdff0cd3c2ee18a4295a34b9feb0968.1703754069439.1707121919333.1707211139270.15; pv_count=129; _rdt_uuid=1703149354986.087b648d-6cdb-4a7f-8fd2-d7260d04f046; _uetsid=dac2b980c3eb11eeb0ac71d6fe2ea171; _uetvid=ae7d85609fdf11eeb8d4c3756bc03cab; __hssc=115815577.2.1707211139270; _ga=GA1.2.241070452.1703149355; prev_filter_for_subject_english=CoB=TR; _clsk=hebjl4%7C1707211413589%7C105%7C0%7Cv.clarity.ms%2Fcollect; _ga_BQH4D3BLSB=GS1.1.1707207561.40.1.1707211752.60.0.0; landing_page_last=https://preply.com/en/online/english-tutors?; visit_time_last=2024-02-06T09:29:13.019Z; lastSearchUrl=https://preply.com/en/online/english-tutors; __cf_bm=5AUMW4TUfdRI0gaw2OsfiDaXbZZw1DhtuEkrcpn67hk-1707211756-1-ARfJY9qzA5ojYl5L1Naao3Em29lrWuvTVAJ4RWC7wc6zTcG7coYCMuJOfLkWI2Pv34CPwVt/uq2Od/kiQjNIDdM=; _cfuvid=RdBbUO07PrRlVKMrwLxwugxlEGDtiPMaGsZkiLO8BX8-1707211756989-0-604800000; _dd_s=rum=0&expire=1707212656564',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    }

    def url_to_params(url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Преобразование значений из списка в строку
        params = {k: ','.join(v) for k, v in query_params.items()}
        return params

    url = dynamic_url
    params = url_to_params(url)

    session = requests.Session()
    base_url = 'https://preply.com/en/online/english-tutors'
    page = 1
    tutors_data = []

    while True:
        url = f"{base_url}?page={page}"
        response = session.get(url,params=params,cookies=cookies,headers=headers )
        soup = BeautifulSoup(response.content, 'lxml')

        tutors = soup.find_all('div', class_="styles_GridCellHeading__gLDJt")
        price_elements = soup.find_all('h4', class_="preply-ds-heading _3DJ88_ R-na51 Bc4V1o _2523Lq")
        links = soup.find_all('a', class_="styles_FullName__abIcx")
        photos = soup.find_all('div', class_='styles_GridCellAvatar__mEer2')

        if len(tutors) == len(price_elements) == len(links):
            for tutor, element, link, photos in zip(tutors, price_elements, links, photos):

                # Extract and process tutor text
                tutor_text = tutor.get_text('h4').replace('h4', '').replace('Супер-репетитор', '').strip()

                # Extract and process price text
                price_text = element.get_text().strip()
                price_number = price_text.replace("\xa0", "").replace(' ', '').replace(',', '')  # Assuming format like '1 154
                number = int(price_number)

                # Extract link href
                href_value = link.get('href')


                # Check if href_value contains the full URL or just a path
                if href_value.startswith('http'):
                    tutor_url = href_value
                else:
                    tutor_url = f"https://preply.com{href_value}"


                tutor_additional_info = get_tutor_details(tutor_url, session)

                # Extract image URL from the photo element
                img_tag = photos.find('img')
                if img_tag and img_tag.has_attr('src'):
                    img_url = img_tag['src']
                else:
                    img_url = 'No image found'

                student_count = 0
                lesson_count = 0

                # Finding student info
                student_info_element = tutor.find_next('p', class_='khPkeq _1jP5ux _8nxFNH',
                                                       string=re.compile('active students'))
                if student_info_element:
                    student_text = student_info_element.get_text().replace(u'\xa0', '').replace(' ', '').replace(',','')
                    student_count = int(re.search(r'\d+', student_text).group())

                # Finding lesson info
                lesson_info_element = tutor.find_next('p', class_='khPkeq _1jP5ux _8nxFNH', string=re.compile('lesson'))
                if lesson_info_element:
                    # Remove non-breaking spaces and any thousand separators before converting to int
                    lesson_text = lesson_info_element.get_text().replace(u'\xa0', '').replace(' ', '').replace(',', '')
                    lesson_count = int(re.search(r'\d+', lesson_text).group())

                tutor_info = {
                        'Tutor Name': tutor_text,
                        'Price': number,
                        'Link': tutor_url,
                        'Image Url': img_url,
                        'Count active student ': student_count,
                        'Count lesson': lesson_count,
                        **tutor_additional_info
                }
                tutors_data.append(tutor_info)
        else:
            print(f"Mismatch in lengths of tutors, prices, and links on page {page}. Skipping this page.")

        next_page_link = soup.find('a', {'aria-label': f'page-{page + 1}'})
        if next_page_link:
            page += 1  # Move to the next page
        else:
            break  # No more pages, exit the loop

        # Save to CSV only if there is data
    if tutors_data:
        keys = tutors_data[0].keys()
        with open('tutors_data.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(tutors_data)
    else:
        print("No data to save to CSV.")

    if tutors_data:
        df = pd.DataFrame(tutors_data)

        # Save to Excel file
        with pd.ExcelWriter('tutors_data.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

            # Apply filter
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            worksheet.auto_filter.ref = worksheet.dimensions

    else:
        print("No data to save.")


def main():
    with open('data.json','r',encoding='utf-8') as file:
        data = json.load(file)

    category_to_param = {

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
    user_inputs = collect_inputs(data)
    dynamic_url = construct_url("https://preply.com/en/online/english-tutors", category_to_param, data, user_inputs)
    print("Constructed URL:", dynamic_url)
    get_free_tutor(dynamic_url)


if __name__ == '__main__':
    main()

