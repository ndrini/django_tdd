import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

# REPO_URL = 'https://github.com/ndrini/book-example.git'
REPO_URL = 'https://github.com/ndrini/django_tdd'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    # deploy in the server the same commit version in the local machine
    # equivalent of the git pull manually did	
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')
		
