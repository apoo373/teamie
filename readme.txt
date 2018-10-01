This Assignment has been designed in python django. In order to run this App, you need to install all the requirements.

Prerequisites:
1) This Software Requires python2.7 and pip
  a) sudo apt-get install python2.7
  b) sudo apt-get install python-pip
2) The other requirements are mentioned in requirements.txt and can be installed using pip
  a) sudo pip install -r requirements.txt


Steps to Run the App
1) Extract the tar.gz file
  a) tar -xvf <file_name>
  b) cd teamie
2) Install the Prerequisites
3) IMPORTANT: Add your credentails to the App
  a) Add your twitter Apps Secret Key to the '/teamie/twitter_users/setting.py' file.
  b) Append the 'LOGIN_REDIRECT_URL' value in the above file to the approved callback urls in your twitter API
  NOTE :: Step b) is very important as it is a security feature of twitter and without it the App will not function as twitter only allows post-login redirection to pre-approved urls.
4) run the django server
  a) python manage.py runserver
5) Go to your browser at 'http://127.0.0.1:8000/twitter/login'

Features of the App
1) All of the features have embellished with a UI with bootstrap and related js and css.
2) The App will redirect to '/twitter/allFollowers', where all followers of the user will be listed in a table.
3) The User can analyze a specific follower by clicking the 'Analyze' button
4) The 'Analyze' button will redirect to '/twitter/followerAnalysis/<twitterId>' where all the details are listed in various tables.
5) There are 3 Basic tables on this page:
  a) Basic Details: Basic Details of the follower
  b) Rubrik Metrics: All required Metrics arrayed in a table
  c) Counts: Friends Count, Followers Count etc of the follower
6) All logic and coding related to the Rubrik computation is present in '/teamie/twitter_users/rubric.py'
7) The Document mentioned to return a json response for a particular follower. However I have rendered it on a page (Its much more elegant and pretty !!)
  a) However, the data asked for is present in complete (along with some additional) and the json is being printed
  b) You can get the Json response by uncommenting the 'JsonResponse()' line in the 'twitter_follower_analysis' function in the '/teamie/twitter_users/views.py' file.
8) The functionality to filter by category has been implemented
  a) GET HTTP 'http://127.0.0.1:8000/checklist/category/{category_Name}'
  b) eg. 'http://127.0.0.1:8000/checklist/category/health'
8) There is a logout Link in the Dashboard as well.
