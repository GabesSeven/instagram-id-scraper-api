<h1 align="center">Instagram ID scraper API</h1>

<hr>

## 📋 Project description

<p align="justify">
  <br>
  Instagram ID scraper API, project built as a work on the Upwork.com (<a href='https://www.upwork.com/'>https://www.upwork.com/</a>) platform, objective of this project is to filter users from strings provided in the input file. <br>
  <br>
When parsing the string, if there are more than three users, nothing is returned, otherwise, the respective ID of that user is returned.<br>
  <br>
"search.py" has an authentication process, simulating packages from a smartphone.<br>
  <br>
"search2.py" does not have an authentication process.<br>
</p>

<hr>


## 🖥️ Usability

<!--sec data-title="Prompt: OS X and Linux" data-id="OSX_Linux_prompt" data-collapse=true ces-->

To run the "search.py" program, it is necessary to have an input file with the strings to be scraped: <br>

    $ ls input-file.txt 
    user1
    user2
    user3
    user4
    ...

The program is executed passing the input file as the first parameter and the output file as the second parameter: <br>  

    $ python search.py input-file.txt output-file.txt

Finally, the ID of each user separated by pipeline will be returned, if the number of users found corresponding to the searched string is less than four: <br>

    $ ls output-file.txt 
    user1
    |id1,id2,id3
    user2
    |id1,id2
    user3
    |id1
    user4
    |
    ...
    
In the previous example, user1 found four users, user2 two users, user3 one user, and user4 found more than four users.

<!--endsec-->


<hr>

## 📁 Project access

You can [access the project's source code](https://github.com/GabesSeven/instagram-id-scraper-api/) or [download it](https://github.com/GabesSeven/instagram-id-scraper-api/archive/refs/heads/main.zip).

<hr>

## ✔️ Techniques and technologies used

- ``Python``

<hr>

## 🧑‍💻 Developer

| [<img src="https://avatars.githubusercontent.com/u/37443722?v=4" width=115><br><sub>Gabriel Ferreira</sub>](https://github.com/GabesSeven)
| :---: 
