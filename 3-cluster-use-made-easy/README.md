# SSH & Github made easy

Much thanks to Ziteng for his help with this section! 


## SSH config file. 
One of my least favorite things about SSH is that you need to type this annoying string 
every time you use it. 
`ssh john@dev.example.com -p 2322`

With SSH config files, you can avoid this pain. 
Start by making a `~/.ssh/config` file. 

In this file, you can add configurations like the following 


```
Host lambda
    HostName 192.168.1.1 # Get this from lambda instance
    User ubuntu
    ForwardAgent yes
    IdentityFile ~/.ssh/lambdalab.pem
 ```

This then allows you to ssh trivially 

`ssh lambda`

There is an example config file in this folder. 

See this [link](https://linuxize.com/post/using-the-ssh-config-file/) for more.

Note that in the case of lambda, you will need to update the git config file 
every time you initialize a new instance, since the ip will change. 




## Dealing with Github on a remote server. 


If you use any remote computing resources for any amount of time, you'll encounter some annoyances. 
Namely, github requires an SSH key to pull private repos. Also, remembering different commands 
for different hosts can be a big pain. 

Most of this information is available [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh).

In particular, following this page, we want to execute the following steps


1. Generate new SSH key [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
2. Add the new SSH key to your git account [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
3. Turn on SSh agent forwarding. See [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/using-ssh-agent-forwarding)

Part 3 is the key step. This will set up an agent so that github authentication. 
You would then add the following to your config file 
```
 Host github.com
    User git
    Hostname github.com
    AddKeysToAgent yes
    IdentityFile ~/.ssh/github
 ```

This will tell the agent to pass on your github credentials whenever you 
start an SSH session. For this to work, we need to be sure to add
`ForwardAgent yes` when we add a remote server to our config file. 
See the example in the previous section. 

If you do this, then your github keys will automagically be transfered 
onto a server when you log in. 

### Possible considerations. 

1. the `ssh-add` command has to be run every time the local machine is rebooted
(you can add that in zshrc but I just manually do that since I rarely ever reboot my laptop)

2. if you are testing this on some existing repo, you have to make sure the repo was cloned using ssh instead of https. 
If it’s new repo, use `git clone git@github.com:ZachariahPang/Figure-Learner.git` 
instead of `git clone https://github.com/ZachariahPang/Figure-Learner.git`. If it’s an existing repo, 
switch http over to ssh following stesp here https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories#switching-remote-urls-from-https-to-ssh
