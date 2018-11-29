from fabric import task
import time

@task
def build_application(c):
    """ Build the local package & deploy this to the server. """

    # create python package
    c.local('python setup.py sdist --formats=gztar')

    filename = '{}.tar.gz'.format(c.local('python setup.py --fullname').stdout.strip())

    application_folder = c.local('python setup.py --name').stdout.strip().lower()
    usergroup = \
    username = 'www-{}'.format(application_folder)

    # upload package to server
    c.put('dist/{}'.format(filename), '/tmp/{}'.format(filename))

    # first deployment (folder not found)
    if c.run('if [ -d "/var/www/{}" ]; then echo 1; else echo 0; fi'
                     .format(application_folder)).stdout.strip() == '0':

        # create user
        c.run('useradd -r -M -U -s /sbin/nologin {}'.format(username))

        # create folder
        c.run('mkdir /var/www/{}'.format(application_folder))

        # create virtual env
        c.run('python3 -m venv /var/www/{}/env'.format(application_folder))

        # update pip
        c.run('/var/www/{}/env/bin/pip install --upgrade pip'.format(application_folder))

        # upload the config files
        c.put('config/config.ini', '/var/www/{}'.format(application_folder))

        # update the uwsgi configuration (symlink based on template.ini)
        #c.run('ln -s /etc/uwsgi/apps-available/template.ini /etc/uwsgi/vassals/{}.ini'.format(application_folder))

        # create the ngix config (use template to create new config)
        #c.run('sed -e s/%n/{0}/g /etc/nginx/applications-available/template > /etc/nginx/applications-available/{0}'
        #      .format(application_folder))

        # link the config
        #c.run('ln -s /etc/nginx/applications-available/{0} /etc/nginx/applications-enabled/{0}'
        #      .format(application_folder))

    # install application in venv
    c.run('/var/www/{}/env/bin/pip install /tmp/{}'.format(application_folder, filename))

    # change ownership
    c.run('chown -R {}:{} /var/www/{}'.format(username, usergroup, application_folder))

    # reload uwsgi
    #c.run('touch /etc/uwsgi/vassals/{}.ini'.format(application_folder))

    # reload config
    #c.run('nginx -s reload')


@task
def cleanup_application(c):
    """ Delete the package from the server & remove the config files. """

    application_folder = c.local('python setup.py --name').stdout.strip().lower()
    username = 'www-{}'.format(application_folder)

    # delete symlink
    c.run('unlink /etc/uwsgi/vassals/{}.ini'.format(application_folder), warn=True)

    # wait until application is shut down by the emperor
    time.sleep(5)

    # delete folders
    c.run('rm -r /var/www/{}'.format(application_folder), warn=True)

    # delete users
    c.run('userdel {}'.format(username), warn=True)

    # delete ngix config
    c.run('unlink /etc/nginx/applications-enabled/{}'.format(application_folder), warn=True)
    c.run('rm /etc/nginx/applications-available/{}'.format(application_folder), warn=True)

    # reload config
    c.run('nginx -s reload', warn=True)