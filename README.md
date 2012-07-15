imap-cleanup
============

I found myself needing a script to remove thousands of unwanted email that had been accidentally archived instead of deleted. This script does just that.


## Installation

	git clone git://github.com/cvaughn/imap-cleanup.git

## Configure

open cleanup.py and fill in configuration dictionary

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

## Usage

	./cleanup.py configuration_name
	example:
		./cleanup.py example_account_1

## GMAIL

To use with Gmail you need to change Gmail's IMAP settings so that it conforms to the
IMAP spec when it comes to deleting email.

* go to Gmail Settings
* click Forwarding and POP/IMAP tab
* check "Auto-Expunge off - Wait for the client to update the server."
* check "Move the message to the Trash"
* Save

## The MIT License (MIT)
Copyright (c) 2012 Chris Vaughn

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.