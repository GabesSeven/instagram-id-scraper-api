#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Gabrie Ferreira
# colocar cometário de dados
# inserir e criar o read-me

# ******** libraries ********
import os
import sys
import getpass
import shutil
import requests
import json
import configparser
import uuid
import hmac
import hashlib


# ******** global variables ********
link = 'https://www.instagram.com/accounts/login/'
login_url = 'https://www.instagram.com/accounts/login/ajax/'

# account_username = ''
# account_password = ''


# ******** Instagram class start ********
class Instagram :

    def __init__(self, username, password):
        self.session = requests.session()
        self.username = username
        self.password = password
        self.device_id = "DAA237D-CB58-4D4D-8096-2F5E172921A3"
        self.pk = None
        self.csrftoken = None
        self.base_url = "https://i.instagram.com/api/v1/"
        self.secret_key = ("ac5f26ee05af3e40a81b94b78d762dc8287bcdd8254fe86d0971b2aded8884a4")
        self.key_version = "4"
        self.headers = {
            "Host": "i.instagram.com",
            "X-IG-Connection-Speed": "44kbps",
            "Accept": "*/*",
            "X-IG-Connection-Type": "WiFi",
            "X-IG-App-ID": "124024574287414",
            "Accept-Language": "en-US;q=1",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-IG-ABR-Connection-Speed-KBPS": "0",
            "User-Agent": "Instagram 39.0.0.12.95 (iPhone6,1; iOS 10_2; en_US; en-US; scale=2.00; gamut=normal; 640x1136) AppleWebKit/420+",
            "Connection": "keep-alive",
            "X-IG-Capabilities": "36r/Bw==",
        }

    #######################################################

    def calculate_hash(self, message):
        return hmac.new(self.secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

    #######################################################

    def reorder_signed_body(self, signed_body_json):
        key_association = {}
        reordered_dict = {}
        for key in list(signed_body_json.keys()):
            result = 0
            for char in key:
                result = (-result + (result << 5) + ord(char)) & 0xFFFFFFFF
            if sys.maxsize > 2 ** 32:  # if os is 64 bit
                if result > 0x7FFFFFFF:
                    result -= 0x100000000
                elif result < -0x80000000:
                    result += 0x100000000
            key_association[key] = result
        hash_sorted_keys = sorted(key_association.items(), key=lambda x: x[1])
        for t in hash_sorted_keys:
            reordered_dict[t[0]] = signed_body_json[t[0]]
        return reordered_dict

    #######################################################

    def generate_signed_body(self, signed_body_dict):
        reordered_stringed_dict = json.dumps(self.reorder_signed_body(signed_body_dict)).replace(" ", "")
        signed_hash = self.calculate_hash(reordered_stringed_dict)
        return f"{signed_hash}.{reordered_stringed_dict}"

    ######################################################

    def make_request(self, method, endpoint, params=None, data=None, json=None, headers=None, json_content=True):
        res = self.session.request(
            method,
            f"{self.base_url}{endpoint}",
            params=params,
            data=data,
            json=json,
            headers=headers,
        )

        if json_content is True:
            return res.json()
        return res

    #######################################################

    def login_2fa(self, username, code_2fa, id_2fa):
        data = {
            "signed_body": self.generate_signed_body(
                {
                    "username": username,
                    "adid": "uuid-adid",
                    "device_id": self.device_id,
                    "two_factor_identifier": str(id_2fa),
                    "verification_code": str(code_2fa),
                }
            ),
            "ig_sig_key_version": self.key_version,
        }

        login_2fa_response = self.make_request(
            "POST",
            "accounts/two_factor_login/",
            data=data,
            headers=self.headers,
            json_content=False,
        )
        return login_2fa_response

    #######################################################

    def login(self):
        data = {
            "signed_body": self.generate_signed_body(
                {
                    "reg_login": "0",
                    "password": self.password,
                    "device_id": self.device_id,
                    "username": self.username,
                    "adid": "uuid-adid",
                    "login_attempt_count": "0",
                    "phone_id": self.device_id,
                }
            ),
            "ig_sig_key_version": self.key_version,
        }

        login_response = self.make_request("POST", "accounts/login/", data=data, headers=self.headers, json_content=False)

        if login_response.json().get("two_factor_required"):
            code_2fa = input("[*] 2fa required - Enter code received: ")
            username = login_response.json().get("two_factor_info").get("username")
            id_2fa = (login_response.json().get("two_factor_info").get("two_factor_identifier"))
            login_response = self.login_2fa(username, code_2fa, id_2fa)

        print(login_response)
        self.pk = str(login_response.json()["logged_in_user"]["pk"])
        self.csrftoken = login_response.cookies["csrftoken"]
        return login_response.json()

    #######################################################

    def logout(self):
        data = {"device_id": self.device_id}
        return self.make_request("POST", "accounts/logout/", data=data, headers=self.headers)

    #######################################################

    def search_top(self, search_string):
        query_string_params = {
            "rank_token": f"{self.pk}_{str(uuid.uuid4()).upper()}",
            "query": search_string,
            "context": "blended",
            "timezone_offset": "-14400",
        }

        return self.make_request("GET", "fbsearch/topsearch_flat/", params=query_string_params, headers=self.headers)
# ******** Instagram class start ********


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

        # ******** capture data for authentication and login Instagram ********
        numbers_of_attempts = 0

        while True:
            print('\n\n**** Connect to an Instagram account **** ')
            print('\nUsername: ', end='')
            account_username = input()
            account_password = getpass.getpass(prompt='\nPassword: ')

            IG = Instagram(account_username, account_password)

            IG.login()

            try:
                print('\n\n**** Connecting to Instagram... **** ')
                if IG.login():
                  break
            except:
                numbers_of_attempts += 1
                print("\n\n**** Login failed, %s attempt(s) **** " % numbers_of_attempts)

            # ******** checks number of access attempts ********
            if(numbers_of_attempts == 3):
                print('\n\n**** More than three incorrect authentication attempts. See you later... **** ')
                Usage(False)

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
            search_results = IG.search_top(search)
            length = len(search_results["list"])
            print('\n\n**** %s results found **** ' % length)

            # ******** discovering and recording pks ********
            # if length == 3:
            #     # output_file.write(
            #     #     search+u"\u007C"+
            #     #     search_results["list"][0]["user"]["pk"]+','+
            #     #     search_results["list"][1]["user"]["pk"]+','+
            #     #     search_results["list"][2]["user"]["pk"]+'\n'
            #     # )
            #     print(
            #         "%s|%s,%s,%s\n" % (
            #             search,
            #             search_results["list"][0]["user"]["pk"],
            #             search_results["list"][1]["user"]["pk"],
            #             search_results["list"][2]["user"]["pk"],
            #         ),
            #         end='',
            #         file=output_file,
            #     )
            #

            if length == 2:
                # output_file.write(
                #     search+'|'+
                #     search_results["list"][0]["user"]["pk"]+','+
                #     search_results["list"][1]["user"]["pk"]+'\n'
                # )
                print(
                    "%s|%s,%s\n" % (
                        search,
                        search_results["list"][0]["user"]["pk"],
                        search_results["list"][1]["user"]["pk"],
                    ),
                    end='',
                    file=output_file,
                )
            elif length == 1:
                # output_file.writeline(
                #     search+'|'+
                #     search_results["list"][0]["user"]["pk"]+'\n'
                # )
                print(
                    "%s|%s\n" % (
                        search,
                        search_results["list"][0]["user"]["pk"],
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

        IG.logout()
        input_file.close()
        output_file.close()
# ******** main function end ********


if __name__ == "__main__":
  sys.exit(main())
