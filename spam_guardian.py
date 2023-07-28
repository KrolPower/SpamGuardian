import imaplib
import smtplib
import email
import json
import time
import logging

# Load credentials from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

# IMAP settings
IMAP_SERVER = config['imap_server']
IMAP_USERNAME = config['imap_username']
IMAP_PASSWORD = config['imap_password']
IMAP_MAILBOX = config['imap_mailbox']

# SMTP settings - Set the SMTP variables equal to the IMAP variables
SMTP_SERVER = IMAP_SERVER
SMTP_PORT = config['smtp_port']
SMTP_USERNAME = IMAP_USERNAME
SMTP_PASSWORD = IMAP_PASSWORD

# List of target emails to monitor
TARGET_EMAILS = config['target_emails']

# Subject line for the automated response emails
with open('email_subject.txt', 'r') as subject_file:
    EMAIL_SUBJECT = subject_file.read().strip()

# Number of emails to send each time
NUM_EMAILS_TO_SEND = config['count']

# Configure logging
logging.basicConfig(filename='email_spam.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to send a single email
def send_email(target_email):
    try:
        # Connect to the SMTP server
        smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_server.starttls()
        smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)

        # Read the email body from file
        with open('email_body.txt', 'r') as body_file:
            email_body = body_file.read().strip()

        # Send the specified number of emails to the target person
        for _ in range(NUM_EMAILS_TO_SEND + 1):
            message = f'Subject: {EMAIL_SUBJECT}\n\n{email_body}'
            smtp_server.sendmail(SMTP_USERNAME, target_email, message.encode('utf-8'))

        smtp_server.quit()

        email_count = get_emails_count(target_email)
        logging.info(f'{email_count} emails found from {target_email}. \n{NUM_EMAILS_TO_SEND} emails sent to {target_email}.')
        print(f'{email_count} emails found from {target_email}. \n{NUM_EMAILS_TO_SEND} emails sent to {target_email}.')

    except Exception as e:
        logging.error(f'Failed to send emails to {target_email}: {str(e)}')
        print(f'Failed to send emails to {target_email}: {str(e)}')
        return False

    return True

# Retrieve the count of emails from a target person
def get_emails_count(target_email):
    try:
        # Connect to the IMAP server
        imap_server = imaplib.IMAP4_SSL(IMAP_SERVER)
        imap_server.login(IMAP_USERNAME, IMAP_PASSWORD)
        imap_server.select(IMAP_MAILBOX)

        # Search for emails from the target person
        status, email_ids = imap_server.search(None, f'(FROM "{target_email}")')

        if status == 'OK':
            email_ids = email_ids[0].split()
            count = len(email_ids)
            imap_server.logout()

            return count

    except Exception as e:
        logging.error(f'An error occurred while retrieving email count for {target_email}: {str(e)}')
        print(f'An error occurred while retrieving email count for {target_email}: {str(e)}')

    return 0

delay = config['delay']  # Delay between each iteration, in seconds

# Continuously monitor the email inbox
previous_counts = {target_email: get_emails_count(target_email) for target_email in TARGET_EMAILS}
first_iteration = True

# Initial email counts
for target_email in TARGET_EMAILS:
    email_count = get_emails_count(target_email)
    logging.info(f'{email_count} initial emails found from {target_email}')
    print(f'{email_count} initial emails found from {target_email}')

while True:
    try:
        # Get the current count of emails for each target person
        current_counts = {target_email: get_emails_count(target_email) for target_email in TARGET_EMAILS}

        for target_email in TARGET_EMAILS:
            current_count = current_counts[target_email]
            previous_count = previous_counts[target_email]

            if not first_iteration:
                if current_count > previous_count:
                    logging.info(f'{current_count - previous_count} new email(s) received from {target_email}.')
                    print(f'{current_count - previous_count} new email(s) received from {target_email}.')
                    send_email(target_email)
                else:
                    logging.info(f'No new emails from {target_email}.')
                    print(f'No new emails from {target_email}.')

            previous_counts[target_email] = current_count

        first_iteration = False

        # Delay between each iteration
        time.sleep(delay)

    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')
        print(f'An error occurred: {str(e)}')
        break
    except KeyboardInterrupt:
        logging.info('Monitoring stopped')
        print('Monitoring stopped')
        break