BEeF is a phishing + gmail bomber toolkit, made in python3 created by the blackhat to DoS attack
via gmail. It uses simply techniques to evade gmail anti-spam filter and you can use the tool
for DoS or saturation inbox atack ::You must to use 10 zombies/dummys accounts, because after the attack
the accounts will be banned instantly::.
_________________________________________________________________________________________________________

Installation (kali-linux/Termux)

1) Sudo apt update/pkg update *(Termux)*

2) git clone:

3) python3 -m venv venv

4) source venv/bin/activate or source venv/bin/activate.fish (if use fish)

5) pip3 install fake-useragent

6) pip3 install dnspython

7) cd

8) python3 BEeF.py -h to see te usage. (read carefully!)
________________________________________________________________________________________________________

Basic BEeF attack (Normal mode)

Example: 

python3 BEeF.py -m normal -t target@gmail.com -s yourgmail@gmail.com -p "app pass" -c count -d wathever you want

DoS BEeF attack (more dangerous!)

1* setup +10 zombies or dummys account to attack

2) #create a nano accounts.txt
you must put like this

Dummyaccount@gmail.com:apppassword
zombieaccount@gmail.com:apppassword
cadaveraccount@gmail.com:apppasword
attackeracc@gmail.com:appassword
phisheraccount@gmail.com:apppassword
easyhaha@gmail.com:apppasword
bashacc@gmail.com:apppasword
hellohaha@gmail.com:apppassword
hellotonter@gmail.com:apppassword

ctrl + o, ctrl + x

python3 BEeF.py -m super/BEeF DoS -t target@gmail.com -c count -a nano accounts.txt -d duration
________________________________________________________________________________________________________________________

the name BEeF is temporally, credits to 'https://github.com/beefproject' 

(!) When the DoS attack started, the gmail will bombed then the accounts will banned, please make sure use zombies accounts

(!) use it carefully, U can add proxies to anonymous with the option -x

(!) read "python3 BEeF.py -h" carefully

(!) regular password will not work, use app password

(!) the password must use " ". ex: "qekd aksi wdxa"

Thanks!
