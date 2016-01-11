__author__ = 'brianyang'

from fabric.api import local, settings, abort, cd, run, env, lcd
from fabric.contrib.console import confirm
from fabric.network import ssh

ssh.util.log_to_file("paramiko.log", 10)

env.hosts = ['52.76.137.215']
env.user = 'ubuntu'
env.key_filename = "~/Documents/why.pem"


def commit_code():
    code_dir = "/home/q/blog"
    with settings(warn_only=True):
        with lcd(code_dir):
            result = local("git pull origin master")
            if result.failed and not confirm("Pull failed, continue?"):
                abort("abort!")
            local("git add .")
            local("git commit -m 'auto commit'")
            local("git push origin master")


def deploy_server():
    code_dir = "/home/q/blog"
    with settings(warn_only=True):
        with cd(code_dir):
            run("sudo git pull origin master")
            result = run("sudo uwsgi --ini conf/uwsgi.conf  --reload pidfile")
            if result.failed:
                run("sudo ps -ef|grep uwsgi")
                run("""sudo ps -ef|grep "\-\-ini conf/uwsgi.conf"|awk -F ' ' '{print $2}'|xargs sudo kill -9""")
                result = run("sudo uwsgi --ini conf/uwsgi.conf")
                if result.failed:
                    print "launch failed"


def deploy():
    commit_code()
    deploy_server()