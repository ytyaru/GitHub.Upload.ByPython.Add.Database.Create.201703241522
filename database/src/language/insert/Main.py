import database.src.language.insert.LanguageSource
import database.src.language.insert.Inserter
class Main(object):
    def __init__(self, path_languages_sqlite3):
        self.source = database.src.language.insert.LanguageSource.LanguageSource()
        self.inserter = database.src.language.insert.Inserter.Inserter(path_languages_sqlite3)
    def Run(self):
        self.inserter.Insert(self.source.Get())

if __name__ == "__main__":    
    m = Main()
    m.Run()

