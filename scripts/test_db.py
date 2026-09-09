import psycopg

hostname = "localhost"
database = "placement_mail"
username = "postgres"
pwd = "gmail"
port_id = 5432
conn = None
cur = None

try:
    conn = psycopg.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    cur = conn.cursor()
    create_script = '''
                    CREATE TABLE IF NOT EXISTS emails (
                        message_id VARCHAR(255) PRIMARY KEY,
                        thread_id VARCHAR(255), 
                        subject VARCHAR(255),
                        sender VARCHAR(255),
                        email_body TEXT,
                        received_datetime TIMESTAMP
                    );
                    CREATE TABLE IF NOT EXISTS attachments (
                        attachment_id VARCHAR(255) PRIMARY KEY,
                        message_id VARCHAR(255) REFERENCES emails(message_id) ON DELETE CASCADE,
                        file_name VARCHAR(255),
                        file_type VARCHAR(50),
                        file_url VARCHAR(512) 
                    );
                    '''
    cur.execute(create_script)
    conn.commit()
    print("Table successfully created with a foreign key linkage")
    
    

except Exception as e:
    print(e)
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()