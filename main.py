import requests
import bs4
import csv

base_url = "https://it.wikipedia.org"


def main():
    municipalities = get_municipalities()
    tw_dictionary = get_twinnings(municipalities)
    save(tw_dictionary)


def get_municipalities():
    alphabetical_index = get_alphabetical_index()
    municipalities_dict = build_dict(alphabetical_index)
    return municipalities_dict


def get_alphabetical_index():
    print("Getting alphabetical index...")
    general_index = "https://it.wikipedia.org/wiki/Comuni_d%27Italia"
    res = requests.get(general_index)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "lxml")
    elements_tags = soup.select("a[href^='/wiki/Comuni_d%27Italia_(']")
    alphabetical_index = []
    for i in elements_tags:
        alphabetical_index.append(base_url + i.attrs["href"])
    return alphabetical_index


def build_dict(index):
    print("Getting municipalities information...")
    municipalities_dict = {}
    for i in index:
        res = requests.get(i)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "lxml")
        elements_tags = soup.select("table[class~='wikitable'] a")
        # stores municipality, province and region sequentially,
        # so we need to iterate the list by threes
        length = len(elements_tags)
        for j in range(0, length, 3):
            link = base_url + elements_tags[j].attrs["href"]
            name = elements_tags[j].getText()
            province = elements_tags[j+1].getText()
            region = elements_tags[j+2].getText()
            temp_dict = {
                "name": name,
                "province": province,
                "region": region
            }
            # nested dictionary
            municipalities_dict[link] = temp_dict
    return municipalities_dict


def get_twinnings(municipalities):
    for i in municipalities:
        print("Getting twinnings for " + municipalities[i]["name"] + "...")
        municipalities[i]["twinnings"] = []
        res = requests.get(i)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "lxml")
        countries_tags = soup.select("ul > li > a[href^='/wiki/File:Flag']")
        names_tags = soup.select("ul > li > a[href^='/wiki/File:Flag'] + a")
        # iterate through the two lists in parallel
        for j, k in zip(countries_tags, names_tags):
            country = j.attrs["title"]
            name = k.getText()
            new_twinning = {
                "country": country,
                "name": name
            }
            municipalities[i]["twinnings"].append(new_twinning)
    return municipalities


def save(tw_dictionary):
    first_country = "italia"
    municipalities_without_twinnings = []
    with open("twinnings.csv", "w", newline='', encoding='utf-8') as f:
        twinnings_writer = csv.writer(f, delimiter=",")
        twinnings_writer.writerow(["first_country", "region", "province", "first_name",
                                   "second_country", "second_name"])
        for i in tw_dictionary:
            region = tw_dictionary[i]["region"].lower()
            province = tw_dictionary[i]["province"].lower()
            first_name = tw_dictionary[i]["name"].lower()

            # if the municipality has got at least one twinning, write them to the file
            if tw_dictionary[i]["twinnings"]:
                print("Saving twinnings for " + tw_dictionary[i]["name"] + "...")
                for j in tw_dictionary[i]["twinnings"]:
                    second_country = j["country"].lower()
                    second_name = j["name"].lower()
                    twinnings_writer.writerow([first_country, region, province, first_name,
                                               second_country, second_name])

            # else, save municipality information in a list
            else:
                municipalities_without_twinnings.append([region, province, tw_dictionary[i]["name"]])

    # save municipalities without twinnings in a list
    with open("twinningless.csv", "w", newline='', encoding='utf-8') as f:
        twinningless_writer = csv.writer(f, delimiter=",")
        twinningless_writer.writerow(["region", "province", "name"])
        for i in municipalities_without_twinnings:
            print("Saving information for twinningless municipality " + i[2] + "...")
            i[2] = i[2].lower()
            twinningless_writer.writerow(i)


if __name__ == "__main__":
    main()
