import numpy as np
import common
import client
import gym



class EnvMarioKart8(gym.Env):
    '''
    OpenAI Gym environment to enable an RL agant to play Mario Kart 8 Deluxe on the Yuzu emulator.
    '''

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, host, port, target_instance, game_setup, callback_reset_game_setup, render_mode="rgb_array"):
        '''
        Instanciate one client instance.
        Call "start()" to connect the client.
        Parameters:
            host (str): IPv4 address of the MQTT server.
            port (int): TCP/IP Port of the MQTT server.
            target_instance (str): The id of the instance which the server is listening.
            game_setup (dict): An dict representing the wanted game state in the format:
                - MAIN_MODE                = common.GameSetup.MainMenu.<value>
                - GAME_MODE                = common.GameSetup.GameMode.<value>
                - PLAYER                   = common.GameSetup.Player.<value>
                - PLAYER_VARIANT           = common.GameSetup.Player.<value>.<value>
                - CAR_BODY                 = common.GameSetup.Car.Body.<value>
                - CAR_WHEEL                = common.GameSetup.Car.Wheel.<value>
                - CAR_WING                 = common.GameSetup.Car.Wing.<value>
                - RACE_RULE_MODE           = common.GameSetup.RaceRule.Mode.<value>
                - RACE_RULE_TEAMS          = common.GameSetup.RaceRule.Teams.<value>
                - RACE_RULE_ITEMS          = common.GameSetup.RaceRule.Items.<value>
                - RACE_RULE_COM            = common.GameSetup.RaceRule.COM.<value>
                - RACE_RULE_COM_VEHICLES   = common.GameSetup.RaceRule.COMVehicles.<value>
                - RACE_RULE_COURSES        = common.GameSetup.RaceRule.Courses.<value>
                - RACE_RULE_RACE_COUNT     = common.GameSetup.RaceRule.RaceCount.<value>
                - COURSE_CUP               = common.GameSetup.Course.Cup.<value>
                - COURSE                   = common.GameSetup.Course.Cup.Special.<value>
                - MAX_STEP                 = <int value> which represent max step to done before closing the game instance.
                See common.py to find what values exists.
            callback_reset_game_setup (callable): This callback is called when a reset command is sent by the agent.
                This callback is triggered just before the client reports the reset order to the server.
                It's therefore the ideal place to modify the game setup if you wish.
            render_mode (str): Set this option to "human" if you want to display a debug viewer to see what's currently happening in the game.
        Returns:
            An "EnvMarioKart8" OpenAI Gym environment.
        '''
        self.window_size = 128
        self.observation_space = gym.spaces.Dict(
            {
                'image': gym.spaces.Box(low=0, high=255, shape=(self.window_size, self.window_size, 3), dtype=np.uint8),
            }
        )
        self.action_space = gym.spaces.Dict(
            {
                'action': gym.spaces.Box(low=-1.0, high=1.0, shape=(7,), dtype=np.float32)
            }
        )
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        #
        self.game_setup = game_setup
        self.callback_reset_game_setup = callback_reset_game_setup
        #
        self.client = client.Client(host, port, target_instance)
        self.client.start()
        self.client.isReady.wait()
        #
        self._frame     = None
        self._last_lap  = None
        self._last_time = None
        #
        if self.render_mode == "human":
            cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            cv2.waitKey(10)

    def compute_reward(self):
        '''
        Example of a reward function. Feel free to edit this function to test your ideas.
        This function was used to train the "github.com/0xlouis/MarioKart8-Dreamer" agent.
        Returns:
            An float that represent the current step reward.
        '''
        coins   = self.client.step_coins # The Coin amount of the player [0;10]
        rank    = self.client.step_rank # The rank of the player [0;11] (0 mean first, 11 mean last)
        timer   = self.client.step_timer # The internal timer value of the game : 1 tick equal ~16.7ms (60fps)
        lap     = self.client.step_lap_continuous # Naive (sub-optimal) continuous position of the player on the track: generally in the interval [0;3] but technically [-inf;+inf]
        towing  = self.client.step_towing # Bugged, do not use. Should be 0 when the player get towed (this value also trigger when you use Piranha Plant).
        track   = self.client.step_track # The current track id (see common.py to use this value conveniently)
        
        # Calculate the biased speed ("biased" because this speed takes into account the absolute distance from the finish of the lap).
        # In this way, the speed becomes negative if the player drives in the opposite direction. And becomes attenuated in the neutral direction.
        # This is an important bias, since the right angle is NOT the optimal angle, and the agent has to find the "true" optimum angle on his own, despite the bias.
        # In practice, this isn't a problem : the agent also finds the cuts by itself, so it's not as bad as it sounds.
        try:
            coeff = common.INTERNAL_TRACK_TO_LAP_LENGHT[common.INTERNAL_TRACK_TO_ENUM[track]]
        except KeyError:
            coeff = 1.0
        if (self._last_lap is not None) and (self._last_time is not None):
            dt = timer - self._last_time
            if dt != 0:
                biased_speed = (coeff * (lap - self._last_lap)) / dt
            else:
                biased_speed = 0.0
        else:
            biased_speed = 0.0
        # Towing negative reward
        # if towing == 0:
        #     biased_speed = -2.0

        # Store old values to measure rate changes
        self._last_lap  = lap
        self._last_time = timer

        # Compute Rewards
        reward_speed    = biased_speed
        reward_coins    = coins
        reward_rank     = 12-(rank+1)
        
        # Aligning rewards through standardization: necessary to give meaning to weighting (see below)
        reward_speed    = (reward_speed - 7.0) / 2.0
        reward_coins    = (reward_coins - 8.503807297092868) / 1.8238985237638008
        reward_rank     = (reward_rank - 10.332045446636464) / 1.617004738635091

        # Reduce rewards with weighting
        if self.client.step_is_race_finish:
            reward = reward_rank * 100.0 # Last final reward if the race is finish (only the rank count)
        else:
            reward = (reward_speed * 0.625) + (reward_rank * 0.3125) + (reward_coins * 0.0625) # Weighted sum reduction 

        # print("*"*64)
        # print("reward           : {}".format(reward))
        # print("reward_speed     : {}".format(reward_speed))
        # print("reward_coins     : {}".format(reward_coins))
        # print("reward_rank      : {}".format(reward_rank))

        return reward

    def _get_obs(self):
        return {'image': self.render()}

    def _get_info(self):
        return {}

    def reset(self):
        '''
        Reset the environment.
        Returns:
            observation (dict): The current observation (the rgb frame of the game) in the format {'image':...}.
            info (dict): Always empty.
        '''
        super().reset()

        self._frame     = None
        self._last_lap  = None
        self._last_time = None

        self.callback_reset_game_setup(self)
        self.client.setup_game(self.game_setup)
        self.client.reset_game()
        self._frame = self.client.step_frame

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info

    def step(self, action):
        '''
        Make one step in the environment.
        Parameters:
            action (dict): IPv4 address of the MQTT server.
        Returns:
            observation (dict): An dict with an 'action' key with float value :
              [go_forward, go_backward, look_backward, throw_horn, bump_drift, go_x_direction, set_y_direction]
              Note : The float is casted to the bool value True if the scalar is > 0.0 then False.
            reward (float): The current reward.
            terminated (bool): If this is the terminal step.
            info (dict): Always empty.
        '''
        go_forward      = action['action'][0] > 0.0
        go_backward     = action['action'][1] > 0.0
        look_backward   = action['action'][2] > 0.0
        throw_horn      = action['action'][3] > 0.0
        bump_drift      = action['action'][4] > 0.0
        go_x_direction  = action['action'][5]
        set_y_direction = action['action'][6]

        self.client.action_game(go_forward, go_backward, go_x_direction, set_y_direction, look_backward, throw_horn, bump_drift)
        self._frame = self.client.step_frame

        observation = self._get_obs()
        info        = self._get_info()
        reward      = self.compute_reward()
        step_no     = self.client.step_no
        terminated  = self.client.step_terminal

        if self.render_mode == "human":
            self._render_frame()
        
        # if terminated:
        #     print("terminal", step_no)
        # else:
        #     print("step", step_no)

        return observation, reward, terminated, info

    def render(self):
        return self._render_frame()

    def _render_frame(self):
        if self.render_mode == "human":
            cv2.imshow("image", cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB))
            cv2.waitKey(10)
        return self._frame

    def close(self):
        pass


# Test / Debug
if __name__=="__main__":
    import joystic
    import common
    import random
    import cv2

    # Setup the game
    game_setup = {}
    game_setup['MAIN_MODE']                = common.GameSetup.MainMenu.SINGLE_PLAYER
    game_setup['GAME_MODE']                = common.GameSetup.GameMode.VS_RACE
    game_setup['PLAYER']                   = common.GameSetup.Player.MASKASS
    game_setup['PLAYER_VARIANT']           = common.GameSetup.Player.MaskassVariant.DEFAULT
    game_setup['CAR_BODY']                 = common.GameSetup.Car.Body.BIDDYBUGGY
    game_setup['CAR_WHEEL']                = common.GameSetup.Car.Wheel.ROLLER
    game_setup['CAR_WING']                 = common.GameSetup.Car.Wing.CLOUD_GLIDER
    game_setup['RACE_RULE_MODE']           = common.GameSetup.RaceRule.Mode.CC_150
    game_setup['RACE_RULE_TEAMS']          = common.GameSetup.RaceRule.Teams.NO_TEAMS
    game_setup['RACE_RULE_ITEMS']          = common.GameSetup.RaceRule.Items.FRANTIC_ITEMS
    game_setup['RACE_RULE_COM']            = common.GameSetup.RaceRule.COM.HARD
    game_setup['RACE_RULE_COM_VEHICLES']   = common.GameSetup.RaceRule.COMVehicles.ALL
    game_setup['RACE_RULE_COURSES']        = common.GameSetup.RaceRule.Courses.RANDOM
    game_setup['RACE_RULE_RACE_COUNT']     = common.GameSetup.RaceRule.RaceCount.FOUR
    game_setup['COURSE_CUP']               = common.GameSetup.Course.Cup.SPECIAL
    game_setup['COURSE']                   = common.GameSetup.Course.Cup.Special.RAINBOW_ROAD
    game_setup['MAX_STEP']                 = 3000

    # When the game is reset : Change setup to choose random rules.
    def callback_reset_game_setup(env):
      env.game_setup['RACE_RULE_MODE']    = random.choice([common.GameSetup.RaceRule.Mode.CC_150, common.GameSetup.RaceRule.Mode.MIRROR])
      env.game_setup['RACE_RULE_COURSES'] = common.GameSetup.RaceRule.Courses.CHOOSE
      env.game_setup['COURSE_CUP']        = random.randint(0, 11)
      env.game_setup['COURSE']            = random.randint(12, 15)

    env = EnvMarioKart8(host="192.168.27.66", port=1883, target_instance="01234567", game_setup=game_setup, callback_reset_game_setup=callback_reset_game_setup, render_mode="human")

    print("Init controller...")
    controller = joystic.JoysticPS2("/dev/input/by-id/usb-0810_USB_Gamepad-event-joystick")
    print("Init controller... OK")

    print("Reseting...")
    obs, nfo = env.reset()
    print("Reseting... OK")

    def human_policy(obs):
        action = {'action': controller.to_gym()}
        return action

    def random_policy(obs):
        go_forward      = random.randint(0,1)
        go_backward     = random.randint(0,1)
        go_x_direction  = (random.random()*2)-1
        set_y_direction = (random.random()*2)-1
        look_backward   = random.randint(0,1)
        throw_horn      = random.randint(0,1)
        bump_drift      = random.randint(0,1)
        action = {'action': [go_forward, go_backward, look_backward, throw_horn, bump_drift, go_x_direction, set_y_direction]}
        return action

    while True:
        act = human_policy(obs) # The RL agent is an Human with this line.
        # act = random_policy(obs) # The RL agent is an random with this line.
        # print(act)
        obs, rwd, end, nfo = env.step(act)
        # print(obs, rwd, end, nfo)
        if end:
            print("End of the episode.")
            print("Reseting...")
            env.game_setup = game_setup
            obs, nfo = env.reset()
            print("Reseting... OK")
