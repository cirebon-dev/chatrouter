# -*-coding:utf8;-*-
import chatrouter


chatbot = chatrouter.group("main")


@chatbot.add_command("show my id")
def show_handler():
    message = chatrouter.data_user
    return message.from_user.id
