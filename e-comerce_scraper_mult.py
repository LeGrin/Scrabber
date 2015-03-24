#!/usr/bin/env python
# -*- coding: ASCII -*-

import os
import HTMLParser
import sys
import itertools
import time
import urllib2
import multiprocessing


class BColors:
    def __init__(self):
        pass

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Info:
    def __init__(self):
        pass

    def _init_(self):
        self.Company_name = ""
        self.Company_type = ""
        self.Company_subtype = ""
        self.Company_region = ""
        self.Company_url = ""
        self.Company_number = ""
        self.Company_email = ""
        self.Company_skype = ""
        self.Company_contact_person = ""

    def valid_info(self):
        n = BColors.HEADER + '[N]' + BColors.ENDC if self.Company_name == " " \
            else BColors.OKGREEN + '[N]' + BColors.ENDC
        t = BColors.HEADER + '[T]' + BColors.ENDC if self.Company_type == " " \
            else BColors.OKGREEN + '[T]' + BColors.ENDC
        s = BColors.HEADER + '[S]' + BColors.ENDC if self.Company_subtype == " " \
            else BColors.OKGREEN + '[S]' + BColors.ENDC
        r = BColors.HEADER + '[R]' + BColors.ENDC if len(self.Company_region) < 4 \
            else BColors.OKGREEN + '[R]' + BColors.ENDC
        u = BColors.HEADER + '[U]' + BColors.ENDC if self.Company_url == " " \
            else BColors.OKGREEN + '[U]' + BColors.ENDC
        num = BColors.HEADER + '[NUM]' + BColors.ENDC if '+380' not in self.Company_number \
            else BColors.OKGREEN + '[NUM]' + BColors.ENDC
        e = BColors.HEADER + '[E]' + BColors.ENDC if '@' not in self.Company_email \
            else BColors.OKGREEN + '[E]' + BColors.ENDC
        sky = BColors.HEADER + '[SKY]' + BColors.ENDC if len(self.Company_skype) < 4 \
            else BColors.OKGREEN + '[SKY]' + BColors.ENDC
        c = BColors.HEADER + '[C]' + BColors.ENDC if self.Company_contact_person == " " \
            else BColors.OKGREEN + '[C]' + BColors.ENDC
        return n + t + s + r + u + num + e + sky + c

    def print_info(self):
        return ('"' + self.Company_name + '"' + "," + '"' + self.Company_type + '"' + "," + '"' + self.Company_subtype +
                '"' + "," + '"' + self.Company_region + '"' + "," + '"' + self.Company_url + '"' + "," + '"' +
                self.Company_number + '"' + "," + '"' + self.Company_email + '"' + "," + '"' + self.Company_skype +
                '"' + "," + '"' + self.Company_contact_person + '"').replace(
            '\t', '').replace('\r', '').replace('\n', '') + '\n'


def get_page(url):
    try:
        # print 'trying to get ' + url
        time.sleep(2)
        return opener.open(url).read()
    except:
        return ""


def get_range(dictionary):
    if batch == 0:
        return dictionary
    if batch == 1:
        return dict(itertools.islice(dictionary.iteritems(), 0, 10))
    if batch == 2:
        return dict(itertools.islice(dictionary.iteritems(), 11, 20))
    if batch == 3:
        return dict(itertools.islice(dictionary.iteritems(), 21, 30))
    if batch == 4:
        return dict(itertools.islice(dictionary.iteritems(), 11, 42))


def get_categories(cat_class, pages):
    categories = {}
    i = 0
    for link in pages.values():
        # print "Parsing..."
        # print link
        # print "links"
        link_char = 0
        page = get_page(link)
        while link_char != -1:
            link_char = page.find(cat_class, link_char + 1)
            if link_char == -1:
                break
            start_quote = page.find("href=", link_char)
            start_quote = page.find('"', start_quote + 1)
            end_quote = page.find('"', start_quote + 1)
            url = page[start_quote + 1:end_quote]
            start_quote = page.find(">", end_quote)
            end_quote = page.find("<", start_quote + 1)
            name = str(page[start_quote + 1:end_quote])
            # print name, url
            file_opened = open(file_path, 'r')
            if ("http" in url) & (url not in visited_pages) & (url not in str(file_opened.read())):
                categories[name] = url
                visited_pages.append(url)
                # print url
                i += 1
            else:
                print '###LUCK###'
    print "number of links " + str(i)
    return categories


def get_max_page(url, pagination):
    num_char = 0
    page = get_page(url)
    num = 0
    while num_char != -1:
        num_char = page.find(pagination, num_char + 1)
        if num_char == -1:
            break
        start_quote = page.find("page=", num_char)
        end_quote = page.find('"', start_quote + 1)
        start_quote = page.find(">", end_quote)
        end_quote = page.find("<", start_quote + 1)
        num_char = end_quote
        num = int(page[start_quote + 1:end_quote])
    return num


def gen_next_link(initial_url, page_str, number):
    if str(number) == 0:
        return initial_url
    return initial_url + page_str + str(number)


def file_writer(company_info, path):
    file_opened = open(path, 'a')
    file_opened.write(company_info.print_info())
    file_opened.close()
    return None


def sum_files(sum_filepath, file_folder):
    for file_in_folder in os.listdir(file_folder):
        if file_in_folder.endswith('.csv'):
            print file_in_folder
            file_opened = open(sum_filepath, 'a')
            file_copied = open(file_folder + file_in_folder, 'r')
            file_opened.write(file_copied.read())
            file_opened.close()
    return None


def scrabble_site(url):
    file_opened = open(file_path, 'a')
    file_opened.write("CompanyName,Category,SubCategory,Region,Site,Numbers,Email,Skype,Person\n")
    file_opened.close()
    categories = get_categories(catalog_class, {"": url})
    # os.system('echo started with ' + str(len(categories)) + ' categories' + ' | wall')
    jobs = []
    for category in get_range(categories):
        p = multiprocessing.Process(target=process_subcategories, args=(category, categories,))
        jobs.append(p)
        p.start()
    return None


def process_companies(category, subcategory, subcategories):
    counter = 0
    print '##' + subcategory
    max_page_num = get_max_page(subcategories[subcategory], pagination_class)
    if max_page_num == 0:
        max_page_num = 1
    for number in range(1, max_page_num + 1):
        companies = get_categories(company_link_class,
                                   {subcategory: gen_next_link(subcategories[subcategory], next_page_appender, number)})
        for company in companies:
            if "http://www.ua.all.biz/click.php" not in companies[company]:
                companies[company] += '/contacts'
                # os.system(companies[company] + " " + get_contact_info(companies[company], category, subcategory)+ \
                # 'wall')
                # print companies[company] + " " +
                # if batch == 1:
                # start = 10392
                # if batch == 2:
                # start = 9763
                # if batch == 3:
                # start = 11500
                # if batch == 4:
                # start = 9260
                # if (counter >= start):
                # get_contact_info(companies[company], category, subcategory)
                # print str(counter) + " " + category + " " + /
                # get_contact_info(companies[company], category, subcategory)
                counter += 1
                get_contact_info(companies[company], category, subcategory)
    print subcategory + " DONE"


def process_subcategories(category, categories):
    print category
    subcategories = get_categories(sub_catalog_class, {category: categories[category]})
    # os.system('echo processing batch' + str(batch) + ' | wall')
    # os.system('echo' + '"'+ ' starting category  ' +  str(category)  + ' with ' + str(len(subcategories)) + \
    # ' subcategories' + '"' + '| wall')
    jobs = []
    for subcategory in subcategories:
        p = multiprocessing.Process(target=process_companies, args=(category, subcategory, subcategories,))
        jobs.append(p)
        p.start()
    print category + " DONE"
    return


def get_contact_info(url, category, subcategory):
    page = get_page(url)
    if '?show=phones' in page:
        page = get_page(url + "?show=phones")
    new_contact = Info()
    new_contact.Company_type = category
    new_contact.Company_subtype = subcategory
    new_contact.Company_url = url
    new_contact.Company_skype = get_damn_skype(page)
    email = get_info(email_class, page)
    # if len(email) > 2:
    # print email
    new_contact.Company_email = str(pars.unescape(email.replace('&#xFEFF', ' ').replace('&#x441;', ' ')))
    new_contact.Company_region = get_info(region_class, page)
    new_contact.Company_name = get_info(name_class, page)
    new_contact.Company_number = get_info(phone_class, page)
    new_contact.Company_contact_person = get_info(person_class, page)
    file_writer(new_contact, file_path)
    return new_contact.valid_info()


def get_info(class_type, page):
    item_char = 0
    output = " "
    while item_char != -1:
        item_char = page.find(class_type, item_char + 1)
        if item_char == -1:
            break
        start_quote = page.find(">", item_char)
        end_quote = page.find("<", start_quote + 1)
        output = output + " " + str(page[start_quote + 1:end_quote]).replace('"', '').replace("'", '')
    return output


def get_damn_skype(page):
    item_char = 0
    output = ""
    while item_char != -1:
        item_char = page.find('Skype', item_char + 1)
        if item_char == -1:
            break
        start_quote = page.find("b-link_contacts", item_char)
        start_quote = page.find(">", start_quote)
        end_quote = page.find("<", start_quote + 1)
        output = output + " " + str(page[start_quote + 1:end_quote]).replace('"', '').replace("'", '')
    return output


if __name__ == '__main__':
    start_url = "http://www.ua.all.biz/enterprises"
    catalog_class = "b-left--menu__link"
    sub_catalog_class = "b-left--menu__link"
    pagination_class = "b-paging__link"
    next_page_appender = "?page="
    company_link_class = "b-pli-alliance__contacts__www"
    phone_class = "b-contacts-data-phone tel"
    name_class = '"name"'
    email_class = "b-link b-link_contacts email"
    person_class = "b-contacts-data-content"
    region_class = "locality"
    visited_pages = []
    batch = int(sys.argv[1])
    file_path = "main_mult" + str(batch) + ".csv"
    pars = HTMLParser.HTMLParser()
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Googlebot/2.1')]
    scrabble_site(start_url)




