#!/usr/bin/env python
import sys
import getpass
import imaplib


configuration = {
    'example_account_1': {
        'host': 'imap.gmail.com',
        'user': 'example_account_1@gmail.com',
        'mailbox': '[Gmail]/All Mail',
        'email_addresses_to_remove': [
            '@facebookmail.com',
            '@e.groupon.com'
        ]
    },
    'example_account_2': {
        'host': 'imap.example_email_host.com',
        'user': 'example_account@example_email_host.com',
        'mailbox': 'Archive',
        'email_addresses_to_remove': [
            'example_account_1@gmail.com',
            'spam@'
        ],
    }
}


def main():
    if len(sys.argv) < 2:
        print 'please give which config to run with'
        return
    else:
        config_name = sys.argv[1]

    if config_name not in configuration:
        print 'couldn\'t find that config entry'
        return

    cleanup = configuration[config_name]
    host = cleanup['host']
    user = cleanup['user']
    mailbox = cleanup['mailbox']
    addresses_to_remove = cleanup['addresses_to_remove']

    #connect to host
    imap = imaplib.IMAP4_SSL(host)
    imap.login(user, getpass.getpass())

    #get the mailbox we want to work with
    imap.select(mailbox)
    total_emails_to_remove = len(addresses_to_remove)
    for i, email_address in enumerate(addresses_to_remove):
        print '{0}/{1} '.format(i + 1, total_emails_to_remove),
        print email_address

        criteria = '(FROM "{0}")'.format(email_address)
        typ, data = imap.search(None, criteria)
        total_msgs = len(data[0].split())

        print "\tFound {0} messages".format(total_msgs)
        if total_msgs == 0:
            continue

        if total_msgs > 5000:
            prog = ProgressBar(0, 5000)
        else:
            prog = ProgressBar(0, total_msgs)
        oldprog = str(prog)

        print "\tSetting Delete Flag..."
        flagged_count = 0
        for num in data[0].split():
            imap.store(num, '+FLAGS', '\\Deleted')
            flagged_count += 1
            prog.increment_amount()
            if oldprog != str(prog):
                print "\t", prog, "\r",
                sys.stdout.flush()
                oldprog = str(prog)
            if flagged_count == 5000:
                print "\n\tcalling expunge..."
                typ, data = imap.expunge()
                prog.update_amount(0)
                flagged_count = 0
        print "\n\tcalling expunge..."
        typ, data = imap.expunge()
        print "\t{0} messages deleted".format(len(data))
    imap.close()
    imap.logout()


class ProgressBar:
    """
    based on code from http://www.5dollarwhitebox.org/drupal/node/65
    """
    def __init__(self, min_value=0, max_value=100, width=77):
        self.char = '#'
        self.mode = 'fixed'
        self.bar = ''
        self.min = min_value
        self.max = max_value
        self.span = max_value - min_value
        self.width = width
        self.amount = 0  # When amount == max, we are 100% done
        self.update_amount(0)

    def increment_amount(self, add_amount=1):
        """
        Increment self.amount by 'add_ammount' or default to incrementing
        by 1, and then rebuild the bar string.
        """
        new_amount = self.amount + add_amount
        if new_amount < self.min:
            new_amount = self.min
        if new_amount > self.max:
            new_amount = self.max
        self.amount = new_amount
        self.build_bar()

    def update_amount(self, new_amount=None):
        """
        Update self.amount with 'new_amount', and then rebuild the bar
        string.
        """
        if not new_amount:
            new_amount = self.amount
        if new_amount < self.min:
            new_amount = self.min
        if new_amount > self.max:
            new_amount = self.max
        self.amount = new_amount
        self.build_bar()

    def build_bar(self):
        """
        Figure new percent complete, and rebuild the bar string base on
        self.amount.
        """
        diff = float(self.amount - self.min)
        percent_done = int(round((diff / float(self.span)) * 100.0))
        # figure the proper number of 'character' make up the bar
        all_full = self.width - 2
        num_hashes = int(round((percent_done * all_full) / 100))

        if self.mode == 'dynamic':
            # build a progress bar with self.char (to create a dynamic bar
            # where the percent string moves along with the bar progress.
            self.bar = self.char * num_hashes
        else:
            # build a progress bar with self.char and spaces (to create a
            # fixe bar (the percent string doesn't move)
            self.bar = self.char * num_hashes + ' ' * (all_full - num_hashes)

        percent_str = str(percent_done) + "%"
        self.bar = '[ ' + self.bar + ' ] ' + percent_str

    def __str__(self):
        return str(self.bar)


if __name__ == '__main__':
    main()
