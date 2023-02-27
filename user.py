import uuid
from connection import get_connection

# Get database connection Object
db = get_connection()


# User class
class User:
    def __init__(self, first_name, last_name, email, id='', verified=True):
        # Main initialiser
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.id = uuid.uuid4().hex
        self.verified = verified

    def get_id(self):
        return str(self.email)

    @classmethod
    def make_from_dict(cls, d):
        # Initialise User object from a dictionary
        print("inside class+++++++{}".format(d['id']))
        return cls(d['first_name'], d['last_name'], d['email'], d['id'], d['verified'])

    def dict(self):
        # Return dictionary representation of the object
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "verified": self.verified
        }

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
