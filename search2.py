#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Gabrie Ferreira
# colocar cometário de dados
# inserir e criar o read-me

# ******** libraries ********
import sys
import os
import urllib.request
import json
from pprint import pprint
import string

# ******** seach function start ********
def searchProfile(url):
    # print(url)
    resp = urllib.request.urlopen(url).read()
    return json.loads(resp.decode('utf-8'))
# ******** seach function start ********

# ******** Usage function start ********
def Usage(error_input):

    if(error_input):
        print('./search.py input-file output-file\n\n              or              \n\npython search.py input-file output-file \n')

    exit()
# ******** Usage function end ********

# ******** main function start ********
def main(argv = None):
    # ******** check number of input parameters ********
    if len(sys.argv) !=3:
        print('Incorrect amount of parameters, try: \n')
        Usage(True)
    else:
        # print(sys.argv[0], sys.argv[1], sys.argv[2])

        # ******** checks if input-file and output-file are existing files ********
        if not(os.path.exists(sys.argv[1]) and os.path.exists(sys.argv[2])):
            # print(os.path.exists(sys.argv[1]), os.path.exists(sys.argv[2]))
            print('No input or output file, try: \n')
            Usage(True)

        # ******** performs fetching each line of the input file and writing to the output file ********
        print('\n\n**** Conducting searches... **** ')

        input_file = open(sys.argv[1], 'r')
        output_file = open(sys.argv[2], 'w')

        count = 1
        searchs = input_file.readlines()

        for search in searchs:
            print("\n\n**************** Search %s: %s  " % (count, search) )
            count+=1

            # ******** perform search on Instagram ********
            url = 'https://instagram.com/web/search/topsearch/?context=blended&query='+search
            search_results = searchProfile(url)
            # print (search_results["users"])

            length = len(search_results["users"])
            print('\n\n**** %s results found **** ' % length)


            # ******** discovering and recording pks ********
            # if length == 3:
            #     # output_file.write(
            #     #     search+u"\u007C"+
            #     #     search_results["users"][0]["user"]["pk"]+','+
            #     #     search_results["users"][1]["user"]["pk"]+','+
            #     #     search_results["users"][2]["user"]["pk"]+'\n'
            #     # )
            #     print(
            #         "%s|%s,%s,%s\n" % (
            #             search,
            #             search_results["users"][0]["user"]["pk"],
            #             search_results["users"][1]["user"]["pk"],
            #             search_results["users"][2]["user"]["pk"],
            #         ),
            #         end='',
            #         file=output_file,
            #     )
            #
            if length == 2:
                # output_file.write(
                #     search+'|'+
                #     search_results["users"][0]["user"]["pk"]+','+
                #     search_results["users"][1]["user"]["pk"]+'\n'
                # )
                print(
                    "%s|%s,%s\n" % (
                        search,
                        search_results["users"][0]["user"]["pk"],
                        search_results["users"][1]["user"]["pk"],
                    ),
                    end='',
                    file=output_file,
                )
            elif length == 1:
                # output_file.writeline(
                #     search+'|'+
                #     search_results["users"][0]["user"]["pk"]+'\n'
                # )
                print(
                    "%s|%s\n" % (
                        search,
                        search_results["users"][0]["user"]["pk"],
                    ),
                    end='',
                    file=output_file,
                )
            else:
                # output_file.write(
                #     search+'|\n'
                # )
                print(
                    "%s|\n" % (
                        search,
                    ),
                    end='',
                    file=output_file,
                )

        input_file.close()
        output_file.close()
# ******** main function end ********


if __name__ == "__main__":
  sys.exit(main())
