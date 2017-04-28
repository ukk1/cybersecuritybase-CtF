# cybersecuritybase-CtF
Cyber Security Base - Capture The Flag

#### Cats (Easy)

A flag was hidden somewhere into an image of a cat that we needed to find. I first used strings to look up the contents of the image. No further magic was needed:

    strings cat.jpeg
      
    {HiddenCatFlag01}

#### Crack the password (Easy)

In this challenge we were required to find the password from the password_checker application that was provided. I first used strings to look the contents of the binary. This quickly provided the answer:

    Enter the password :
    CorrectPasswrdAA
    You entered correct password
    
#### Hidden in script (Easy)

The challenge was to find a secret backend key, which was leaking through a hidden debugging mode in JavaScript at https://cyber-bank.testmycode.io/.

When visiting the application, it loads a JavaScript -file https://cyber-bank.testmycode.io/assets/application-9bc2bee65ff0948f32fe86b8e5fd85ea194a1e8d46183aa99f7b17681245b793.js

Searching through the JavaScript with a string "debug" I found this: 

    "cyberdebugmode","true","GET","/nothing_to_see_here.json"
    
Visiting the URL we can find the backend key:

    backend-key	"BM1GOMYajD4ONBHxEOq4"
    
#### Admin panel (Easy)

The challenge contains a small web application and requires us to access a secret admin panel. The description states that "The panel supposedly leaked previously when a popular search engine accidentally indexed it. However, security has been tightened since then", which seems that a indexing bot has visited the robots.txt page.

Visiting the https://cyber-bank.testmycode.io/robots.txt gives us:

    # See http://www.robotstxt.org/robotstxt.html for documentation on how to use the robots.txt file
    #
    # To ban all spiders from the entire site uncomment the next two lines:
    # User-agent: *
    # Disallow: /
    Disallow: /super_secret_admin_panel_fds


Thus, visiting the /super_secret_admin_panel_fds gives us the database password, which was the flag for this challenge:

    Database password: "cannothackmelol".
    
#### Awkward Ending Syndrome (Easy)

Looking at the challenge name and description it contains clues about what sort of encryption algorithm is being used, AES and mode of CBC (Canadian Born person named Chad).

In the challenge we have the ciphertext and key that was being used to encrypt the message. Now we also know the scheme, which means we can decrypt the message.

CBC mode uses an IV (initialization vector), which is used to randomize each ciphertext. If the IV would be static or missing completely it would mean that the same string would produce a same ciphertext. When an IV is introduced, it provides randomness into the ciphertext, which means that when two similar plaintext strings are encrypted with different IV the ciphertext is also different.

All in all, with some python script we can decrypt the message:

    from Crypto.Cipher import AES
    import binascii

    key = binascii.unhexlify('000102030405060708090A0B0C0D0E0F')
    iv = binascii.unhexlify('00000000000000000000000000000000')
    ciphertext = binascii.unhexlify('3B953347892900C95858A5C16FD8DFB0920DF37294CBC3313AAB85608D32328D')

    obj = AES.new(key, AES.MODE_CBC, iv)
    plaintext = obj.decrypt(ciphertext)

    print plaintext
    
The flag for this challenge was: ThisIsTheFlagDEAD

#### Save the Day (Easy)

We are provided an access.log file to search information about the admin credentials. The credentials can be found easily by just using grep to search the string 'password' from the logs.

    cat log |grep password
    
    13.207.157.242 - - [21/Nov/2016:13:52:55 +0300] "POST /sessions/new?username=admin&password=wronghorsebatterystable HTTP/1.0" 403 4992 "[FILTERED]" "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_7_3; rv:1.9.2.20) Gecko/2016-04-06 01:17:12 Firefox/3.8"
    
Flag for the challenge was 'wronghorsebatterystable'.


#### Curious cat (Medium)

This challenge provided us another cat image that contained some sort of secret.

First I used exiftool to look the metadata of the picture.

    exiftool cat02.jpeg
    
It showed some interesting data, such as the file size, which seems to show that some steganography has been used.  
    
    File Size                       : 4.0 MB

After this, I used steghide tool to extract the data from the picture.

    steghide extract -sf cat02.jpeg
    
However, it required us to provide a password. No luck.

What about using strings to look for the contents...

    {Search deeper. You might need a "passphrase"}
    
Trying again with steghide and providing the "passphrase" as a password we get the flag.

    steghide extract -sf cat02.jpeg 
    Enter passphrase: 
    wrote extracted data to "cat02chidden.txt".
    root@kali:~/Desktop# cat cat02chidden.txt 
    HiddenCatFlagDE23
    
#### Fuzzy calculator (Medium)

In this challenge we were provided a 64-bit Linux binary, which seems to have some sort of memory corruption issue. Also the name of the challenge seems to suggest that some sort of fuzzing is required to find the correct memory address where the overwrite happens.

I started fuzzing the application with overly long strings, such as "AAAAAAAA" using the following:

	printf "%0.sA" {1..100000} | ./clock
	
This quickly resulted into Segmentation fault.

	Welcome to the cyber calculator!
	Please type a calculation to proceed. (For example 1+1)
	Segmentation fault
	
So it was time to fire the calculator app with GNU debugger (gdb) to see in what memory address does it happen. I used input redirection in gdb to take input from a file where the overly long string of As were saved:

	printf "%0.sA" {1..100000} > fuzzz.txt
	root@kali:~/Desktop# gdb ./clock 
	GNU gdb (Debian 7.12-6) 7.12.0.20161007-git
	...
	...
	Reading symbols from ./clock...(no debugging symbols found)...done.
	(gdb) run < fuzzz.txt 
	Starting program: /root/Desktop/clock < fuzzz.txt
	Welcome to the cyber calculator!
	Please type a calculation to proceed. (For example 1+1)

	Program received signal SIGSEGV, Segmentation fault.
	0x0000000000403670 in memcpy ()
	(gdb) 

The 0x0000000000403670 memory address was the solution for this challenge.
    
#### Killing hashes (Medium)

The challenge gives us the following hash that needs to be cracked

    ef16ab3c539a766ecbe30eb008032e16

At first glance, it seems to be MD5 as it is 32 character alphanumeric string, which means it should be quite easy to crack. We could use password cracking software such as John the Ripper. However, it is much quicker to use readily available tools online, such as https://hashkiller.co.uk/md5-decrypter.aspx

The decrypted password and flag was

    Bundaita
    
#### queenrulez (Medium)

We are provided a cleartext password and its hash value "queenrulez2000" - "bf078b4812ac9e58b486b8f75ba968ba4f18b502". However, the challenge requires us to find out the users new password, which hash value is "3ede8b7d2e4c4fc26529ba543a6c4414793dc502". The challenge also says that only the last four digits has been changed.

The password is hashed with SHA-1 algorithm. I wrote a quick bash script that will generate the password hashes from queenrulez1000 to queenrulez9999.

    #!/bin/bash

    START=0000
    END=9999

    for I in $(seq $START $END)
    do
	    echo "queenrulez$I"
	    echo -n "queenrulez$I" |shasum
    done

When the hashes are created we can search through the list of hashes for a match "3ede8b7d2e4c4fc26529ba543a6c4414793dc502".

The solution was:

    queenrulez5215 - 3ede8b7d2e4c4fc26529ba543a6c4414793dc502

#### Forgot the password? (Medium)

This challenge also required us to discover the correct password for the application. First I used the strings to search the contents of the binary.

    strings password_checker_2
    
    Enter the password :
    Q29ycmVjdFBhc3N3cmRBQUFC
    You entered correct password
    You entered incorrect password

The string "Q29ycmVjdFBhc3N3cmRBQUFC" seems to be the password. However, supplying it as is the password_checker_2 returns an incorrect password message. Looking at the string more closely it uses only alphanumeric characters and is divisible by 4, which suggests that it is base64 encoded. 

By decoding the string in base64 we get the flag:

    echo -n "Q29ycmVjdFBhc3N3cmRBQUFC" |base64 -d
    
    CorrectPasswrdAAAB
