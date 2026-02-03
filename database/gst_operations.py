from database.db import get_connection


def save_gst_transaction(gstin, amount, gst_rate, gst_amount, total_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO gst_transactions (gstin, amount, gst_rate, gst_amount, total_amount)
        VALUES (?, ?, ?, ?, ?)
    """, (gstin, amount, gst_rate, gst_amount, total_amount))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def save_gst_return(gstin, month, year, return_id, status="PENDING"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO gst_returns (gstin, month, year, return_id, status)
        VALUES (?, ?, ?, ?, ?)
    """, (gstin, month, year, return_id, status))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def save_late_fee(gstin, tax_amount, delay_days, late_fee):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO gst_late_fees (gstin, tax_amount, delay_days, late_fee)
        VALUES (?, ?, ?, ?)
    """, (gstin, tax_amount, delay_days, late_fee))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def fetch_transactions(gstin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gst_transactions WHERE gstin=?", (gstin,))
    results = cursor.fetchall()
    conn.close()
    return [dict(r) for r in results]

def fetch_gst_returns(gstin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gst_returns WHERE gstin=?", (gstin,))
    results = cursor.fetchall()
    conn.close()
    return [dict(r) for r in results]
