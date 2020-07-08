import json
from time import process_time
import tqdm
from difflib import SequenceMatcher
import sys


def similar(a, b):  # https://stackoverflow.com/a/17388505
    return SequenceMatcher(None, a, b).ratio()


def price_cluster(in_dict):
    print("Creation of the price cluster")
    # 0 dicts corresponds to the result of the iteration: for each entry, all corresponding entries
    price_dict_0 = {}
    for i in in_dict:
        i_price = in_dict[i]["price"]
        price = [(k, v["price"]) for k, v in in_dict.items() if v["price"] == i_price]
        price_dict_0[i] = price
    print("End of iteration")

    # 2nd step: creation of the clusters
    new_list = []
    out_list = []
    out_dict = {}

    for i in price_dict_0:
        new_list.append([n for n, v in price_dict_0[i]])
    current_position = 0
    for current_list in new_list:
        if current_list[0] == new_list[current_position - 1][0]:
            pass
        else:
            out_list.append(current_list)
        current_position += 1

    for item in out_list:
        price = mon_dict[item[0]]["price"]
        out_dict[price] = item

    with open('../output/json/price_clusters.json', 'w') as outfile:
        outfile.truncate(0)
        json.dump(out_dict, outfile)

    counter = 0
    for k in out_dict:
        counter += len(out_dict[k])
    print("Number of entries of the price dict: %s" % counter)
    new_list.clear()
    out_list.clear()
    out_dict.clear()


def np_cluster(in_dict):
    print("Creation of the number of pages cluster")
    # 0 dicts corresponds to the result of the iteration: for each entry, all corresponding entries
    np_dict_0 = {}
    for i in in_dict:
        i_pn = in_dict[i]["number_of_pages"]
        numberOfPages = [(k, v["number_of_pages"]) for k, v in in_dict.items() if v["number_of_pages"] == i_pn]
        np_dict_0[i] = numberOfPages
    print("End of iteration")
    # 2nd step: creation of the clusters
    new_list = []
    out_list = []
    out_dict = {}
    for i in np_dict_0:
        new_list.append([n for n, v in np_dict_0[i]])
    current_position = 0
    for current_list in new_list:
        if current_list[0] == new_list[current_position - 1][0]:
            pass
        else:
            out_list.append(current_list)
        current_position += 1

    for item in out_list:
        np = mon_dict[item[0]]["number_of_pages"]
        out_dict[np] = item

    print("New_list: %s " % len(new_list))
    print("Out_list: %s " % len(out_list))
    with open('../output/json/np_clusters.json', 'w') as outfile:
        outfile.truncate(0)
        json.dump(out_dict, outfile)
    new_list.clear()
    out_list.clear()
    out_dict.clear()


def format_cluster(in_dict):
    # 0 dicts corresponds to the result of the iteration: for each entry, all corresponding entries
    print("Creation of the format cluster")
    frmt_dict_0 = {}
    for i in in_dict:
        i_format = in_dict[i]["format"]
        frmt = [(k, v["format"]) for k, v in in_dict.items() if v["format"] == i_format]
        frmt_dict_0[i] = frmt
    print("End of iteration")

    # 2nd step: creation of the clusters
    new_list = []
    out_list = []
    out_dict = {}
    for i in frmt_dict_0:
        new_list.append([n for n, v in frmt_dict_0[i]])
    current_position = 0
    for current_list in new_list:
        if current_list[0] == new_list[current_position - 1][0]:
            pass
        else:
            out_list.append(current_list)
        current_position += 1

    for item in out_list:
        format = mon_dict[item[0]]["format"]
        out_dict[format] = item

    print("New_list: %s " % len(new_list))
    print("Out_list: %s " % len(out_list))
    with open('../output/json/format_clusters.json', 'w') as outfile:
        outfile.truncate(0)
        json.dump(out_dict, outfile)
    new_list.clear()
    out_list.clear()
    out_dict.clear()


def term_cluster(in_dict):
    print("Creation of the term cluster")
    # 0 dicts corresponds to the result of the iteration: for each entry, all corresponding entries
    term_dict_0 = {}
    for i in in_dict:
        i_term = in_dict[i]["term"]
        term = [(k, v["term"]) for k, v in in_dict.items() if v["term"] == i_term]
        term_dict_0[i] = term
    print("End of iteration")
    # 2nd step: creation of the clusters: it works, but why ?
    new_list = []
    out_list = []
    out_dict = {}
    for i in term_dict_0:
        new_list.append([n for n, v in term_dict_0[i]])
    current_position = 0

    for current_list in new_list:
        # if A belonging to list1 is in list2, the two lists are equal, and we can remove one
        if current_list[0] == new_list[current_position - 1][0]:
            pass
        else:
            out_list.append(current_list)
        current_position += 1
    for item in out_list:
        term = mon_dict[item[0]]["term"]
        out_dict[price] = term

    print("New_list: %s " % len(new_list))
    print("Out_list: %s " % len(out_list))
    with open('../output/json/term_clusters.json', 'w') as outfile:
        outfile.truncate(0)
        json.dump(out_dict, outfile)
    new_list.clear()
    out_list.clear()
    out_dict.clear()


def second_method(input_dict):
    with open('../output/json/comparison.json', 'r+') as outfile:
        data = {}
        outfile.truncate(0)
        json.dump(data, outfile)

    for i in tqdm.tqdm(input_dict):
        term = input_dict[i]["term"]
        date = input_dict[i]["date"]
        format = input_dict[i]["format"]
        price = input_dict[i]["price"]
        pn = input_dict[i]["number_of_pages"]
        for j in input_dict:
            dict2 = {}
            score = 0
            if j == i:
                pass
            else:
                if input_dict[j]["term"] == term:
                    score = score + 0.2
                else:
                    score = score - 0.1

                if input_dict[j]["date"] == date and input_dict[j]["date"] is not None:
                    score = score + 0.5
                else:
                    score = score - 0.5

                if input_dict[j]["number_of_pages"] == pn:
                    score = score + 0.1
                else:
                    score = score - 0.1

                if input_dict[j]["format"] == format:
                    score = score + 0.1
                else:
                    score = score - 0.3

                if input_dict[j]["price"] == price:
                    score = score + 0.1
                else:
                    score = score - 0.1
                try:
                    dict2["author_distance"] = similar(input_dict[j]["author"], input_dict[i]["author"])
                except:
                    dict2["author_distance"] = 0
                dict2["score"] = score
                if "%s-%s" % (j, i) in output_dict1:
                    pass
                else:
                    output_dict1["%s-%s" % (i, j)] = dict2
    final_list = []
    print("Écriture du dictionnaire de sortie")
    for key in output_dict1:
        final_list.append((output_dict1[key]["score"], key, output_dict1[key]["author_distance"]))
    final_list.sort(reverse=True, key=lambda x: (x[2], x[0]))  # we sort by author distance first, and then by the score
    final_final_list = [item for item in tqdm.tqdm(final_list) if item[0] >= 0.4 and item[2] >= 0.4]
    print("Nombre d'entrées communes trouvées: %s" % len(final_final_list))

    with open('../output/json/comparison.json', 'w') as outfile:
        json.dump(final_final_list, outfile)


def first_method(dictionnary):
    print("Number of entries of the input dict: %s" % len(dictionnary))
    price_cluster(dictionnary)
    t2 = process_time()
    print(t2 - t1)
    format_cluster(dictionnary)
    t3 = process_time()
    print(t3 - t2)
    np_cluster(dictionnary)
    t4 = process_time()
    print(t4 - t3)
    term_cluster(dictionnary)
    t_stop = process_time()
    print(t_stop - t4)
    print("Elapsed time during the whole program in seconds:", t_stop - t1)


def author_sorting(dictionnary, authorname):  # this function extracts the entries based on the similarity with the searched author name
    output_dict = {}
    for key in dictionnary:
        if dictionnary[key]["author"] is not None and similar(dictionnary[key]["author"].lower(), authorname) > 0.75:
                output_dict[key] = dictionnary[key]
    with open('../output/json/filtered_dict.json', 'w') as outfile:
        outfile.truncate(0)
        json.dump(output_dict, outfile)
    return output_dict


if __name__ == "__main__":
    t1 = process_time()
    author = sys.argv[1]
    with open('../output/json/export.json', 'r') as outfile:
        mon_dict = json.load(outfile)
    mon_dict = author_sorting(mon_dict, author)
    output_dict1 = {}
    second_method(mon_dict)
    t_stop = process_time()
    print(t_stop - t1)
    print("Elapsed time during the whole program in seconds:", t_stop - t1)
