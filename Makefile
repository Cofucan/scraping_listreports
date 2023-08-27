encrypt_emails:
	python secure.py --encrypt emails.json key.key

encrypt_options:
	python secure.py --encrypt options.ini key.key

decrypt_emails:
	python secure.py --decrypt emails.json.enc key.key

decrypt_options:
	python secure.py --decrypt options.ini.enc key.key

generate_key:
	python secure.py --generate-key key.key
