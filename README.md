# about hydra-john
Hydra-John is a mixture of hydra and john-the-ripper (aka john or JTR)
I got the idea of hydra-john while i was playing some video-games (because i was bored and i got nothing to do)

## some hydra john commands
the first command that you arte going to use is the `hydra-john -help` command and after getting the basics through the help command you can type this long command:
```
sh:
```
python hydra_john.py -u user_list.txt -ptph /etc/shadow -host <target_host_ip> -port 22 -tuser target_user -tpass target_password
```
