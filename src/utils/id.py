from uuid import uuid4

def generate_id():
    return uuid4().__str__()