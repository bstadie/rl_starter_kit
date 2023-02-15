## Introduction

VSCode has a nice integration with remote access, which is one way to access Quest. VSCode offers two ways to connect to Quest via SSH, either by password authentication or by public key authentication. Once connected, the terminal can be accessed in a view on VSCode and SLURM jobs can be easily sent to the queue within the VSCode window. 

## Setting up VSCode for Remote Access

VSCode comes with several extesions and plugins that can be downloaded. When VSCode is open, find the settings gear icon in the lower left corner and select 'Extensions' from the drop down. There are three extensions to install. All three are published and owned by Microsoft.

- Remote - SSH 
- Remote - SSH: Editing Config Files
- Remote Explorer

Once these extensions are loaded, VSCode is ready to connect to remote servers.

## Setting up SSH Connection

The SSH connection can be configured to allow for an easier login process. This guide will cover key-based login, which prevents a need to enter a password every time, and is equally. if not more secure, than password based logins. 

Quest generates a public/private key pair for each user. Once in Quest, navigate to `~/.ssh/` which will contain a private key called `id_rsa` and  a public key called `id_rsa.pub`. The public key is to be copied to the local device and will be the key used to log into the Quest remote servers. 

The process for logging from the local device differs for Windows and *nix (OSX or Ubuntu) 

### *nix Based OS

In the local server, navigate to `~/.ssh/` and create a file called `config` if it doesnt exist yet. Using a text editor of choice, include the following within the `config` file:

```
Host          quest (or any other name to alias the host)
HostName      quest.northwestern.edu
IdentityFile  (location of the saved id_rsa.pub file from Quest)
User          (quest user login)
```

Save the file updates. This creates an alias for the login to Quest. The following command will tell ssh to log into the `user@quest.northwestern.edu` using the public key stored at the location given in `IdentityFile`

```
ssh quest
```

If this results in a successful login, then the SSH aliasing is successful and can be used for VSCode remote connects too.

### Windows Based OS

The instructions for adding an SSH config file in the Windows OS follows the same process as above, except the `.ssh` folder will need to be created in  `C:\Users\YOURNAME\` and the config file will be in `C:\Users\YOURNAME\.ssh`

## VSCode Remote Access

If the extensions in VSCode were installed correctly, the lower left corner should have a green tab. Clicking on the tab gives a drop down on which host to connect to. VSCode looks for a config file and prompts the user to instruct the correct server to connect to. If the config file in `.ssh` was created properly, VSCode will be able to screen the `quest.northwestern.edu` as a legitimate server and it will be displayed as is alias. 

VSCode will connect to the selected host and now all file updates made in VSCode will be directly made on Quest.

## Terminal Access

Within VSCode, `Ctrl+J` will open a panel that includes a tab called `TERMINAL`. If VSCode is logged into Quest remotely, the terminal prompt will be automatically logged into the Quest server. Any command issued is a command issued on the Quest server.

### SLURM

In [2-basic-quest-cluster](https://github.com/bstadie/rl_starter_kit/tree/main/2-basic-quest-cluster#readme) there is instruction on how to set up a virtual environment on Quest, and how to create and monitor jobs in SLURM. 

To make this process more convenient, navigate to the active directory where work is being done via terminal on VSCode with `cd path/to/directory`. Issuing the following command in terminal will send a job to SLURM as specified by `jobSubmission.sh`

```
sbatch jobSubmission.sh
```

The following allows for monitoring all jobs and provides ids for each job running on SLURM:

```
squeue -u [username]
```

The following cancels any job based on id:

```
scancel [job id]
```

All commands as listed in 2-basic-quest-cluster will work on this terminal, while any text editing can easily be done on VSCode.


### Todo

- [x] Introduction to VSCode extensions
- [x] SSH config file
- [x] Terminal view
- [ ] log files update real time

