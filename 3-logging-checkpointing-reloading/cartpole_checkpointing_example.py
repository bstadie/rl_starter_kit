# import packages
import wandb
import gym
import numpy as np
import matplotlib.pyplot as plt
import random
import torch.nn as nn
import torch

#set the Checkpoint file
PROJECT_NAME = 'resume_run'
CHECKPOINT_PATH = './checkpoint.tar'
NStates = 4
NActions = 2

run = wandb.init(project=PROJECT_NAME, resume=True)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# Define Pytorch Model
class QFunctionNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(QFunctionNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu1(out)
        out = self.fc2(out)
        out = self.relu2(out)
        out = self.fc3(out)
        return out


class ReplayBuffer:
    def __init__(self, mem_size=10000):
        self.mem_count = 0
        self.mem_size = mem_size
        self.states = np.zeros((mem_size, NStates), dtype=np.float32)
        self.actions = np.zeros(mem_size, dtype=np.int64)
        self.rewards = np.zeros(mem_size, dtype=np.float32)
        self.next_states = np.zeros((mem_size, NStates), dtype=np.float32)
        self.terminated = np.zeros(mem_size, dtype=np.bool)

    def add_to_buffer(self, state, action, reward, next_state, terminated):
        mem_index = self.mem_count % self.mem_size

        self.states[mem_index] = state
        self.actions[mem_index] = action
        self.rewards[mem_index] = reward
        self.next_states[mem_index] = next_state
        self.terminated[mem_index] = terminated

        self.mem_count += 1
        return True

    def sample_buffer(self, batch_size=32):
        # return 32 random points from the buffer.
        # sampling with replacement is okay.
        MEM_MAX = min(self.mem_count, self.mem_size)
        batch_indices = np.random.choice(MEM_MAX, batch_size, replace=True)

        states = self.states[batch_indices]
        actions = self.actions[batch_indices]
        rewards = self.rewards[batch_indices]
        states_ = self.next_states[batch_indices]
        dones = self.terminated[batch_indices]

        return states, actions, rewards, states_, dones


class QLearningAgent:
    def __init__(self, env, epsilon_greedy_threshold=0.50, epsilon_decay=0.995):
        #self.replayBuffer = ReplayBuffer()
        self.env = env
        self.q_func = QFunctionNet(input_size=NStates, num_classes=NActions, hidden_size=128).to(device)

        self.criterion = nn.MSELoss()
        #self.criterion = nn.SmoothL1Loss()
        #self.optimizer = torch.optim.RMSprop(self.q_func.parameters())
        self.optimizer = torch.optim.Adam(self.q_func.parameters(), lr=0.001)

        self.epsilon_greedy_threshold = epsilon_greedy_threshold
        self.epsilon_decay = epsilon_decay

        # learning rate
        #self.alpha = 0.5
        # discount factor
        self.gamma = 0.95

        self.total_training_steps = 0


    def train(self, states, acts, rews, next_states, terminated):
        states_torch = torch.from_numpy(states).float()
        acts_torch = torch.from_numpy(acts)
        #acts_torch = acts_torch.unsqueeze(1)
        next_states_torch = torch.from_numpy(next_states).float()
        rews_torch = torch.from_numpy(rews).float()
        terminated_torch = torch.from_numpy(terminated).float()

        batch_indices = np.arange(len(states), dtype=np.int64)

        q_values = self.q_func(states_torch)
        next_q_values = self.q_func(next_states_torch)

        predicted_value_of_actions_actually_taken = q_values[batch_indices, acts_torch]
        max_q_value_of_next_state = torch.max(next_q_values, dim=1)[0]

        q_target = rews_torch + self.gamma * max_q_value_of_next_state * (1-terminated_torch)


        loss = self.criterion(q_target, predicted_value_of_actions_actually_taken)

        #current_Q_values = self.q_func(states_torch)
        #current_Q_values_at_taken_actions = current_Q_values.gather(1, acts_torch)
        #next_q_values = self.q_func(next_states_torch)
        #max_of_next_q_values = next_q_values.max(1)[0]
        #max_of_next_q_values = max_of_next_q_values.detach()
        #target_Q_values = rews_torch + (self.gamma * max_of_next_q_values*terminated_torch)
        #loss = self.criterion(target_Q_values, current_Q_values_at_taken_actions)
        # Backward and optimize
        self.optimizer.zero_grad()
        loss.backward()

        #for param in self.q_func.parameters():
        #    param.grad.data.clamp_(-1, 1)

        self.optimizer.step()

        if self.total_training_steps % 1 == 0:
            #self.epsilon_greedy_threshold -= 0.05
            self.epsilon_greedy_threshold = max(self.epsilon_greedy_threshold * self.epsilon_decay, 0.01)
            #print(self.epsilon_greedy_threshold)

        self.total_training_steps += 1

    def get_action(self, obs, evaluate=False):
        obs_correct_format = torch.from_numpy(np.expand_dims(obs, 0))
        action_values = self.q_func(obs_correct_format)
        action_values = action_values.cpu().detach().numpy()[0]
        if evaluate is False:
            p = random.uniform(0, 1)
            if p > self.epsilon_greedy_threshold:
                action = np.argmax(action_values)
            else:
                action = self.env.action_space.sample()
            return action
        else:
            action = np.argmax(action_values)
            return action


def plot_fancy(steps_survived_history):
    plt.figure(2)
    plt.clf()
    #durations_t = torch.FloatTensor(episode_durations)
    steps_survived_history_torch = torch.FloatTensor(steps_survived_history)
    plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(np.array(steps_survived_history))
    # take 100 episode averages and plot them too
    if len(steps_survived_history) >= 20:
        means = steps_survived_history_torch.unfold(0, 20, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(19), means))
        plt.plot(means.numpy())

    plt.pause(0.001)  # pause a bit so that plots are updated


def main():
    env = gym.make('CartPole-v1')
    env.action_space.seed(42)
    env.observation_space.seed(42)

    #obs, info = env.reset()
    obs = env.reset()

    replay_buffer = ReplayBuffer()
    q_learning_agent = QLearningAgent(env=env)

    epochs = 2000
    ep = 0
    steps_survived = 0

    # Resume the run
    if wandb.run.resumed:
        #checkpoint = torch.load(wandb.restore(CHECKPOINT_PATH))
        checkpoint = torch.load(CHECKPOINT_PATH)
        q_learning_agent.q_func.load_state_dict(checkpoint['model_state_dict'])
        q_learning_agent.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        ep = checkpoint['ep']
        steps_survived = checkpoint['steps_survived']

    while ep < epochs:
        #obs, info = env.reset()
        obs = env.reset()

        terminated = False

        while not terminated:

            action = q_learning_agent.get_action(obs=obs)

            #next_obs, reward, terminated, truncated, info = env.step(action)
            next_obs, reward, terminated, info = env.step(action)

            replay_buffer.add_to_buffer(state=obs, action=action,
                                        reward=reward, next_state=next_obs,
                                        terminated=terminated)

            obs = next_obs

            steps_survived += 1

            if steps_survived > 450:
                break

        if(len(replay_buffer.states)) > 100:
            for i in range(0, 20):
                states_mb, acts_mb, rews_mb, next_states_mb, terminated = replay_buffer.sample_buffer(batch_size=32)
                q_learning_agent.train(states_mb, acts_mb, rews_mb, next_states_mb, terminated)

        if ep % 7 == 0 and ep > 0:

            steps_survived = 0
            #obs, info = env.reset()
            obs = env.reset()
            terminated = False
            while not terminated:
                steps_survived += 1
                action = q_learning_agent.get_action(obs=obs, evaluate=True)
                #next_obs, reward, terminated, truncated, info = env.step(action)
                next_obs, reward, terminated, info = env.step(action)
                obs = next_obs
                if steps_survived > 450:
                    break
            wandb.log({'ep': ep, 'steps_survived': steps_survived})

            # Save our checkpoint loc
            torch.save({
               'ep':ep,
               'steps_survived': steps_survived,
               'optimizer_state_dict': q_learning_agent.optimizer.state_dict(),
               'model_state_dict': q_learning_agent.q_func.state_dict()
            }, CHECKPOINT_PATH)

            print(steps_survived)

            # saves checkpoint to wandb
            wandb.save(CHECKPOINT_PATH)
        ep += 1



if __name__ == "__main__":
    main()




