This is a project to deploy a flask web app on AWS elastic beanstalk.
Flask is an open source web application framework for Python.
On Linux and macOS, you can use your preferred shell and package manager. On Windows 10, you can install the Windows Subsystem for Linux to get a Windows-integrated version of Ubuntu and Bash.

Flask requires Python 3.7 or later. In this tutorial we use Python 3.7 and the corresponding Elastic Beanstalk platform version. Install Python by following the instructions at Setting up your Python development environment.
Set up a Python virtual environment with Flask
Create a project directory and virtual environment for your application, and install Flask.

To set up your project environment

Create a project directory.

~$ mkdir eb-flask
~$ cd eb-flask
Create and activate a virtual environment named virt:

~/eb-flask$ virtualenv virt
~$ source virt/bin/activate
(virt) ~/eb-flask$
You will see (virt) prepended to your command prompt, indicating that you're in a virtual environment. Use the virtual environment for the rest of this tutorial.

Install Flask with pip install:

(virt)~/eb-flask$ pip install flask==2.0.3
View the installed libraries with pip freeze:

(virt)~/eb-flask$ pip freeze
click==8.1.1
Flask==2.0.3
itsdangerous==2.1.2
Jinja2==3.1.1
MarkupSafe==2.1.1
Werkzeug==2.1.0
This command lists all of the packages installed in your virtual environment. Because you are in a virtual environment, globally installed packages like the EB CLI are not shown.

Save the output from pip freeze to a file named requirements.txt.

(virt)~/eb-flask$ pip freeze > requirements.txt
This file tells Elastic Beanstalk to install the libraries during deployment. For more information, see Specifying dependencies using a requirements file.

Create a Flask application
Next, create an application that you'll deploy using Elastic Beanstalk. We'll create a "Hello World" RESTful web service.

Create a new text file in this directory named application.py with the following contents:

Example ~/eb-flask/application.py


from flask import Flask

# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
  
  
  Deploy your site with the EB CLI
You've added everything you need to deploy your application on Elastic Beanstalk. Your project directory should now look like this:

~/eb-flask/
|-- virt
|-- application.py
`-- requirements.txt
The virt folder, however, is not required for the application to run on Elastic Beanstalk. When you deploy, Elastic Beanstalk creates a new virtual environment on the server instances and installs the libraries listed in requirements.txt. To minimize the size of the source bundle that you upload during deployment, add an .ebignore file that tells the EB CLI to leave out the virt folder.

Example ~/eb-flask/.ebignore


virt
Next, you'll create your application environment and deploy your configured application with Elastic Beanstalk.

To create an environment and deploy your Flask application

Initialize your EB CLI repository with the eb init command:

~/eb-flask$ eb init -p python-3.7 flask-tutorial --region us-east-2
Application flask-tutorial has been created.
This command creates a new application named flask-tutorial and configures your local repository to create environments with the latest Python 3.7 platform version.

(optional) Run eb init again to configure a default keypair so that you can connect to the EC2 instance running your application with SSH:

~/eb-flask$ eb init
Do you want to set up SSH for your instances?
(y/n): y
Select a keypair.
1) my-keypair
2) [ Create new KeyPair ]
Select a key pair if you have one already, or follow the prompts to create a new one. If you don't see the prompt or need to change your settings later, run eb init -i.

Create an environment and deploy your application to it with eb create:

~/eb-flask$ eb create flask-env
Environment creation takes about 5 minutes and creates the following resources:

EC2 instance – An Amazon Elastic Compute Cloud (Amazon EC2) virtual machine configured to run web apps on the platform that you choose.

Each platform runs a specific set of software, configuration files, and scripts to support a specific language version, framework, web container, or combination of these. Most platforms use either Apache or NGINX as a reverse proxy that sits in front of your web app, forwards requests to it, serves static assets, and generates access and error logs.

Instance security group – An Amazon EC2 security group configured to allow inbound traffic on port 80. This resource lets HTTP traffic from the load balancer reach the EC2 instance running your web app. By default, traffic isn't allowed on other ports.

Load balancer – An Elastic Load Balancing load balancer configured to distribute requests to the instances running your application. A load balancer also eliminates the need to expose your instances directly to the internet.

Load balancer security group – An Amazon EC2 security group configured to allow inbound traffic on port 80. This resource lets HTTP traffic from the internet reach the load balancer. By default, traffic isn't allowed on other ports.

Auto Scaling group – An Auto Scaling group configured to replace an instance if it is terminated or becomes unavailable.

Amazon S3 bucket – A storage location for your source code, logs, and other artifacts that are created when you use Elastic Beanstalk.

Amazon CloudWatch alarms – Two CloudWatch alarms that monitor the load on the instances in your environment and that are triggered if the load is too high or too low. When an alarm is triggered, your Auto Scaling group scales up or down in response.

AWS CloudFormation stack – Elastic Beanstalk uses AWS CloudFormation to launch the resources in your environment and propagate configuration changes. The resources are defined in a template that you can view in the AWS CloudFormation console.

Domain name – A domain name that routes to your web app in the form subdomain.region.elasticbeanstalk.com.

All of these resources are managed by Elastic Beanstalk. When you terminate your environment, Elastic Beanstalk terminates all the resources that it contains.
