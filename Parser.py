import threading
import Config
from PageLoader import *
import TelegramBot
import sqlite3


class Parser:
    iter = 1
    def __init__(self) -> None:
        CreateTable = ("""CREATE TABLE IF NOT EXISTS Cars(
            idCars INTEGER NOT NULL,
            Link TEXT,
            PRIMARY KEY(idCars))""")
        DBConnection = sqlite3.connect('cars.db')
        DB = DBConnection.cursor()

        DB.execute(CreateTable)
        DBConnection.commit()

        self.NewLinks = []
        self.Link = Config.LINK

    def isNewCar(self, Link) -> bool:
        DBConnection = sqlite3.connect('cars.db')
        DB = DBConnection.cursor()
        row = DB.execute(f"SELECT idCars FROM Cars WHERE Link = '{Link}'")
        return row.fetchone() is None

    def Parse(self) -> None:
        print(f"Iteration {self.iter}")
        self.iter += 1        
        pl = PageLoader(self.Link)
        self.Links = pl.getCarLinks()
        
        DBConnection = sqlite3.connect('cars.db')
        DB = DBConnection.cursor()

        for link in self.Links:
            if self.isNewCar(link):
                TelegramBot.SendCar(link)
                DB.execute(f"INSERT INTO Cars(Link) VALUES ('{link}')")
                DBConnection.commit()
        threading.Timer(Config.UPDATE_TIME * 60, self.Parse).start()

def main():
    parser = Parser()
    parser.Parse()
    TelegramBot.main()

if __name__ == '__main__':
    main()
