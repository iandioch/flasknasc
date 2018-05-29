from flask import Flask

app = Flask(__name__)


class User:
    users = {}

    def __init__(self, prefix, key):
        if prefix in User.users:
            raise RuntimeError(
                'User already exists with prefix {}'.format(prefix))
        self.prefix = prefix
        self.key = key
        self.links = {}

        User.users[prefix] = self

    @staticmethod
    def get_url(prefix, link_id):
        if prefix not in User.users:
            raise RuntimeError('No such user prefix {}'.format(prefix))
        user = User.users[prefix]
        if link_id not in user.links:
            raise RuntimeError(
                'User has no link with given id {}'.format(link_id))
        return user.links[link_id]


@app.route('/')
def root():
    return 'hello world'


if __name__ == '__main__':
    app.run()
