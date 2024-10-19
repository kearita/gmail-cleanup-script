## **Gmail Cleanup Script**

### **Project Overview**
This Python script automates the process of deleting old and unread emails in Gmail in order to free up space in my Google account. The script connects to Gmail using the Gmail API and moves unread emails that are older than a specified number of days to the trash. It also targets emails in the "Promotions" and "Social" tabs that are older than 30 days and moves all spam emails to the trash.

### **Motivation**
I created this project because I was running out of Google storage space. Most of my emails were not important so I wanted to automate the cleanup process because I had about 29,000 emails across 2 Gmail accounts that I have had for over a decade. This project works across both of my Gmail accounts and runs automatically each week via Task Scheduler.

### **Key Features**:
- Deletes unread emails older than 90 days.
- Deletes unread emails in the "Promotions" and "Social" categories that are older than 30 days.
- Moves all emails in the Spam folder to the trash.
- Handles multiple Gmail accounts.
- Implemented pagination to handle thousands of emails efficiently.
- Automatically runs weekly via Task Scheduler on Windows.

## Setup and Installation

### 1. **Gmail API Setup:**
   - I went to [Google Cloud Console](https://console.cloud.google.com/).
   - Created a new project and enable the **Gmail API**.
   - Then I configured the **OAuth consent screen** and created **OAuth 2.0 credentials** (set as a "Desktop App").
   - Then I downloaded the `credentials.json` file and placed it in the directory with my Python script.
   
### 2. **Python Dependencies:**
   I installed the required dependencies by running:
   ```bash
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3. **Running the script:**
  - The first time I ran the script, it prompts you to authenticate and grant access to the Gmail account. Then that generate a `token.pickle` file for future runs, so you don't need to authenticate each time.
   - I set it up so you can modify the script to add credentials for multiple Gmail accounts by creating separate `credentials.json` and `token.pickle` files for each account.

### 4. **Task Automation:**
   - I set up the script to run automatically every week using **Task Scheduler** on Windows:
     - I opened **Task Scheduler** and created a new task.
     - Then I set the task to run the Python script weekly on Sundays.
     - Then I pointed the Task Scheduler to the Python executable and the script file path.

### 5. **Challenges:**
   - **Initial Authentication**: I had to learn how to set up OAuth 2.0 credentials to connect the script to Gmail, which involved configuring Google Cloud and setting up the consent screen.
   
   - **Switching from `messages.delete` to `messages.trash`**: Initially, I used `messages.delete`, but this caused issues because I was getting a `HttpError 403`. I thought the problem was the scopes but it didn't fix it. Switching to `messages.trash` fixed the problem by sending the emails to the Trash folder, where they are automatically deleted after 30 days anyway.
   
   - **Pagination**: The Gmail API returns up to 100 emails per request, which was limiting the script to only processing 100 emails at a time. I implemented pagination to fetch and delete all emails beyond the first 100 in each run, allowing the script to handle thousands of emails across multiple accounts. After U made this fix and ran it, it took <> hours!

   - **Multiple Accounts**: I added support for both of my Gmail accounts, allowing the script to clean up emails from more than one account by storing separate credentials and tokens for each.

   ### **Results**
   - I set up the script to run automatically every week using **Task Scheduler** on Windows:
   - I started with approximately 29,000 emails across both of my Gmail accounts.
   - For the first account, the script deleted 15,302 emails.
   - For the second account, the script deleted 4,420 emails.
   - The entire process took about 6 hours to complete.
