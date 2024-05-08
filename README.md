# ec2-hashrig

This is just a little project I whipped up. It's more for proof of concept, but it does work.

The idea is that you host an AWS EC2 instance which is very beefy, but very expensive (something like p4d.24xlarge for example, which is like 24k a month to run continous). However, you have a script which automatically starts the instance, feeds a hash, returns the cracked hash, and then shuts down the instance. This way, you only incur potentially minutes of costs, but still have access to powerful compute.

The bash script is hard-coded for NTLM. In reality, you would want to modify it to take in parameters for how you want it to crack hashes.

Anyways, this was fun to play with, and I think it's a start for something more real.

You will need a .aws folder containing a credential file in the following format, stored in the default filepath that boto3 looks for (or modify the settings):

\[default]
region = us-east-1
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY



You will also need to make /potfile, /hashes, and /scripts folders in root filesystem (I build this for Ubuntu specifically). Modify permissions correctly.

You will also of course need an IAM user with access creds.

I kind of just threw this whole thing together in an hour, be warned, and be careful if running an expensive instance.
