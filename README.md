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
