from database.db import get_connection

def calculate_gst(user_id, amount, rate):
    gst_amount = amount * rate / 100
    total = amount + gst_amount

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO gst_calculations (user_id, amount, gst_rate, gst_amount, total)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, amount, rate, gst_amount, total))

    conn.commit()
    conn.close()

    return {
        "amount": amount,
        "gst_rate": rate,
        "gst_amount": gst_amount,
        "total": total
    }


def get_gst_liability(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT amount, gst_rate, gst_amount, total, created_at
        FROM gst_calculations
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 10
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()

    return rows
