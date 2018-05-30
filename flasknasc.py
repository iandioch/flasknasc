import json
import random
import string

from pathlib import Path

from flask import Flask, redirect, request

app = Flask(__name__)

ROOT_PATH = Path('.flasknasc')
CONFIG_FILE_PATH = ROOT_PATH / 'config.json'


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

    def save_urls(self, root_path_obj):
        user_dir = root_path_obj / self.prefix
        if not user_dir.exists():
            print('Creating user directory for prefix {}'.format(self.prefix))
            user_dir.mkdir(parents=True)
        links_file = user_dir / 'links.json'
        data = {
            'links': []
        }
        for link in self.links:
            data['links'].append({
                'id': link,
                'address': self.links[link]
            })
        with links_file.open(mode='w') as f:
            json.dump(data, f)

    @staticmethod
    def get_url(prefix, link_id):
        if prefix not in User.users:
            raise RuntimeError('No such user prefix {}'.format(prefix))
        user = User.users[prefix]
        if link_id not in user.links:
            raise RuntimeError(
                'User has no link with given id {}'.format(link_id))
        return user.links[link_id]

    @staticmethod
    def new_url(prefix, key, link_id, address):
        if prefix not in User.users:
            raise RuntimeError('No such user prefix {}'.format(prefix))
        user = User.users[prefix]
        if key != user.key:
            raise RuntimeError('Key does not match')
        if link_id in user.links:
            raise RuntimeError('Link already exists with this ID')
        user.links[link_id] = address
        user.save_urls(ROOT_PATH)


def load_config_file(path):
    with path.open() as f:
        data = json.load(f)
        if 'users' in data:
            for user in data['users']:
                prefix = user['prefix']
                key = user['key']
                user_obj = User(prefix, key)
                user_obj.load_saved_urls(ROOT_PATH)
        return data

def generate_random_id(length=12):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.route('/')
def root():
    return 'hello world'


@app.route('/fwd/<string:user_prefix>/<string:link_id>')
def route_fwd(user_prefix, link_id):
    try:
        return redirect(User.get_url(user_prefix, link_id))
    except Exception as e:
        return str(e)


@app.route('/new/<string:user_prefix>/<string:link_id>')
def route_new(user_prefix, link_id):
    try:
        key = request.args.get('key')
        address = request.args.get('address')
        User.new_url(user_prefix, key, link_id, address)
        print(f'new link: /fwd/{user_prefix}/{link_id} -> {address}')
        return f'/fwd/{user_prefix}/{link_id}'
    except Exception as e:
        return str(e)

@app.route('/new/<string:user_prefix>')
def route_new_random_id(user_prefix):
    try:
        link_id = generate_random_id()
        key = request.args.get('key')
        address = request.args.get('address')
        User.new_url(user_prefix, key, link_id, address)
        print(f'new link: /fwd/{user_prefix}/{link_id} -> {address}')
        return f'/fwd/{user_prefix}/{link_id}'
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    config = load_config_file(CONFIG_FILE_PATH)
    port = int(config.get('port', 5821))
    host = config.get('host', '0.0.0.0')
    debug = config.get('debug', True)
    app.run(host=host, port=port, debug=debug)
