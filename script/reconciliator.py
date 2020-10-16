import json
from time import process_time
import tqdm
from difflib import SequenceMatcher
import sys
import os
import re
import networkx
from networkx.algorithms.components.connected import connected_components
import argparse


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


def to_graph(l):   # https://stackoverflow.com/a/4843408
    graphed_list = networkx.Graph()
    for part in l:
        # each sublist is a bunch of nodes
        graphed_list.add_nodes_from(part)
        # it also imlies a number of edges:
        graphed_list.add_edges_from(to_edges(part))
    return graphed_list


def to_edges(l):  # https://stackoverflow.com/a/4843408
    """
        treat `l` as a Graph and returns it's edges
        to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    """
    it = iter(l)
    last = next(it)

    for current in it:
        yield last, current
        last = current


def double_loop(input_dict, searched_date):
    print("Comparing the entries")
    # First we compare each entry with each other one and give a score to each pair
    for i in tqdm.tqdm(input_dict):
        catalog_entry_i = i.split("_d")[0]
        term = input_dict[i]["term"]
        date = input_dict[i]["date"]
        format = input_dict[i]["format"]
        price = input_dict[i]["price"]
        pn = input_dict[i]["number_of_pages"]
        for j in input_dict:
            catalog_entry_j = j.split("_d")[0]
            if catalog_entry_i == catalog_entry_j: # to compare two sub-entries (two tei:desc from the same item) makes no sense
                pass
            else:
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
                    # We clean the dictionnary, as A-B comparison equals B-A comparison
                    if "%s-%s" % (j, i) in output_dict1:
                        pass
                    else:
                        output_dict1["%s-%s" % (i, j)] = dict2

    # The final list contains the result of the whole comparison process, without filtering, sorted by score
    final_list = []
    for key in output_dict1:
        first_entry = key.split("-")[0]
        second_entry = key.split("-")[1]
        final_list.append((
                          output_dict1[key]["score"], [first_entry, second_entry], output_dict1[key]["author_distance"],
                          {first_entry: mon_dict[first_entry]}, {second_entry: mon_dict[second_entry]}))
    final_list.sort(reverse=True, key=lambda x: (x[2], x[0]))  # we sort by author distance first, and then by the score

    # The filtered list removes all entries with a score lower or equal to 0.6
    sensibility = 0.6
    filtered_list_with_score = [[item[1], item[0]] for item in final_list if item[0] > sensibility and item[2] >= 0.4]

    # Now let's create the clusters. We transform the list of pairs into a graph. The connected nodes are our clusters !
    # See https://stackoverflow.com/a/4843408
    filtered_list = [item[0] for item in filtered_list_with_score]
    graphed_list = to_graph(filtered_list)
    cleaned_list = [list(item) for item in list(connected_components(graphed_list))]
    print(list(graphed_list))
    print(cleaned_list)
    cleaned_output_list = []
    n = 0
    for item in cleaned_list:
        temp_list = []
        for entry in item:
            temp_list.append({entry: mon_dict[entry]})
        cleaned_output_list.append(temp_list)
        cleaned_output_list[n].append(item)
        temp_list.reverse()
        n += 1

    print("Number of pairs found: %s" % (len(filtered_list)))
    print("Number of reconciliated documents: %s" % (len(cleaned_output_list)))
    if searched_date:
        path = '../output/json/%s/%s' % (norm_author, searched_date)
    else:
        path = '../output/json/%s' % norm_author

    with open('%s/reconciliated_pairs.json' % path, 'w') as outfile:
        json.dump(filtered_list_with_score, outfile)

    with open('%s/reconciliated_documents.json' % path, 'w') as outfile:
        outfile.truncate(0)
        json.dump(cleaned_output_list, outfile)
    print(cleaned_output_list)

def cluster_method(dictionnary):
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


def author_filtering(dictionnary):  # this function extracts the entries based on the similarity with the searched author name
    output_dict = {}
    for key in dictionnary:
        if dictionnary[key]["author"] is not None and similar(dictionnary[key]["author"].lower(), author) > 0.75:
            output_dict[key] = dictionnary[key]
    with open('../output/json/%s/filtered_db.json' % norm_author, 'w') as outfile:
        outfile.truncate(0)
        print("Number of documents of %s in the database: %s" % (author, len(output_dict)))
        json.dump(output_dict, outfile)
    return output_dict

def year_filtering(dictionnary):
    output_dict = {}
    if re.compile("^a=").match(date): # a= stands for after
        norm_date = date.split("=")[1]
        for key in dictionnary:
            print(dictionnary[key]["date"])
            if dictionnary[key]["date"] is not None and dictionnary[key]["date"] >= norm_date:
                output_dict[key] = dictionnary[key]
    elif re.compile("^b=").match(date): # b= stands for before
        norm_date = date.split("=")[1]
        for key in dictionnary:
            if dictionnary[key]["date"] is not None and dictionnary[key]["date"] <= norm_date:
                output_dict[key] = dictionnary[key]
    else: # any year range
        date_before = date.split("-")[0]
        date_after = date.split("-")[1]
        for key in dictionnary:
            if dictionnary[key]["date"] is not None and date_before <= dictionnary[key]["date".split("-")[0]] <= date_after:
                output_dict[key] = dictionnary[key]
    with open('../output/json/%s/%s/filtered_db.json' % (norm_author, date), 'w') as outfile:
        outfile.truncate(0)
        json.dump(output_dict, outfile)
    return output_dict

def dircreate(path):
    try:
        os.mkdir(path)
    except:
        pass

if __name__ == "__main__":
    t1 = process_time()

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--author", help="Author to be processed (mandatory !)")
    parser.add_argument("-date", "--date", help="Date of the documents to be found (b= for before, a= for after, YYYY-YYYY for a year range)")
    if len(sys.argv)==1:
      sys.exit("""Please give me the name of the author with the -a flag !""")
    args = parser.parse_args()
    author = args.author
    date = args.date
    normalisation_table = str.maketrans("éèêàç", "eeeac") # We normalize author names to create the folders
    norm_author = author.translate(normalisation_table)
    print(author)

    dircreate("../output/json/%s" % norm_author)
    dircreate("../output/json/%s/%s" % (norm_author, date))

    with open('../output/json/export.json', 'r') as outfile:
        mon_dict = json.load(outfile)

    mon_dict = author_filtering(mon_dict)
    if date:
        mon_dict = year_filtering(mon_dict)
    output_dict1 = {}
    print("Number of entries after filtering: %s" % len(mon_dict))
    double_loop(mon_dict, date)
    t_stop = process_time()
    print("Elapsed time during the whole program in seconds:", t_stop - t1)
