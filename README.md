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
