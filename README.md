## README.md

The target of this project is to allow mobile devices or trusted parties to securely send their public IP address to your network to allow dynamic whitelisting of their IP. 

Use cases: You want to open a port on your firewall to your web server, but you don't want just anyone(or anything) to make their way in. This program will securely send you their IP, whitelist on your firewall, and let them(and only them) in.

A VPN is another possible solution to this problem as well...

Tin foil hats welcome!


1. Create Private/Public SSH key via ssh-keygen
2. Ensure the public key is in the "authorized_keys" file on the destination host
3. On the localhost, add the private key in ~/.ssh folder as
"smart-ip-updater"
