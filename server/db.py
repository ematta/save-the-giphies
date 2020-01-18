from save_the_giphies.database.engine import init_db, drop_db

if __name__ == '__main__':
    """ Simple tool to help us recreate the DB (TODO: Build this out) """
    try:
        drop_db()
        init_db()
        print("Recreated")
    except Exception as e:
        print(e)
