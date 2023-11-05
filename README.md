# MarioKart8-Gym-Env
A MarioKart8 OpenAI Gym environment for reinforcement learning projects.

# Coming soon
This project was completed on 03/2023 as a personal project first. I managed to train an agent that beat the hardest CPU in a few hundred hours of play (ingame time).

Now, I'll try to publish an easy-to-read and reproducible version of this project with the aim of serving as an example of "HowTo" transform Switch games into a Gym environment for RL applications.

The agent will be published in other repository.

I will release the code when I find time to clean / comment my actual private repo.

# Currently released

The server part is currently available.
In short, the server lets you run an instance of the emulated game and expose the game's internal state and RGB image on an MQTT server.
Then a client (based on MQTT) can interact with the game remotely. (The client is not yet released).

The code is provided as is, this version is not yet tested and may not work. When everything is complete, I'll explain how to configure the project step by step and how the project architecture actually works in details.