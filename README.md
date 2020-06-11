# The-Quote-Book
A Web App that makes use of a friend's self-curated dataset of funny out-of-context quotes in conversation. This is designed as both a gift to that friend so she can contribute new quotes and see old ones mobile, and as a learning experience for me.




# Recent Updates

### Prod-1
- Push onto AWS for production.
- Register for domain-name nicolesquotebook.com

# Next Updates
- quote upload
- search bar. 



<h1>About the Book</h1>
<p>Nicole Pradas is a wonderfully weird human being and prefers the company
of similarly-curious characters. It's not uncommon for one of these weirdos––
often Nicole herself–– to say something crazy enough to make a stranger's
head turn.</p>
<p> The difference between Nicole and a typical goofball is that she
will write those odd phrases down, often without context, into what she
affectionately refers to as "The Quotebook". For well over a decade,
Nicole's Quote Book has collected funny and strange snapshots of her
daily life and the lives of her friends.</p>

<p> This website is gift to honor that weirdo. Inside, you will find
a collection of random snipits of conversations dating all the way back to
2010. Some are hilarious, some are serious, and some are just plain strange.
All of them are treasured here and available for a select few friends &
family to enjoy and reminisce over. </p>

 </br>
 <h2>About the Developer</h2>

 <p> Will Johnson is one of the many weirdos featured in the Quotebook.
  He works as a Python Developer during the day and enjoys making music
  and woodworking in his spare time. In 2020, he wanted to make something
  special for his amazing friend Nicole while also learning more about
  web-development, so he built this site. He's one of the administrators
  for this site as well.</p>

# <center> Dev Process </center>
### Flask-App development
As an experienced python developer with little/no experience in web-dev, I chose a framework that would let me start in a language I was familiar with. Why Flask over Django? Simple, a friend told me to so I did. To get started building back-end template loaders in my `routes.py` file found in the `app` folder, I read through the first several chapters of this tutorial: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world . I later learned that anyone and everyone who had used flask at some point has seen this tutorial so I highly suggest newcomers learn there too!

The database is in <b> Postgres</b>, again due to my familiarity with the platform. That said, in retrospect there's way more examples and helpful tutorials/docs around MySQL so I might consider that for my next project. Spining up a database was easy enough, but before I could start populating it, I had to come up with a way to model this database so that I can maximize storage efficiency with relatively simple design. 

#### Data Model ERD

{pic of ERD}

It took a while to get to a place where I could execute python commands like `db.add(user)` that would add new rows into these tables, but once I did I could easily implement logic into the `routes.py` file to allow users to submit quotes, signup for a profile, and for administrators to have certain special privileges. 

### UX Development

Another suggestion I got was to start my HTML/CSS work entirely in grayscale. The idea is that if a user can navigate around use the site without much trouble or confusion without any colors or pictures, then the design is less likely to get in the way of the UX. 

This was my very first foray into Javascript, and the reason I was so adamant about using it here was because it really makes certain functionalities pop out. For example: that drop down menu that asks "ARE YOU SURE?" anytime you perform an irreversable action is _technically_ possible without javascript, but it made the whole process a lot smoother if I could just call functions when I needed them. 

The ability to have an unlimited number of quote phrases with speakers meant the site had to adapt to a user wanted to re-build a form on the fly without making any additional requests from the server. This is what the `addFrom.js` file is for and it works waaaay better than any python hack I could put together. 

{pic of additional quote phrases}

### Web Design

As I mentioned before, having the UX coded in grayscale meant I could be a lot more confident in the design choices not impacting the layout. This was almost entirely in CSS, and it took weeks! I have a newfound appreciation for designers who can simply dream up a layout and make it flow without constantly second-guessing themselves. Design is NOT development. I could have tinkered forever but I'm happy with how it came out. 

#### Pre Design Sprint

{Pic of pre-design sprint}

#### Post Design Sprint

{Pic of post-design Sprint}

Amazing what some color, photos, and motion graphics can do to make your site really stand out!

### AWS Deployment

The final and perhaps most challenging part of this whole process was spinning up an EC2 instance on Amazon Web Services to host this. The goal was to have something that was cheap to run (it's a birthday gift, after all) that could handle a few dozen requests but wouldn't need to scale up much from there. As such, I skipped a few vital steps if I were planning on taking this worldwide. 

Things like:
- Load Balancer
- Elastic Beanstalk

I actually tried the Elastic Beanstalk framework pretty thoroughly. The issue I was having with it were the dependencies and specific environment variables that EB does not give me 100% freedom to change as needed, opting instead to do most of that heavy lifting for you. In retrospect, I should have started here at EB and scaled up my website from there. Would have been more expensive to dev since I'd be spinning up Ec2 during dev, but the act of updating and server management that EB has is so killer.

Instead, I spun up the cheapest Linux-based EC2 that Amazon has and cloned my repository in there. It took a while to get the environment to run Python 3 with all the requirements in the `.txt` file, but once I got it running I was able to test the website on the EC2's public IP. Low and behold, there's my webiste on an external machine!

Then I had to do something super challenging which was figure out how to get an EC2 instance to run like a dedicated server. An experienced System Administrator would have had few issues with this, but it took me FOREVER to learn about services and how a machine keeps running commands even when I turn off my terminal window and log out of EC2. The environment variables were particularly stuborn, so this tells me I need to spend more time learning how to put an environment together properly. Dependency issues will always come back to haunt you. 

Best tutorial I found on the subject was here: https://medium.com/@abhishekmeena_68076/how-to-deploy-the-flask-django-app-on-aws-ec2-with-gunicorn-ngnix-with-free-ssl-certificate-566b2ada3b6a

The final stack of AWS tools I used were:
- *RDS*: for hosting the postgres database
- *EC2*: the cloud computer I rigged as a web server.
- *Gunicorn*: Package I used to act as a server for the site (pronounced gun-icorn? or maybe g-unicorn?).
- *SystemCTL*: Package used to set the server up as a continuous service. 
- *Route 53*: To register the domain and port users over to this EC2's IP. 

The very last thing to do is to upload all the quotes to this site! At first I wanted to do this as an exercise in NLP, but in truth it'd really just be data cleaning with a BUNCH of regex that would take me hours to do in code and only about one hour to do myself. Plus, I intend to spend an afternoon going through quote by quote with the birthday-girl so we can reminice about each one. Sometimes the less engineered path is more enjoyable. 

