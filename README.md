Flyback Blog
============

Flyback Blog is a micro blog blog system using python + flask + pymongo + mongodb + markdown.

Here is online example: http://easonhan.info/


### setup development env

Before setup you must install python 2.5+ and install pip and install mongodb. __Make sure your mongodb is running__.

Flyback bbs development env is running well on windows.

* git clone
* [sudo] pip install Flask
* [sudo] pip install pymongo
* [sudo] pip install markdown
* cd flyback_bbs
* python ./db/seeds.py
* python app.py
* access localhost:5000 via your browser


### deploy production env(Linux or Mac ONLY)

Before setup you must install python 2.5+ and install pip and install mongodb. __Make sure your mongodb is running__.
Install nginx and make sure it is runing

* git clone
* [sudo] pip install Flask
* [sudo] pip install pymongo
* [sudo] pip install markdown
* [sudo] pip install gunicorn
* cd flyback_bbs
* python ./db/seeds.py(__you should modify seed.py to change the username and password__)
* see ```nginx.conf.example``` and modify your nginx config to fit what you want 
* reload nginx
* ./bin/start.sh &
* access www.your_domain.com via your browser
