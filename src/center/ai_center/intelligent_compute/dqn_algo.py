import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

# Define the deep neural network
class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Experience replay buffer
class ReplayBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.position = 0

    def push(self, state, action, reward, next_state):
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        self.buffer[self.position] = (state, action, reward, next_state)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state = map(np.stack, zip(*batch))
        return state, action, reward, next_state

    def __len__(self):
        return len(self.buffer)

# Agent class
class Agent:
    def __init__(self, state_dim, action_dim, learning_rate=0.001, c=0.99, ε=1.0, ε_decay=0.995, ε_min=0.01, buffer_capacity=10000, batch_size=32):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.learning_rate = learning_rate
        self.c = c
        self.ε = ε
        self.ε_decay = ε_decay
        self.ε_min = ε_min
        self.buffer = ReplayBuffer(buffer_capacity)
        self.batch_size = batch_size

        self.model = DQN(state_dim, action_dim)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()

    def select_action(self, state):
        if random.random() < self.ε:
            return random.randint(0, self.action_dim - 1)
        else:
            state = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.model(state)
            action = torch.argmax(q_values).item()
            return action

    def learn(self):
        if len(self.buffer) < self.batch_size:
            return

        states, actions, rewards, next_states = self.buffer.sample(self.batch_size)
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions).unsqueeze(1)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)

        q_values = self.model(states).gather(1, actions).squeeze(1)
        next_q_values = self.model(next_states).max(1)[0].detach()
        target_q_values = rewards + self.c * next_q_values

        loss = self.criterion(q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        if self.ε > self.ε_min:
            self.ε *= self.ε_decay

# Simulated environment class
class CDNEnvironment:
    def __init__(self, state_dim):
        self.state_dim = state_dim

    def reset(self):
        return np.random.rand(self.state_dim)

    def step(self, action):
        next_state = np.random.rand(self.state_dim)
        reward = np.random.rand()
        return next_state, reward

# Main program
if __name__ == "__main__":
    # Assume the state dimension and action dimension
    state_dim = 20
    action_dim = 5

    agent = Agent(state_dim, action_dim)
    env = CDNEnvironment(state_dim)

    num_episodes = 1000
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        while not done:
            action = agent.select_action(state)
            next_state, reward = env.step(action)
            agent.buffer.push(state, action, reward, next_state)
            agent.learn()
            state = next_state
