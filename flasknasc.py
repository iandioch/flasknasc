import json

from pathlib import Path

from flask import Flask, redirect

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

    def load_saved_urls(self, root_path_obj):
        user_dir = root_path_obj / self.prefix
        if not (user_dir.exists() and user_dir.is_dir()):
            print('No user directory for user with prefix {}'.format(self.prefix))
            return
        links_file = user_dir / 'links.json'
        if not links_file.exists():
            print('User link file does not exist for user prefix {}'.format(self.prefix))
            return
        with links_file.open() as f:
            data = json.load(f)
            for link in data['links']:
                self.links[link['id']] = link['address']

    @staticmethod
    def get_url(prefix, link_id):
        if prefix not in User.users:
            raise RuntimeError('No such user prefix {}'.format(prefix))
        user = User.users[prefix]
        if link_id not in user.links:
            raise RuntimeError(
                'User has no link with given id {}'.format(link_id))
        return user.links[link_id]


def load_config_file(path):
    with open(path) as f:
        data = json.load(f)
        if 'users' in data:
            for user in data['users']:
                prefix = user['prefix']
                key = user['key']
                user_obj = User(prefix, key)
                user_obj.load_saved_urls(Path('.flasknasc'))


@app.route('/')
def root():
    return 'hello world'


@app.route('/fwd/<string:user_prefix>/<string:link_id>')
def url(user_prefix, link_id):
    try:
        return redirect(User.get_url(user_prefix, link_id))
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    load_config_file('flasknasc_config.json')
    app.run()
