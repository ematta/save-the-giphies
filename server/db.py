from save_the_giphies.database.engine import init_db, drop_db

if __name__ == '__main__':
    drop_db()
    init_db()
