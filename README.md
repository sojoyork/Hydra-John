# about hydra-john
Hydra-John is a mixture of hydra and john-the-ripper (aka john or JTR)
I got the idea of hydra-john while i was playing some video-games (because i was bored and i got nothing to do)

## some hydra john commands
the first command that you arte going to use is the `hydra-john -help` command and after getting the basics through the help command you can type this long command:
```
python hydra_john.py -u user_list.txt -ptph /etc/shadow -host <target_host_ip> -port 22 -tuser target_user -tpass target_password
```

## installing hydra-john
to install hydra-john go to your terminal and type:
```
git clone https://github.com/sojoyork/Hydra-John.git
```
then type:
```
cd Hydra-john
```
then type `python3 hydra-john.py -help` and then you installed hydra-john!

## dependencies:
Perform tests in a controlled and isolated environment to avoid unintended consequences if you are new or smthing elsw. Don't ask me anything.
make sure that the python modules: `paramiko`, `argparse`, and   `subprocess`, are installed (and python too! (if needed)) and make aure John-the-ripper and hydra are in your system's path!
