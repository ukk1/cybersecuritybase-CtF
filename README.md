# cybersecuritybase-CtF
Cyber Security Base - Capture The Flag

#### Cats

A flag was hidden somewhere into an image of a cat that we needed to find. I first used strings to look up the contents of the image. No further magic was needed:

    strings cat.jpeg
      
    {HiddenCatFlag01}

#### Crack the password

In this challenge we were required to find the password from the password_checker application that was provided. I first used strings to look the contents of the binary. This quickly provided the answer:

    Enter the password :
    CorrectPasswrdAA
    You entered correct password
    
#### Admin panel 

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

#### Save the Day 

We are provided an access.log file to search information about the admin credentials. The credentials can be found easily by just using grep to search the string 'password' from the logs.

    cat log |grep password
    
    13.207.157.242 - - [21/Nov/2016:13:52:55 +0300] "POST /sessions/new?username=admin&password=wronghorsebatterystable HTTP/1.0" 403 4992 "[FILTERED]" "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_7_3; rv:1.9.2.20) Gecko/2016-04-06 01:17:12 Firefox/3.8"
    
Flag for the challenge was 'wronghorsebatterystable'.
