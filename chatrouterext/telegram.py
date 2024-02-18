# -*-coding:utf8;-*-
import os
import json
import requests


class telegram:
    """
    Python Telegram bot API wrapper that can be run on every Python 3.
    author: guangrei
    reference https://telegram-bot-sdk.readme.io/reference
    """
    token = os.environ.get("TG_BOT_TOKEN")
    endpoints = 'https://api.telegram.org/bot'+token+'/'
    ssl_verify = True
    data = None
    
    def parse_response(data):
        """
        Function to make telegram response accessible through dot "." like an object.
        The key "from" renamed to "_from" to avoid conflict with Python keyword "from".
        Special thanks to ChatGPT :)
        Args:
            data (dict): json decoded from telegram response.
        Returns:
            dict: dict that can be accessed like an object.
        """
        
        def find_and_replace(data, old_key, new_key):
            if isinstance(data, list):
                for i in range(len(data)):
                    data[i] = find_and_replace(data[i], old_key, new_key)
            elif isinstance(data, dict):
                new_dict = {}
                for key, value in data.items():
                    if key == old_key:
                        new_dict[new_key] = value
                    else:
                        new_dict[key] = find_and_replace(value, old_key, new_key)
                return new_dict
            else:
                return data
                
        def format_dict_nested(dictionary):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    format_dict_nested(value)
                    dictionary[key] = objectify(value)
            return dictionary
            
        class objectify(dict):
            __slots__ = () 
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
            
        def parse(array):
            array = find_and_replace(array, "from", "_from")
            u = format_dict_nested(array)
            return objectify(u)
            
        ret = parse(data)
        return ret
    
    def update(data):
        """
        Function to update telegram.data
        Args:
            data (str): data telegram webhook json.
        """
        data = json.loads(data)
        telegram.data = telegram.parse_response(data)
        
    # below is the low level telegram api wrapper
    
    def set_webhook(url, certificate=None):
        """
        Use this method to specify a url and receive incoming updates via an outgoing webhook.
        Args:
            url (str): HTTPS url to send updates to. Use an empty string to remove webhook integration.
            certificate (str, optional): Path to certificate file. Default to None.
        Returns:
            dict: dict that can be accessed like an object.
        """
        api = telegram.endpoints + 'setWebHook'
        data = {
        "url": url
        }
        if certificate is not None:
            files = {
            'certificate': (os.path.basename(certificate), open(certificate))
            }
            ret = requests.post(api, data=data, files=files, verify=telegram.ssl_verify).json()
        else:
            ret = requests.post(api, json=data, verify=telegram.ssl_verify).json()
        return telegram.parse_response(ret)
        
    def remove_webhook():
        """
        Use this method to remove a previously set outgoing webhook.
        Returns:
            dict: dict that can be accessed like an object.
        """
        api = telegram.endpoints + 'setWebhook?remove'
        payload = { "url": "Empty" }
        ret = requests.post(api, json=payload, verify=telegram.ssl_verify)
        return telegram.parse_response(ret)    
    
    def get_updates(offset=None, limit=100, timeout=0):
        """
        Use this method to receive incoming updates using long polling.
        Args:
            offset (int, optional): Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. An update is considered confirmed as soon as getUpdates is called with an offset higher than its update_id. The negative offset can be specified to retrieve updates starting from -offset update from the end of the updates queue. All previous updates will forgotten. Defaults to None.
            limit (int, optional): Limits the number of updates to be retrieved. Values between 1—100 are accepted. Defaults to 100.
            timeout (int, optional): Timeout in seconds for long polling. Defaults to 0.
        Returns:
            dict: dict that can be accessed like an object.
        """
        payload = {
        "offset": offset,
        "limit": limit,
        "timeout": timeout
        }
        api = telegram.endpoints + 'getUpdates'
        ret = requests.post(api, json=payload, verify=telegram.ssl_verify).json()
        return telegram.parse_response(ret)
        
    def send_message(text, chat_id, parse_mode=None, disable_web_page_preview=False, disable_notification=False, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send text messages.
        Args:
            text (str): Text of the message to be sent.
            chat_id (str): Unique identifier for the target chat or username of the target channel (in the format @channelusername).
            parse_mode (str, optional): Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your bot's message. Defaults to None.
            disable_web_page_preview (bool, optional): Disables link previews for links in this message. Defaults to False.
            disable_notification (bool, optional): Sends the message silently. iOS users will not receive a notification, Android users will receive a notification with no sound. Other apps coming soon. Defaults to False.
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message. Defaults to None.
            reply_markup (str, optional): reply markup. Defaults to None.
        Returns:
            dict: dict that can be accessed like an object.
        """
        api = telegram.endpoints + 'sendMessage'
        json_data = {"chat_id": chat_id, "text": text, "disable_web_page_preview":
                     disable_web_page_preview, "disable_notification": disable_notification}
        if parse_mode:
            json_data['parse_mode'] = parse_mode
        if reply_to_message_id:
            json_data["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            json_data["reply_markup"] = reply_markup
        ret = requests.post(api, json=json_data, verify=telegram.ssl_verify).json()
        return telegram.parse_response(ret)
    
    def send_document(chat_id, document, caption=None, disable_notification=False, reply_to_message_id=None):
        """
        Use this method to send general files.
        Args:
            document (str): File to send. You can either pass a file_id as String to resend a file that is already on the Telegram servers, or upload a new file by just passing the path to the file as String and the SDK will take care of uploading it for you.
            chat_id (str): Unique identifier for the target chat or username of the target channel (in the format @channelusername)
            caption (str, optional): Document caption (may also be used when resending documents by file_id), 0-200 characters. Default to None.
            disable_notification (bool, optional): Sends the message silently. iOS users will not receive a notification, Android users will receive a notification with no sound. Other apps coming soon. Defaults to False.
            reply_to_message_id (int, optional): If the message is a reply, ID of the original message. Defaults to None.
        Returns:
            dict: dict that can be accessed like an object.
        """
            
        api = telegram.endpoints + 'sendDocument'
        data = {
            "chat_id": chat_id,
            "reply_to_message_id": reply_to_message_id,
            "caption": caption,
            "disable_notification": disable_notification
        }
        try:
            files = {
                'document': (os.path.basename(document), open(document))
            }
            ret = requests.post(api, data=data, files=files, verify=telegram.ssl_verify).json()
        except BaseException as e:
            data["document"] = document
            ret = requests.post(api, json=data, verify=telegram.ssl_verify).json()
        return telegram.parse_response(ret)
        
    def send_chat_action(chat_id, action="typing"):
        """
        Args:
            chat_id (str): Unique identifier for the target chat or username of the target channel (in the format @channelusername)
            action (str, optional): Type of action to broadcast. Choose one, depending on what the user is about to receive: typing for text messages, upload_photo for photos, record_video or upload_video for videos, record_audio or upload_audio for audio files, upload_document for general files, find_location for location data. Defaults to "typing".
        Returns:
            dict: dict that can be accessed like an object.
        """
        api = telegram.endpoints + 'sendChatAction'
        payload = { "action": action}
        ret = requests.post(api, json=payload, verify=telegram.ssl_verify)
        return telegram.parse_response(ret)
        
    def get_file(file_id):
        """
        Use this method to get basic info about a file and prepare it for downloading.
        Args:
            file_id (int): File identifier to get info about
        Returns:
            dict: dict that can be accessed like an object.
        """
            
        api = telegram.endpoints + 'getFile?file_id=' + file_id
        ret = requests.get(api, verify=telegram.ssl_verify).json()
        return telegram.parse_response(ret)
    
    
    def download_file(file_path, local_path):
        """
        Use this method to download file from telegram.
        Args:
            file_path (str): telegram.get_file.file_path.
            local_path (str): Local dir with file name and file extension.
        Returns:
            bool: True if download succeeded.
            dict: dict that can be accessed like an object if download failed.
        """
        api = "https://api.telegram.org/file/bot"+telegram.token+"/"+file_path
        r = requests.get(api, verify=telegram.ssl_verify)
        try:
            return telegram.parse_response(r.json())
        except BaseException as e:
            if type(r.content) == str:
                with open(local_path, "w") as f:
                    f.write(r.content)
                return True
            else:
                with open(local_path, "wb") as f:
                    f.write(r.content)
                return True
        
        # below is the high level telegram api wrapper
        
        def reply_message(*args, **kwargs):
            """
            Use this method to quick reply with text message.
            """
            kwargs["chat_id"] = telegram.data.message.chat.id
            return telegram.send_message(*args, **kwargs)
            
        def reply_document(*args, **kwargs):
           """
           Use this method to quick reply with document.
           """
           kwargs["chat_id"] = telegram.data.message.chat.id
           return telegram.send_document(*args, **kwargs)