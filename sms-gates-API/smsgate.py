import re
import time

import requests
import datetime
import socket
from urllib.parse import quote_plus
from .pswd import generate_password


class ZTEmf823dAsSmsGate(object):
    def __init__(self, host='192.168.0.1'):
        self.host = host

    @staticmethod
    def convert_message_content_to_hex_char_code(message_content):
        def add_zero_before_numbers_if_len_lt_4(char_in_hex):
            while len(char_in_hex) < 4:
                char_in_hex = '0' + char_in_hex
            return char_in_hex

        content_in_hex = ''.join([add_zero_before_numbers_if_len_lt_4(hex(ord(el))[2:]) for el in message_content])
        return content_in_hex

    @staticmethod
    def get_message_content(message_in_hex):
        return ''.join([chr(int(message_in_hex[i * 4:(i + 1) * 4], 16)) for i in range(len(message_in_hex) // 4)])

    def get_sms_list(self):
        url = f'http://{self.host}/goform/goform_get_cmd_process?isTest=false&' \
              f'cmd=sms_data_total&page=0&data_per_page=500' \
              f'&mem_store=1&tags=10&order_by=order+by+id+desc&_=1557334439163'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': self.host,
            'Referer': 'http://192.168.0.1/index.html',
        }
        result = requests.get(url, headers=headers).json()
        for message in result['messages']:
            message_content = message['content']
            message['content'] = self.get_message_content(message_content)
        return result

    def send_sms(self, phone_number, message_content):
        send_sms_url = f'http://{self.host}/goform/goform_set_cmd_process'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'DNT': '1',
            'Host': self.host,
            'Origin': f'http://{self.host}',
            'Referer': f'http://{self.host}/index.html',
        }
        date_now = datetime.datetime.now().strftime("%y;%m;%d;%H;%M;%S") + ';+3'
        data = {
            'isTest': 'false',
            'goformId': 'SEND_SMS',
            'notCallback': 'true',
            'Number': phone_number,
            'sms_time': date_now,
            'MessageBody': self.convert_message_content_to_hex_char_code(message_content),
            'ID': -1,
            'encode_type': 'UNICODE'
        }
        return requests.post(send_sms_url, data=data, headers=headers).json()


class YeaStarTg100(object):
    @staticmethod
    def print_server_response(sock, recive_end=b'\r\n\r\n'):
        response = b''
        while True:
            data = (sock.recv(1024))
            if data != b'':
                response +=data
            if recive_end in data:
                break
        return response

    def __init__(self, ip: str='', port: int=5038, username: str='', password: str=''):
        self.gsm_port = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

        command = (f'Action: Login\r\nUsername: {username}\r\nSecret: {password}\r\n\r\n'.encode())
        self.sock.send(command)
        self.print_server_response(self.sock)

        self.sock.send(b'Action: smscommand\r\ncommand: gsm show spans\r\n\r\n')
        response = self.print_server_response(self.sock).decode()
        response = (el.split(':') for el in response.replace('\r', '').split('\n') if el and 'Power on' in el)
        for gsm_port in response:
            gsm_port = re.findall('span \d{1}', gsm_port[0])
            if gsm_port:
                self.gsm_port = gsm_port[0]

    def send_sms(self, message: str, recipient_number: str='375291234567'):
        if not self.gsm_port:
            return "ERR"
        gsm_port = re.findall(r'\d', self.gsm_port)[0]
        message = quote_plus(f'{message}')
        message_uid = generate_password(32)
        command = f'Action: smscommand\r\n' \
                  f'command: gsm send sms {gsm_port}+1 {recipient_number}' \
                  f' \"{message}\" {message_uid}\r\n\r\n'.encode()
        self.sock.send(command)
        response = (self.print_server_response(self.sock, b'--END SMS EVENT--'))
        return "OK" if b'Status: 1' in response else "ERR"

    def check_port(self):
        command = f'Action: smscommand\r\ncommand: gsm show {self.gsm_port}+1\r\n\r\n'.encode()
        self.sock.send(command)
        return self.print_server_response(self.sock)


if __name__ == "__main__":
    sms = YeaStarTg100(ip='192.168.63.142', port=5038, username='username', password='paSSword')
    print(sms.check_port().decode())
