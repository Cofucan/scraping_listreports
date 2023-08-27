# Notes

We need to run Chrome in debug mode. On Windows, we can do that using the following command.

```sh
chrome --remote-debugging-port=9222
```

If Chrome is not in the PATH, you can use the fill path of Chrome.

```sh
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

Then navigate to this address `127.0.0.1:9222/json/version` to confirm that debugging is enabled.

## Encryption

Before doing any encryption, make sure to generate an encryption key and store it in a file. You can do this with the following command. If you are on a Linux environment, you might have to use `python3` instead of `python`.

```sh
python secure.py
```

It will create a file with an encryption key and store it in the project directory. You can also use a previously generated key file. After that, you can use the following command for encrypting the file.

```sh
python secure.py --encrypt <path_to_file> <path_to_keyfile>
```

Please move this file to a secure location as this is the key that will be used to encrypt and decrypt your files. For any particular file, you must use the same encryption key to decrypt it which was used to encrypt it.
