# Tweetlytics
**Real-Time Tweet Analytics With Apache-Kafka and python**

## Retrieve code

* `$ git clone https://github.com/sheshnath08/Tweetlytics.git`
* `$ cd Tweetlytics`


## Major Dependensies

**The project uses [Tweepy](http://www.tweepy.org/) library to get tweets from twitter, [Apache-Kafka](https://kafka.apache.org/) as a messaging queue, [Flask](http://flask.pocoo.org/) as Back-end Server and [Socket-IO](https://socket.io/) to update front-end in Real-Time** 

## Architecture and Dataflow
![Architecture Image](https://raw.githubusercontent.com/username/projectname/branch/path/to/img.png)

##Running

* First, you will need to setup kafka, follow this tutorial by [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-14-04)

* Install the required python library: 

    `$ pip install -r requirement.txt`

* Get Access Token and Consumer keys from [Twitter](https://apps.twitter.com/) and Update Keys.py File
* Run the Back-end Server

    `$ python Tweetlytics.py`
 