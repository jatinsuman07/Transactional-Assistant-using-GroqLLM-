import json
import datetime


DB_FILE = 'transaction_db.json'
COMPLAINT_FILE = 'transaction_issues.json'
NEW_ACC_NUM = 'new_account_numbers.json'

def create_or_load_db():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return generate_initial_db()

def generate_initial_db():
    db={
        "accounts":{
            000000:{
                "name":"Name",
                "balance":0,
                "insurance_amount":0,
                "history":[]
            }
        }
    }
    save_db(db)
    return db

def save_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)


def create_new_account(name):
    db = create_or_load_db()
    try:
        # Step 1: Load existing DB from file
        with open(NEW_ACC_NUM, 'r') as f:
            new_db = json.load(f)
    except FileNotFoundError:
        # If file doesn't exist, initialize
        new_db = {
            "acc_num": {"new": []},
            "accounts": {}
        }

    # Step 2: Check if any account number is available
    if not new_db.get("acc_num", {}).get("new"):
        return json.dumps({"error": "No available account numbers!"})

    # Step 3: Extract and remove the first account number
    account_number = new_db["acc_num"]["new"].pop(0)

    # Step 4: Add new account to 'accounts'
    db["accounts"][account_number] = {
        "name": name,
        "balance": 0,
        "insurance_amount": 0,
        "history": []
    }
    #save account file
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)


    # Step 5: Save updated DB back to file
    with open(NEW_ACC_NUM, 'w') as f:
        json.dump(new_db, f, indent=4)

    # Step 6: Return response
    return json.dumps({
        "success": "Account registered",
        "account_number": account_number
    })


    # Save the updated database (including updated acc_num list)
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

    return json.dumps({'success': 'account registered', 'account_number': account_number})


def check_balance(account_number):
    db = create_or_load_db()
    acc = db['accounts'].get(str(account_number))
    if acc:
        return json.dumps({'Balance': acc['balance']})
    return json.dumps({'error':'account not found'})

def credit_amount(account_number, amount):
    db = create_or_load_db()
    acc = db['accounts'].get(str(account_number))
    if acc:
        acc['balance']+=amount
        acc['history'].append({'type':'credit','amount':amount,'timestamp': str(datetime.datetime.now())})
        save_db(db)
        return json.dumps({'success': 'credit successful'})
    else:
        return json.dumps({'error':'account not found'})


def debit_amount(account_number , amount):
    db = create_or_load_db()
    acc = db['accounts'].get(str(account_number))
    if acc:
        if acc['balance']>=amount:
            acc['balance']-=amount
            acc['history'].append({'type':'debit','amount':amount,'timestamp':str(datetime.datetime.now())})
            save_db(db)
            return json.dumps({'success':'debited successfully'})
        return json.dumps({'error':'insufficient balance'})
    return json.dumps({'error':'account not found'})

def user_complaint(account_number, issue):
    issues = [{'account': account_number, 'complaint': issue, 'timestamp': str(datetime.datetime.now())}]  # list literal
    with open(COMPLAINT_FILE, 'w') as f:
        json.dump(issues, f, indent=4)
    return json.dumps({'success':'complaint registered'})

def pay_insurance(account_number):
    db = create_or_load_db()
    acc = db['accounts'].get(str(account_number))
    if acc:
        acc['balance'] -= acc['insurance_amount']
        acc['history'].append({'type':'insurance_deduction','amount':acc['insurance_amount'], 'timestamp':str(datetime.datetime.now())})
        save_db(db)
        return json.dumps({'success':'insurance deducted'})
    return json.dumps({'error':'account not found'})

def get_payment_history(account_number):
    db = create_or_load_db()
    acc = db['accounts'].get(str(account_number))
    if acc:
        return json.dumps({'history':acc['history']})
    return json.dumps({'error':'account not found'})






