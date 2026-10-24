import sqlite3

DATABASE_NAME = "tracker.db"
STAGES = ["Saved","Applied", "Online Assessments", "Virtual Interview/Phone Interview", "Assessment Centre", "Offer", "Rejected"]

def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def database_setup():
    conn = create_database()
    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        location TEXT,
        dateopened TEXT,
        dateclosing TEXT,
        link TEXT,
        stages TEXT NOT NULL DEFAULT 'Saved',
        notes TEXT
        )
        """
    )
    conn.commit()
    conn.close() 


def add_application(company, role, location, dateopened, dateclosing, link, stages, notes):
    conn = create_database()
    ## ? placeholder values to prevent SQL injection attacks
    cursor = conn.execute(
        """
        INSERT INTO applications (company, role, location, dateopened, dateclosing, link, stages, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
        """,
        (company, role, location, dateopened, dateclosing, link, stages, notes)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def get_all_applications():
    conn = create_database()
    rows = conn.execute(
        " SELECT * FROM applications"
        " ORDER BY dateopened DESC").fetchall()
    conn.close()
    return rows
def get_application_by_id(application_id):
    conn = create_database()
    row = conn.execute("SELECT * FROM applications WHERE id = ?", (application_id,)).fetchone()
    conn.close()
    return row

def edit_application(application_id, company, role, location, dateopened, dateclosing, link, stages, notes):
    conn = create_database()
    conn.execute(
        "UPDATE applications SET company = ?, role = ?, location = ?, dateopened = ?, dateclosing = ?, link = ?, stages = ?, notes = ? WHERE id = ?",
        (company, role, location, dateopened, dateclosing, link, stages, notes, application_id),
    )
    conn.commit()
    conn.close()

def delete_application(application_id):
    conn = create_database()
    conn.execute("DELETE FROM applications WHERE id = ?", (application_id,))
    conn.commit()
    conn.close()
