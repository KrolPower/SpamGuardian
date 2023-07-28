# Spam Guardian

This is a Python script that monitors a specified email inbox for new emails from target email addresses and automatically sends a specified number of response emails to each target email address. The purpose of this script is to act as a spam guardian, responding to potential spam emails to deter further communication.

## Prerequisites

Before running the script, please ensure you have the following:
- Python installed on your machine.
- Access to the email account you want to monitor. For this script, it is assumed that you are using a Gmail account.
- A Gmail app password for the email account you want to monitor. If you haven't created one yet, you can follow the instructions [here](https://support.google.com/accounts/answer/185833?hl=en) to generate an app password.

## Setup

1. Download the `spam_guardian.py` file and save it in a desired location on your machine.
2. Create a new directory alongside the `spam_guardian.py` file and name it `config`.
3. Inside the directory, create a new file named `config.json`.
4. Open the `config.json` file and copy-paste the content from the `config_template.json` file provided in this repository.
5. Replace the placeholder values in the `config.json` file with your actual email account information and settings:

    - `imap_server`: The IMAP server address for your email provider. For Gmail, it should be `"imap.gmail.com"`.
    - `imap_username`: Your full email address, e.g., `"your_email@gmail.com"`.
    - `imap_password`: The app password generated for your email account. It should be a string of random characters.
    - `imap_mailbox`: The mailbox or folder from which the script will monitor for new emails.
    - `smtp_server`: The SMTP server address for your email provider. It should be the same as the `imap_server` setting for Gmail.
    - `smtp_port`: The SMTP port number. For Gmail, it should be `587`.
    - `delay`: The delay in seconds between each iteration of monitoring the email inbox. You can adjust this value as per your preference.
    - `target_emails`: A list of email addresses from which the script will monitor for new emails and send response emails. Add the target email addresses enclosed in double quotes, separated by commas.
    - `count`: The number of response emails to send each time a new email is received from a target email address. Adjust this value as per your requirement. 

6. Save the `config.json` file.

## Email Subject

1. Create a new text file in the same directory as `spam_guardian.py` and name it `email_subject.txt`.
2. Open the `email_subject.txt` file and enter the desired subject line for the response emails.
3. Save the `email_subject.txt` file.

## Email Body

1. Create a new text file in the same directory as `spam_guardian.py` and name it `email_body.txt`.
2. Open the `email_body.txt` file and enter the desired content of the response emails.
3. Save the `email_body.txt` file.

## Running the Script

1. Open a command prompt or terminal window.
2. Navigate to the directory where you saved the `spam_guardian.py` file.
3. Run the following command to start the script:
   ```
   python spam_guardian.py
   ```
4. The script will start monitoring the specified email inbox and display the initial email counts for each target email address.
5. As new emails are received from the target email addresses, the script will log the event and send the specified number of response emails to deter further communication.
6. The script will continue running until you manually stop it by pressing `Ctrl + C` in the command prompt or terminal window.

Please note that the script will log its activities to a file named `email_spam.log` in the same directory. You can check this log file for any errors or troubleshooting if needed.