# **Get Access to Quest**
https://app.smartsheet.com/b/form/797775d810274db5889b5199c4260328

Fill out the form to get the access to Bradly's Quest allocation. 

**Note: Before requesting, make sure to ask Bradly for the proper allocation number!**

After several days you will receive your Quest account activation. The username and password are the same with your NetID and password. 

# Check Your Connection to the Cluster

Take following steps in your terminal:

ssh bcs516@quest.northwestern.edu    # This should be replaced with your netid 

git clone https://github.com/bstadie/rl_starter_kit.git

cd 2-basic-quest-cluster

python basic_test.py



Confirm the test log is there.


vim test_log.txt    #You can use either text editor like VIM, or directly open it in Pycharm.

read the contents 

exit (escape, q!, enter)



rm test_log.txt

vim jobSubmissionTest.sh



The account is currently = XXXX

Replace it with: <project name>

exit (escape, wq)

sbatch jobSubmissionTest.sh

Confirm the job submits and outputs test_log.txt


![](SbatchCheck.png)



After confirming, we are able to run the RL code from 1-local-rl-coding.

![](DQNStart.png)

# Debugging Quest Cluster
Type the following command into terminal to create an interactive session. You can test eveything to your environment in this session.

```
srun -N 1 -n 1 --account=<account> --mem=<memory>G --partition=<partition> --time=<hh:mm:ss> --pty bash -l
```

#Remember to change <> subjects with everything you want.

For example, 
```
srun -N 1 -n 1 --account=p31777 --mem=12G --partition=short --time=00:40:00 --pty bash -l
```
