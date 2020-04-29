#################
########   Final Project
#Name: Yanbo Shi
#Uniqname: yanboshi
#################

from bs4 import BeautifulSoup
import requests
import json
import sqlite3
import re



def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.collegesimply.com/colleges/"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
    '''
    state_dict = {}
    url = 'https://www.collegesimply.com/colleges/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lis = soup.find('select', class_='custom-select')
    state_list = lis.find_all('option')

    for infor in state_list:
        state_dict[infor.text.lower()] = url + infor['value']
    
    return state_dict


def get_university_sites_url_and_html_and_cashing():
    url = 'https://www.collegesimply.com/'
    state_sites_dict = build_state_url_dict()
    university_url_dict = {}
    for state_site in state_sites_dict.values():
        response = requests.get(state_site)
        soup = BeautifulSoup(response.text, 'html.parser')
        lis = soup.find('ol', class_='list-unstyled')
        univer_list = lis.find_all('h4')

        for univ in univer_list:
            univer_url = url + univ.find('a')['href']
            # make_request_using_cache(univer_url,CACHE_DICT)
            univer_name = univ.text
            university_url_dict[univer_name.strip()] = univer_url

    return university_url_dict

def get_data_from_each_university_web(university_web_url):
    data_collection = []
    url_text = make_request_using_cache(university_web_url,CACHE_DICT)
    # response = requests.get(university_web_url)
    soup = BeautifulSoup(url_text, 'html.parser')
    lis = soup.find_all('div', class_='card')

    #name
    try:
        name = soup.find('div',class_='col ml-n3 ml-md-n2').find('h1').text.strip()
        data_collection.append(name)
    except:
        data_collection.append('Missing Name')

    #state
    try:
        state_address = soup.find('span',class_='header-pretitle mb-1 h6').text
        state = state_address.strip().split(',')[1].strip()
        data_collection.append(state)
    except:
        data_collection.append('Missing State')

    #rank
    for elem in lis:
        try:
            if elem.find('h4',class_='card-header-title text-white').text == 'Overview':
                try:
                    rank_string = elem.find_all('span',class_='display-3 mb-0')[1].text.strip()
                    rank = int(re.search(r'\d+', rank_string).group())
                except:
                    rank = None
                data_collection.append(rank)
        except:
            continue
    
    #school type
    for elem in lis:
        try:
            if elem.find('h4',class_='card-header-title text-white').text == 'Overview':
                try:
                    school_type = elem.find_all('td',class_='text-right pr-0 font-weight-bold')[2].text
                except:
                    school_type = 'Missing data'
                data_collection.append(school_type)
        except:
            continue
    
    #accept rate
    for elem in lis:
        try:
            if elem.find('h4',class_='card-header-title text-white').text == 'Getting In':
                try:
                    accept_rate_string= elem.find('div',class_='display-3 mb-0').text
                    accept_rate = float(accept_rate_string.split('%')[0])
                except:
                    accept_rate = None
                data_collection.append(accept_rate)
        except:
            continue
    
    #student population
    for elem in lis:
        try:
            if elem.find('h4',class_='card-header-title text-white').text == 'Overview':
                try:
                    student_population_string = elem.find_all('span',class_='display-3 mb-0')[0].text.strip()
                    student_population = int(''.join(student_population_string.split(',')[0:2]))
                except:
                    student_population = None
                data_collection.append(student_population)
        except:
            continue
    
    #Average salary after 10 years
    for elem in lis:
        try:
            if elem.find('h4',class_='card-header-title text-white').text == 'Outcomes':
                try:
                    ave_salary_string = elem.find_all('span',class_='display-3 mb-0')[0].text.strip()
                    ave_salary = int(''.join(ave_salary_string[1:7].split(',')[0:2]))
                except:
                    ave_salary = None
                data_collection.append(ave_salary)
        except:
            continue
    
    #Degree graduation rate
    for elem in lis:
        try:
            if elem.find('h4',class_='card-header-title text-white').text == 'Outcomes':
                try:
                    degree_rate_string = elem.find_all('span',class_='display-3 mb-0')[1].text.strip()
                    degree_rate = int(degree_rate_string[0:2])
                except:
                    degree_rate = None
                data_collection.append(degree_rate)
        except:
            continue
        

    #Adding URL
    data_collection.append(university_web_url)

    return data_collection



def create_database():

    conn = sqlite3.connect("final_project.sqlite")
    cur = conn.cursor()

    drop_Universities_in_states = '''
        DROP TABLE IF EXISTS "Universities_in_states";
    '''

    create_Universities_in_states = '''
        CREATE TABLE IF NOT EXISTS "Universities_in_states" (
            "Id"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "UniversityName"  TEXT NOT NULL,
            "State"  TEXT NOT NULL,
            "NationalRank"    INTEGER
        );
    '''

    drop_University_details = '''
        DROP TABLE IF EXISTS 'University_details'
    '''

    create_University_details = '''
        CREATE TABLE 'University_details' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Name' TEXT NOT NULL,
        'StudentPopulation' INTEGER,
        'SchoolType' TEXT,
        'ApplicationAcceptedRate' INTEGER,
        'AverageSalaryAfterTenYears' INTEGER,
        'BachelorDegreeGraduationRate' INTEGER,
        'UniversityURL' TEXT NOT NULL
        ); 
    '''


    cur.execute(drop_Universities_in_states)
    cur.execute(create_Universities_in_states)
    cur.execute(drop_University_details)
    cur.execute(create_University_details)

    conn.commit()

    return None


#--------------------------------------------------------------------------------------------
#Adding caching(Using some codes from class material)

CACHE_FILENAME = "final_proj.json"
CACHE_DICT = {}

def load_cache():
    ''' opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()


def make_request_using_cache(url,cache):
    ''' Check Whether the information is in the cache dictionary.
    ----------
    url: string
        The keys of the dictionary
    cache: dictionary
        A dictionary is used to store information
    Returns
    -------
    item
        The item of the dictionary.
    '''
    if (url in cache.keys()): 
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")       
        response = requests.get(url)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

#Ending cashing code.
#--------------------------------------------------------------------------------------------

if __name__ == "__main__":

    # #---------------------------caching
    CACHE_DICT = load_cache()
    # #-----------------------------


    create_database()

    conn = sqlite3.connect("final_project.sqlite")
    cur = conn.cursor()

    insert_data_1 = '''
        INSERT INTO Universities_in_states
        VALUES (NULL, ?, ?, ?)
    '''

    insert_data_2 = '''
        INSERT INTO University_details
        VALUES (NULL, ?, ?,?,?,?,?,?)
    '''

    
    unversity_website_dictionary = get_university_sites_url_and_html_and_cashing()
    for website in unversity_website_dictionary.values():
        data = get_data_from_each_university_web(website)

        if len(data) == 9:
            data_list_1 = [data[0],data[1],data[2]]
            data_list_2 = [data[0],data[5],data[3],data[4],data[6],data[7],data[8]]
            cur.execute(insert_data_1,data_list_1)
            cur.execute(insert_data_2,data_list_2)
        else:
            continue


    conn.commit()

