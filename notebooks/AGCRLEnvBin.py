import numpy as np
class AGCRLEnv:
    def __init__(self,observations,actions,action_parameter,action_space):
        """initialise action space, observation space & load data"""
        self.action_parameter=action_parameter
        self.action_space=action_space
        self.observations=observations
        self.actions=actions
        self.index=0
        self.teamindex=0
        self.observation_space=self.observations[self.teamindex].iloc[0].shape
        self.curr_obs=self.observations[self.teamindex].iloc[self.index]
        self.next_obs=self.curr_obs=self.observations[self.teamindex].iloc[self.index+1]
        self.curr_reward=0
        self.ep_reward=0
        self.interval=action_space[1]-action_space[0]
        
    def estimate_closest_as(self,value):
        return self.action_space[int(value)//int(self.interval)]
    
    def step(self,action):
        """
        return reward and next obs 
        """
        self.reward=self.rewardfunc(action)
        self.ep_reward+=self.reward
        self.index+=1
        cur_obs=self.curr_obs
        next_obs=self.next_obs
        if self.index>=len(self.observations[self.teamindex])-2:
            self.reset()
            return self.curr_obs,self.reward,True 
        self.curr_obs=self.observations[self.teamindex].iloc[self.index]
        self.next_obs=self.curr_obs=self.observations[self.teamindex].iloc[self.index+1]
        return self.curr_obs,self.reward,False
    
    def rewardfunc(self,action):
        """
        action with action at current index in action if equal positive or else negative
        """
#         print(self.action_space[action])
#         print(self.actions[self.teamindex]["assim_sp"][self.index])
        if(self.action_space[action]==self.estimate_closest_as(self.actions[self.teamindex]["assim_sp"][self.index])):
            return 100
        else:
            return 0
#             return -1*abs(self.action_space[action]-self.actions[self.teamindex]["assim_sp"][self.index])
    
    def reset(self):
        """
        set index to 0 and increment team index by 1 if greater than 4 go back to 0
        """
        self.teamindex+=1
        if self.teamindex>=5:
            self.teamindex=0
        self.index=0
        self.observation_space=self.observations[self.teamindex].iloc[0].shape
        self.curr_obs=self.observations[self.teamindex].iloc[self.index]
        self.next_obs=self.curr_obs=self.observations[self.teamindex].iloc[self.index+1]
        self.curr_reward=0
        self.ep_reward=0
        return self.curr_obs
        
    def resetinit(self):
        self.teamindex=0
        self.index=0
        self.observation_space=self.observations[self.teamindex].iloc[0].shape
        self.curr_obs=self.observations[self.teamindex].iloc[self.index]
        self.next_obs=self.curr_obs=self.observations[self.teamindex].iloc[self.index+1]
        self.curr_reward=0
        self.ep_reward=0
        return self.curr_obs