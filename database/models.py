def create_tables(conn):
    cursor = conn.cursor()

    # GST Transactions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gst_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gstin TEXT NOT NULL,
        amount REAL NOT NULL,
        gst_rate REAL NOT NULL,
        gst_amount REAL NOT NULL,
        total_amount REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # GST Returns Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gst_returns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gstin TEXT NOT NULL,
        month TEXT NOT NULL,
        year INTEGER NOT NULL,
        return_id TEXT NOT NULL,
        status TEXT DEFAULT 'PENDING',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # GST Late Fees Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gst_late_fees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gstin TEXT NOT NULL,
        tax_amount REAL NOT NULL,
        delay_days INTEGER NOT NULL,
        late_fee REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    print("Tables created ✅")
