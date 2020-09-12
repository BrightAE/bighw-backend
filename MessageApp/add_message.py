from MessageApp.models import Message


def add_message(msg_type: str = 'all', from_id: int = 0, to_id: int = 0, title: str = 'default_title',
                content: str = 'default content'):
    new_message = Message()
    new_message.type = msg_type
    new_message.from_id = from_id
    new_message.to_id = to_id
    new_message.title = title
    new_message.content = content
    new_message.save()
