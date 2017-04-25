#!python3
#encoding:utf-8
import subprocess
import shlex
import shutil
import os.path
import getpass
import database.src.language.insert.Main
import database.src.gnu_license.create.Main
import database.src.gnu_license.insert.main
import database.src.license.insert.Main
import database.src.other_repo.insert.Main
import database.src.account.Main
import database.src.api.Main
import database.src.repo.insert.Main
class InitializeMasterDbCreator:
    def __init__(self, db_dir_path):
        self.path_dir_db = db_dir_path
        self.path_dir_this = os.path.abspath(os.path.dirname(__file__))
        self.db_files = [
#            'GitHub.Languages.sqlite3': CreateLanguage,
#            'GitHub.Licenses.sqlite3': self.CreateLicenses,
            {'FileName': 'GitHub.Languages.sqlite3', 'Creator': self.__CreateLanguages, 'Inserter': self.__InsertLanguages},
            {'FileName': 'GNU.Licenses.sqlite3', 'Creator': self.__CreateGnuLicenses, 'Inserter': self.__InsertGnuLicenses},
            {'FileName': 'GitHub.Licenses.sqlite3', 'Creator': self.__CreateLicenses, 'Inserter': self.__InsertLicenses},
            {'FileName': 'GitHub.Repositories.__other__.sqlite3', 'Creator': self.__CreateOtherRepo, 'Inserter': self.__InsertOtherRepo},
            {'FileName': 'GitHub.Accounts.sqlite3', 'Creator': self.__CreateAccounts, 'Inserter': self.__InsertAccounts},
            {'FileName': 'GitHub.Apis.sqlite3', 'Creator': self.__CreateApis, 'Inserter': self.__InsertApis},
            {'FileName': 'GitHub.Repositories.{user}.sqlite3', 'Creator': self.__CreateRepo, 'Inserter': self.__InsertRepo},
#            'GitHub.Accounts.sqlite3': CreateAccounts,
#            'GitHub.Repositories.{user}.sqlite3': CreateRepositories,
#            'GitHub.Repositories.__other__.sqlite3': CreateOtherRepositories,
#            'GNU.Licenses.sqlite3': CreateGnuLicenses,
#            'GitHub.Api.sqlite3': CreateApi
        ]
        self.__Setup()

    def Run(self):
        if not(os.path.isdir(self.path_dir_db)):
            print('DBディレクトリを作る----------------')
            os.mkdir(self.path_dir_db)
        for db in self.db_files:
            db_path = os.path.join(self.path_dir_db, db['FileName'])
            if 'GitHub.Repositories.{user}.sqlite3' == db['FileName']:
                if not(os.path.isfile(db_path)):
                    db['Creator'](db_path)
                db_path_new = db_path.replace("{user}", self.github_user_name)
                if not(os.path.isfile(db_path_new)):
                    shutil.copyfile(db_path, db_path_new)
                    db['Inserter'](db_path_new)
            else:
                if not(os.path.isfile(db_path)):
                    print('DBファイルを作る: {0} ----------------'.format(db_path))
                    db['Creator'](db_path)
                    db['Inserter'](db_path)

    def __CreateApis(self, db_path):
        a = database.src.api.Main.Main(db_path)
        a.Run()
#        path_dir = os.path.join(self.path_dir_this, "api/res/sql/create/")
#        subprocess.call(shlex.split("sqlite3 \"{0}\" < \"{1}\"".format(db_path, os.path.join(path_dir, "Apis.sql"))))

    def __InsertApis(self, db_path):
#        path_dir = os.path.join(self.path_dir_this, "api/res/sql/insert/")
#        subprocess.call(shlex.split("sqlite3 \"{0}\" < \"{1}\"".format(db_path, os.path.join(path_dir, "Apis.sql"))))
        pass

    def __CreateRepo(self, db_path):
        subprocess.call(shlex.split("bash ./repo/create/Create.sh \"{0}\"".format(db_path)))

    def __InsertRepo(self, db_path):
        m = database.src.repo.insert.Main.Main(self.github_user_name, self.path_db_account, db_path, self.path_db_license, self.path_db_api)
        m.Initialize()

    def __CreateAccounts(self, db_path):
        a = database.src.account.Main.Main(db_path)
        a.Run()
#        path_dir = os.path.join(self.path_dir_this, "account/res/sql/create/")
#        subprocess.call(shlex.split("sqlite3 \"{0}\" < \"{1}\"".format(db_path, os.path.join(path_dir, "Accounts.sql"))))
#        subprocess.call(shlex.split("sqlite3 \"{0}\" < \"{1}\"".format(db_path, os.path.join(path_dir, "TwoFactors.sql"))))
#        subprocess.call(shlex.split("sqlite3 \"{0}\" < \"{1}\"".format(db_path, os.path.join(path_dir, "AccessTokens.sql"))))

    def __InsertAccounts(self, db_path):
        pass
#        path_dir = os.path.join(self.path_dir_this, "account/res/sql/insert/")
#        subprocess.call(shlex.split("sqlite3 \"{0}\" < \"{1}\"".format(db_path, os.path.join(path_dir, "Accounts.sql"))))
#        subprocess.call(shlex.split("sqlite3 \"{0}\" < \"{1}\"".format(db_path, os.path.join(path_dir, "TwoFactors.sql"))))
#        subprocess.call(shlex.split("sqlite3 \"{0}\" < \"{1}\"".format(db_path, os.path.join(path_dir, "AccessTokens.sql"))))

    def __CreateOtherRepo(self, db_path):
        subprocess.call(shlex.split("bash ./other_repo/create/Create.sh \"{0}\"".format(db_path)))

    def __InsertOtherRepo(self, db_path):
        path_db_license = os.path.join(self.path_dir_db, "GitHub.Licenses.sqlite3")
        print(path_db_license)
        main = database.src.other_repo.insert.Main.Main(self.github_user_name, self.path_db_account, db_path, path_db_license)
        main.Initialize()

    def __CreateLanguages(self, db_path):
        subprocess.call(shlex.split("bash ./language/create/Create.sh \"{0}\"".format(db_path)))

    def __InsertLanguages(self, db_path):
        creator_language = database.src.language.insert.Main.Main(db_path)
        creator_language.Run()

    def __CreateGnuLicenses(self, db_path):
        creator_language = database.src.gnu_license.create.Main.Main(db_path)
        creator_language.Run()

    def __InsertGnuLicenses(self, db_path):
        creator_gnu_license = database.src.gnu_license.insert.main.GnuSite(db_path)
        creator_gnu_license.GetAll()

    def __CreateLicenses(self, db_path):
        subprocess.call(shlex.split("bash ./license/create/Create.sh \"{0}\"".format(db_path)))

    def __InsertLicenses(self, db_path):
#        creator_license = self.__LicenseCreator(db_path)
        creator_license = database.src.license.insert.Main.Main(self.github_user_name, self.path_db_account, self.path_db_repo, db_path)
        creator_license.Initialize()
    """
    def __LicenseCreator(self, db_path):
        github_user_name = 'ytyaru'
        os_user_name = getpass.getuser()
        device_name = '85f78c06-a96e-4020-ac36-9419b7e456db'
        path_db_base = 'mint/root/db/Account/GitHub'
        path_db_account = '/media/{0}/{1}/{2}/private/v0/GitHub.Accounts.sqlite3'.format(os_user_name, device_name, path_db_base)
        path_db_repo = '/media/{0}/{1}/{2}/public/v0/GitHub.Repositories.{3}.sqlite3'.format(os_user_name, device_name, path_db_base, github_user_name)
        return license.insert.Main.Main(github_user_name, path_db_account, path_db_repo, db_path)
    """
    def __Setup(self):
        self.github_user_name = 'ytyaru'
        os_user_name = getpass.getuser()
        device_name = '85f78c06-a96e-4020-ac36-9419b7e456db'
        path_db_base = 'mint/root/db/Account/GitHub'
        self.path_db_account = '/media/{0}/{1}/{2}/private/v0/GitHub.Accounts.sqlite3'.format(os_user_name, device_name, path_db_base)
        self.path_db_repo = '/media/{0}/{1}/{2}/public/v0/GitHub.Repositories.{3}.sqlite3'.format(os_user_name, device_name, path_db_base, self.github_user_name)
        self.path_db_license = '/media/{0}/{1}/{2}/public/v0/GitHub.Licenses.sqlite3'.format(os_user_name, device_name, path_db_base)
        self.path_db_api = '/media/{0}/{1}/{2}/public/v0/GitHub.Apis.sqlite3'.format(os_user_name, device_name, path_db_base)

