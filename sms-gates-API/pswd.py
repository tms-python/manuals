import random
char_collection = [
            'QWERTYUPASDFGHJKLZXCVBNM',
            'qwertyuipasdfghjkzxcvbnm',
            '123456789',
            '!#$%',
        ]


def generate_password(char_count):
    def select_random_char(el):
        return el[random.randrange(0, len(el))]
    return ''.join(
        [
            select_random_char(char_collection[random.randrange(4)])
            for el in range(int(char_count))
        ]
    )


def verification_password(entered_password, char_count=10):
    def verify_part_of_collection(elements):
        for char in elements:
            if char in entered_password:
                return True
            else:
                continue
        return False
    if len(entered_password) >= char_count:
        for elements in char_collection:
            if verify_part_of_collection(elements):
                continue
            else:
                return verification_password(generate_password(char_count))
        return entered_password
    else:
        return verification_password(generate_password(char_count))
