import requests
import json
from conf import key,token

class Trello:
    def __init__(self,key,token):
        self.auth = {'key':key,'token':token}
        self.url= "https://api.trello.com/1"
        self.headers = {
            'type': "type",
            'content-type': "application/json"
                }

    def get_account_details(self):
            "Get the details of the user"
            result_flag = False
            get_account_details_url = 'https://api.trello.com/1/members/me/'
            try:
                response = requests.get(url=get_account_details_url,params=self.auth)
                if response.status_code == 200:
                    self.boards = response.json()['idBoards']
                    result_flag = True
            except Exception as e:
                print (str(e))
        
            return result_flag

    def get_board_names(self):
            get_board_url = 'https://api.trello.com/1/members/me/boards'
            board_list=[]
            try:
                response = requests.get(url=get_board_url,params=self.auth)
                response = response.json()
                for i in range(len(response)):
                    board_list.append(response[i]["name"])
            except Exception as e:
                print(str(e))
           
            return board_list


    def get_board_id_by_name(self,board_name):
            "Get the board id for a board name"
            board_id = None
            self.get_account_details()
            for board in self.boards:  
                board_url = self.url + '/boards/' + board
                
                board_details = requests.get(url=board_url,params=self.auth)

                board_details = board_details.json()
                
                if board_details['name']  == board_name:
                    board_id = board
            return board_id

    def get_board_list(self,board_id):
        "Get the board id for a board name"
        board_list_url = self.url +'/boards/'+ board_id +'/lists'
        board_details = requests.get(url=board_list_url,params=self.auth)
        return board_details.json()

    def get_board_label(self,board_id):

        board_label_url = self.url +'/boards/'+ board_id +'/labels'
        board_label_details = requests.get(url=board_label_url,params=self.auth)
        return board_label_details.json()

    def get_list_id(self,board_id,list_name):
        "Get the list id where you are adding the new cards"

        board_list = self.get_board_list(board_id)
        for i in range(len(board_list)):
            if board_list[i]['name'] == list_name:
                board_list_id = board_list[i]['id']
        return board_list_id

    def get_lable_id_board(self,board_id,label_name):

        label_id = None
        board_label_details = self.get_board_label(board_id)
        for i in range(len(board_label_details)):
            if board_label_details[i]['color'] == label_name:
                labels_id = board_label_details[i]['id']
        return labels_id

        


    # def add_card_to_given_list(self, list_name, new_card_name, )
    def add_member_card(self,board_name,card_name,list_name,label_name,comment):
        " Add members to the board"
        result_flag = True
        board_id = self.get_board_id_by_name(board_name)
        list_id = self.get_list_id(board_id,list_name)
        label_id = self.get_lable_id_board(board_id,label_name)
        
        url = self.url + "/cards"
        querystring = {"name": card_name, "idList": list_id,'idLabels':label_id,"key": key, "token": token}
        response = requests.request("POST", url, params=querystring)
        card_id = response.json()["id"]
        #url for adding comment to card
        url_for_comment = self.url +'/cards/'+ card_id +'/actions/comments'
        comment_string = {"key": key, "token": token, 'text':comment}
        response = requests.request("POST", url_for_comment, params=comment_string)

        return card_id
       



