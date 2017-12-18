
from urllib.request import urlopen
import json
import requests
import json_loader
import fetch
from bs4 import BeautifulSoup

# loads heroes.json into memory for testing
# with open(r"C:\Users\z071728\pust777\five-man-bot\FiveMan\content_lookup.json") as f:
#     data = json.load(f)
######################################################################
# for elem in data:
#     elem = {"hots-cntr": i, "hots-pch-nts": i, "icy-veins": i,
#                 "storm-spy": elem[i]["storm-spy"]}
######################################################################
# # loaded aliases and names
# for elem in data:
#     elem['alias'] = alias.get(elem['name'], elem['alias'])
#    elem['name'] = heroes.get(elem['id'])
######################################################################
# # prints list
# for elem in data[:73]:
#     print('{0}--{1}'.format(elem['id'], elem['name']))
content_file = r"C:\Users\pust7\five-man-bot\FiveMan\content_lookup.json"
content_json = json_loader.get_json(content_file)

def item_generator(json_input, lookup_value, yield_value):
    if isinstance(json_input, dict):
        for k, v in json_input.iteritems():
            if v == lookup_value:
                yield json_input[yield_value]
            else:
                for child_val in item_generator(v, lookup_value, yield_value):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, lookup_value, yield_value):
                yield item_val

def get_hero_list():
    '''Returns a list of current heroes from battlenet'''
    url = "http://us.battle.net/heroes/en/heroes/#/"
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.text, 'html.parser')
    for cdata in soup.findAll(text=True):
        if "window.heroes" in cdata:
            cdata = cdata.split(".heroes = ")[1]
            heroes = cdata.split(";\n")[0]
            continue
    hero_json = json.loads(heroes)
    hero_list = []
    for elem in hero_json:
        hero_list.append(elem['analyticsName'])
    hero_list.remove('chogall')
    hero_list.append('cho')
    hero_list.append('gall')
    return hero_list

def get_hero_name(hero):
    '''Return correct hero name when given alias name'''
    try:
        alias_json = json_loader.get_json("alias_lookup.json")
    except IOError:
        alias_json = json_loader.get_json(r"C:\Users\pust7\five-man-bot\FiveMan\alias_lookup.json")
    if alias_json.get(hero.lower(), "HeroError") == "HeroError":
        return "{} is not a valid hero".format(hero)
    else:
        return alias_json.get(hero.lower())

def get_hero_content_name(hero, content):
    '''Returns correct hero name when given hero name and content type'''
    try:
        content_json = json_loader.get_json("content_lookup.json")
    except IOError:
        content_file = r"C:\Users\pust7\five-man-bot\FiveMan\content_lookup.json"
        content_json = json_loader.get_json(content_file)
    if hero.lower() in content_json:
        hero_name = content_json.get(hero.lower())[content]
    else:
        return "{} is not a valid hero".format(hero)
    return hero_name

# def get_talent_tier(hero, hero_build_list):
#     '''TODO write function that returns {"Hamstring": [1, 1, 1, 1, 3, 2, 4]}'''
#     resp = requests.get("https://hotsapi.net/api/v1/heroes/{}".format(hero), verify=False)
#     hero_json = resp.json()["talents"]
    # elem in hero_build_list[1:]

def get_hero_builds(hero):
    '''returns hero builds from icy-veins.com'''
    build_dict = {hero: {}}
    if get_hero_name(hero.lower()) != "HeroError":
        content_hero = get_hero_content_name(get_hero_name(hero.lower()), "icy-veins")
        url = 'https://www.icy-veins.com/heroes/{}-build-guide'.format(content_hero)
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        builds = soup.find('div', class_='heroes_tldr')
        # gets talent names
        if builds.findAll('h4') != []:
            for h4_tag in builds.findAll('h4'):
                if "Build" in h4_tag.get_text():
                    build_name = h4_tag.get_text()[:-25].replace("\n", "")
                for a_tag in h4_tag.findAll("a"):
                    build_dict[hero][build_name] = ','.join(a_tag["href"][-7:])
            return build_dict
        else:
            for bold_tag in builds.findAll('b'):
                if "Build" in bold_tag.get_text():
                    talent_list = []
                    build_name = bold_tag.get_text()[:-1]
                elif  "Lost" in bold_tag.get_text():
                    talent_list = []
                    build_name = bold_tag.get_text()[:-1]
                for tier in builds.findAll('span', 'heroes_tldr_talent_tier_visual'):
                    x = 1
                    for bool_tag in tier.findAll("span"):
                        if str(bool_tag) == '<span class="heroes_tldr_talent_tier_no"></span>':
                            x = x + 1
                        else:
                            talent_list.append(x)
                            if len(talent_list) == 7:
                                build_dict[hero][build_name] = ','.join(str(s) for s in talent_list)
                                talent_list = []
            return build_dict
    else:
        return "{} is not a valid hero".format(hero)

def main():
    builds = {}
    for hero in get_hero_list()[35:]:
        builds.update(get_hero_builds(hero))
    print(builds)

if __name__ == '__main__':
    main()



# writes json file
# with open(r"C:\Users\pust7\five-man-bot\FiveMan\content_lookup.json", 'w') as f:
#     json.dump(data, f, indent=4)
