from app import create_app, db

def init_db():
    """  
    Initialize the database and create the tables.
    """
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()

def migrate_db_tables():
    """
    Migrate the database to the latest version.
    """
    app = create_app()
    with app.app_context():
        db.create_all()
        db.session.commit()

if __name__ == '__main__':
    migrate_db_tables()