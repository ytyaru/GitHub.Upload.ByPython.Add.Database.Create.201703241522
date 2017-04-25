#!/usr/bin/python3
#!python3
#encoding:utf-8
import sys
import os.path
import subprocess
import configparser
import argparse
import database.src.Create
import uploader.Main

class Main:
    def __init__(self):
        pass

    def Run(self):
#    def Run(self, path_dir_pj, user_name=None, description=None, homepage=None):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        path_db = os.path.abspath(config['Path']['DB'])
        print(path_db)
        creator = database.src.Create.InitializeMasterDbCreator(path_db)
        creator.Run()

        parser = argparse.ArgumentParser(
            description='GitHub Repository Uploader.',
#            usage='$ hup `pwd`'
        )
        parser.add_argument('path_dir_pj')
        parser.add_argument('-u', '--username')
        parser.add_argument('-d', '--description')
        parser.add_argument('-l', '--homepage', '--link', '--url')
        args = parser.parse_args()
        print(args)
        print('path_dir_pj: {0}'.format(args.path_dir_pj))
        print('-u: {0}'.format(args.username))
        print('-d: {0}'.format(args.description))
        print('-l: {0}'.format(args.homepage))

        if None is args.username:
            args.username = config['GitHub']['User']
            print('default-username: {0}'.format(args.username))
        print(os.path.join(path_db, 'GitHub.Accounts.sqlite3'))
        print(os.path.join(path_db, 'GitHub.Repositories.{0}.sqlite3'.format(args.username)))
        main = uploader.Main.Main(args.username, args.description, args.homepage, args.path_dir_pj, 
                os.path.join(path_db, 'GitHub.Accounts.sqlite3'), 
                os.path.join(path_db, 'GitHub.Repositories.{0}.sqlite3'.format(args.username))
        )
        main.Run()


if __name__ == '__main__':
    main = Main()
    main.Run()
