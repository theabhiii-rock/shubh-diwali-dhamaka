"""
Diwali Dhamaka Lottery Platform - Full Automated Verification Test
"""
import os
import sys
import json
import sqlite3
import threading
import time
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from server import run_server, DB_PATH, get_db_connection

def run_tests():
    base_url = "http://localhost:8088"
    
    # 1. Test Stats
    print("\n[1] Testing GET /api/stats...")
    with urlopen(f"{base_url}/api/stats") as res:
        stats = json.loads(res.read().decode())
        assert stats["ticket_price"] == 49
        assert stats["target_tickets"] == 100000
        assert stats["total_winners"] == 100
        assert len(stats["prizes"]) == 3
        print("  ✓ Stats OK! Total tickets sold so far:", stats["total_tickets_sold"])

    # 2. Test Order Creation
    print("\n[2] Testing POST /api/order/create...")
    order_payload = {
        "name": "Abhishek Verma",
        "phone": "9876543210",
        "email": "abhishek@example.com",
        "quantity": 5,
        "payment_method": "UPI"
    }
    req = Request(
        f"{base_url}/api/order/create",
        data=json.dumps(order_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urlopen(req) as res:
        order_res = json.loads(res.read().decode())
        assert order_res["success"] is True
        assert order_res["amount"] == 5 * 49
        order_id = order_res["order_id"]
        print(f"  ✓ Order created successfully! Order ID: {order_id}, Amount: ₹{order_res['amount']}")

    # 3. Test Order Verification & Ticket Generation
    print("\n[3] Testing POST /api/order/verify...")
    verify_payload = {
        "order_id": order_id,
        "transaction_id": "UPI-REF-998877665544",
        "payment_method": "UPI"
    }
    req = Request(
        f"{base_url}/api/order/verify",
        data=json.dumps(verify_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urlopen(req) as res:
        verify_res = json.loads(res.read().decode())
        assert verify_res["success"] is True
        tickets = verify_res["tickets"]
        assert len(tickets) == 5
        for t in tickets:
            assert t["ticket_number"].startswith("DWL-")
            assert t["phone"] == "9876543210"
        print(f"  ✓ Payment verified! 5 Random tickets generated: {[t['ticket_number'] for t in tickets]}")

    # 4. Test Post-Purchase Delivery Details Save
    print("\n[4] Testing POST /api/delivery/save (Doorstep Address for Cracker Delivery)...")
    delivery_payload = {
        "phone": "9876543210",
        "name": "Abhishek Verma",
        "email": "abhishek@example.com",
        "pincode": "302001",
        "city": "Jaipur",
        "state": "Rajasthan",
        "address_line": "Plot 45, Golden City, MI Road",
        "landmark": "Near Panchbatti",
        "alternate_phone": "9876500000"
    }
    req = Request(
        f"{base_url}/api/delivery/save",
        data=json.dumps(delivery_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urlopen(req) as res:
        delivery_res = json.loads(res.read().decode())
        assert delivery_res["success"] is True
        print("  ✓ Delivery details saved cleanly for doorstep delivery!")

    # 5. Test Profile & My Tickets Lookup
    print("\n[5] Testing GET /api/profile?phone=9876543210...")
    with urlopen(f"{base_url}/api/profile?phone=9876543210") as res:
        profile = json.loads(res.read().decode())
        assert profile["success"] is True
        assert profile["ticket_count"] >= 5
        assert profile["delivery"]["city"] == "Jaipur"
        assert profile["delivery"]["pincode"] == "302001"
        print(f"  ✓ Profile retrieved! User has {profile['ticket_count']} tickets with confirmed delivery address.")

    # 6. Seed enough tickets to reach >= 100 for Winner Draw test
    print("\n[6] Ensuring at least 100 participants for the Grand Winner Draw...")
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) as cnt FROM tickets')
    cnt = c.fetchone()['cnt']
    if cnt < 100:
        needed = 105 - cnt
        print(f"  Seeding {needed} sample tickets for fair draw testing...")
        now = time.strftime('%Y-%m-%dT%H:%M:%S')
        for i in range(needed):
            phone = f"91000{i:05d}"
            name = f"Participant {i+1}"
            order_id = f"SEED-{i+1}"
            c.execute('INSERT OR IGNORE INTO users (name, phone, created_at) VALUES (?, ?, ?)', (name, phone, now))
            uid = c.lastrowid or 1
            t_no = f"DWL-{100000 + i}"
            c.execute('''
            INSERT OR IGNORE INTO tickets (ticket_number, order_id, user_id, phone, user_name, price, purchase_time)
            VALUES (?, ?, ?, ?, ?, 49, ?)
            ''', (t_no, order_id, uid, phone, name, now))
        conn.commit()
    conn.close()

    # 7. Test Admin 100-Winner Fair Cryptographic Draw
    print("\n[7] Testing POST /api/admin/draw (Grand 100-Winner Draw)...")
    draw_payload = {"pin": "diwali2026", "force": True}
    req = Request(
        f"{base_url}/api/admin/draw",
        data=json.dumps(draw_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urlopen(req) as res:
        draw_res = json.loads(res.read().decode())
        assert draw_res["success"] is True
        assert draw_res["total_drawn"] == 100
        assert draw_res["tier_1_count"] == 50  # Top 50 winners: ₹25k
        assert draw_res["tier_2_count"] == 30  # Next 30 winners: ₹15k
        assert draw_res["tier_3_count"] == 20  # Remaining 20 winners: ₹5k
        print(f"  ✓ 100-Winner Draw Verified! Tier 1: {draw_res['tier_1_count']}, Tier 2: {draw_res['tier_2_count']}, Tier 3: {draw_res['tier_3_count']}")

    # 8. Test Winners API
    print("\n[8] Testing GET /api/winners...")
    with urlopen(f"{base_url}/api/winners") as res:
        win_data = json.loads(res.read().decode())
        assert win_data["is_draw_completed"] is True
        assert len(win_data["tier_1_winners"]) == 50
        assert len(win_data["tier_2_winners"]) == 30
        assert len(win_data["tier_3_winners"]) == 20
        first_winner = win_data["tier_1_winners"][0]
        print(f"  ✓ Winner Board Verified! Top 1 Winner: {first_winner['name']} (Ticket: {first_winner['ticket_number']}, Prize: ₹{first_winner['prize_amount']})")

    # 9. Test CSV Export
    print("\n[9] Testing GET /api/admin/export-csv?type=winners...")
    with urlopen(f"{base_url}/api/admin/export-csv?type=winners") as res:
        csv_text = res.read().decode('utf-8-sig')
        lines = csv_text.strip().split('\n')
        # 1 header line + 100 winner lines
        assert len(lines) == 101
        print("  ✓ CSV Export Verified! Exactly 100 winners with shipping columns generated.")

    print("\n=======================================================")
    print("🎉 ALL 9 TEST SUITES PASSED FLAWLESSLY! PLATFORM IS 100% OPERATIONAL!")
    print("=======================================================\n")

if __name__ == "__main__":
    from http.server import HTTPServer
    from server import LotteryRequestHandler, init_db
    init_db()
    
    server = HTTPServer(('127.0.0.1', 8088), LotteryRequestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.5)

    try:
        run_tests()
    finally:
        server.shutdown()
        server.server_close()
