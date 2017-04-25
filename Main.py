#!/usr/bin/python3
#!python3
#encoding:utf-8
import os.path
import subprocess
import Data
import command.repository.Creator
import command.repository.Commiter
import command.repository.Deleter
import command.repository.Editor
import command.aggregate.Aggregate

class Main:
    def __init__(self, user_name, description, homepage, path_dir_pj, path_db_account, path_db_repo):
        self.data = Data.Data(user_name, description, homepage, path_dir_pj, path_db_account, path_db_repo)
        self.creator = command.repository.Creator.Creator(self.data)
        self.commiter = command.repository.Commiter.Commiter(self.data)
        self.deleter = command.repository.Deleter.Deleter(self.data)
        self.editor = command.repository.Editor.Editor(self.data)
        self.agg = command.aggregate.Aggregate.Aggregate(self.data)

    def Run(self):
        if -1 != self.__Create():
            self.__Commit()

    def __CreateInfo(self):
        print('ユーザ名: ' + self.data.get_username())
        print('メアド: ' + self.data.get_mail_address())
        print('SSH HOST: ' + self.data.get_ssh_host())
        print('リポジトリ名: ' + self.data.get_repo_name())
        print('説明: ' + self.data.get_repo_description())
        print('URL: ' + self.data.get_repo_homepage())
        print('リポジトリ情報は上記のとおりで間違いありませんか？[y/n]')

    def __Create(self):
        if os.path.exists(".git"):
            return 0
        answer = ''
        while '' == answer:
            self.__CreateInfo()
            answer = input()
            if 'y' == answer or 'Y' == answer:
                self.creator.Create()
                return 0
            elif 'n' == answer or 'N' == answer:
                print('call.shを編集して再度やり直してください。')
                return -1
            else:
                answer = ''

    def __CommitInfo(self):
        print('リポジトリ名： {0}/{1}'.format(self.data.get_username(), self.data.get_repo_name()))
        print('説明: ' + self.data.get_repo_description())
        print('URL: ' + self.data.get_repo_homepage())
        print('----------------------------------------')
        self.commiter.ShowCommitFiles()
        print('commit,pushするならメッセージを入力してください。Enterかnで終了します。')
        print('サブコマンド    n:終了 a:集計 e:編集 d:削除 i:Issue作成')

    def __Commit(self):
        while (True):
            self.__CommitInfo()
            answer = input()
            if '' == answer or 'n' == answer or 'N' == answer:
                print('終了します。')
                break
            elif 'a' == answer or 'A' == answer:
                self.agg.Show()
            elif 'e' == answer or 'E' == answer:
                self.__ConfirmEdit()
            elif 'd' == answer or 'D' == answer:
                self.__ConfirmDelete()
                break
            elif 'i' == answer or 'I' == answer:
                print('(Issue作成する。(未実装))')
            else:
                self.commiter.AddCommitPush(answer)
                self.agg.Show()

    def __ConfirmDelete(self):
        print('.gitディレクトリ、対象リモートリポジトリ、対象DBレコードを削除します。')
        print('リポジトリ名： {0}/{1}'.format(self.data.get_username(), self.data.get_repo_name()))
        self.deleter.ShowDeleteRecords()
        print('削除すると復元できません。本当に削除してよろしいですか？[y/n]')
        answer = input()
        if 'y' == answer or 'Y' == answer:
            self.deleter.Delete()
            print('削除しました。')
            return True
        else:
            print('削除を中止しました。')
            return False

    def __ConfirmEdit(self):
        print('編集したくない項目は無記入のままEnterキー押下してください。')

        print('リポジトリ名を入力してください。')
        name = input()
        if None is name or '' == name:
            # 名前は必須項目。変更しないなら現在の名前をセットする
            name = self.data.get_repo_name()
        print('説明文を入力してください。')
        description = input()
        print('Homepageを入力してください。')
        homepage = input()
        
        if '' == description and '' == homepage and self.data.get_repo_name() == name:
            print('編集する項目がないため中止します。')
        else:
            self.editor.Edit(name, description, homepage)
            print('編集しました。')
