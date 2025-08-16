# Omni.gg Project

## Project Overview
**Omni.gg** is a web application designed to provide analytics, statistics, and strategy tools for fps gamers. The platform allows users to:  
- View player stats dashboards  
- Compare player performance  
- Access premium features like detailed weapon analytics and map insights  

The application is built using **Python, Streamlit, MySQL**, and **Docker** for containerized deployment.

---

## Link to Video
https://youtu.be/1Tm40zkdA8w 


## Team Members
Elisabeth Chen
Khanh Hoang
Aiza Padhiary
Jeffrey Vittini Ruiz
Yuna Ryu


## Prerequisites
- A GitHub Account
- A terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.
- VSCode with the Python Plugin installed
- A distribution of Python running on your laptop. The distribution supported by the course is Anaconda or Miniconda.
  - Create a new Python 3.11 environment in conda named `db-proj` by running:  
     ```bash
     conda create -n db-proj python=3.11
     ```
  - Install the Python dependencies listed in `api/requirements.txt` and `app/src/requirements.txt` into your local Python environment. You can do this by running `pip install -r requirements.txt` in each respective directory.


## Structure
- The repo is organized into five main directories:
  - `./app` - the Streamlit app
  - `./api` - the Flask REST API
  - `./database-files` - SQL scripts to initialize the MySQL database
  - `./datasets` - folder for storing datasets

- The repo also contains a `docker-compose.yaml` file that is used to set up the Docker containers for the front end app, the REST API, and MySQL database. 


## Setting Up The Repo
1. Clone this repo to your local machine.
   1. You can do this by clicking the green "Code" button on the top right of the repo page and copying the URL. Then, in your terminal, run `git clone <URL>`.
   1. Or, you can use the GitHub Desktop app to clone the repo. See [this page](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-a-repository-from-github-to-github-desktop) of the GitHub Desktop Docs for more info. 
1. Open the repository folder in VSCode.
1. Set up the `.env` file in the `api` folder based on the `.env.template` file.
   1. Make a copy of the `.env.template` file and name it `.env`. 
   1. Open the new `.env` file. 
   1. On the last line, delete the `<...>` placeholder text, and put a password. Don't reuse any passwords you use for any other services (email, etc.) 
1. For running the testing containers (for your personal repo), you will tell `docker compose` to use a different configuration file than the typical one.  
   1. `docker compose up -d` to start all the containers in the background
   1. `docker compose down` to shutdown and delete the containers
   1. `docker compose up db -d` only start the database container (replace db with api or app for the other two services as needed)
   1. `docker compose stop` to "turn off" the containers but not delete them.
1. The one you will use for testing is `sandbox.yaml`.
   1. `docker compose -f sandbox.yaml up -d` to start all the containers in the background
   1. `docker compose -f sandbox.yaml down` to shutdown and delete the containers
   1. `docker compose -f sandbox.yaml up db -d` only start the database container (replace db with api or app for the other two services as needed)
   1. `docker compose -f sandbox.yaml stop` to "turn off" the containers but not delete them.


## User Roles
The code in this project demonstrates how to implement a simple Role-based Access Control (RBAC) system in Streamlit without using a user authentication (usernames and passwords). The Streamlit pages are split up among 4 roles - Casual Gamer, Data Analyst, Pro Gamer, and System Adminstrator.

- **Casual Gamer**: As a casual gamer, the user can view basic player stats, have an option of upgrading to a premium (and being able to view more advanced stats such as weapon analytics and map insights), and can compare their stats with others

- **Data Analyst**: As a data analyst for an E-sports team, the user can view player stats, weapon analytics, map insights, and can compare players with other players to assess how players perform

- **Pro Gamer**: As a pro gamer, the user can view player stats, weapon analytics, map insights, and can compare their stats with others to view and evaluate their performance

- **System Administrator**: As a system administrator, the user can manage roles, view the performance of users, and see anomalies to review data glitches or potential cheaters


## Planned Features
While the core functionality is in place, we have several features planned for future development to enhance the user experience.

### Goals and Milestones
The "Goals and Milestones" feature is designed to be a part of the application, allowing users to define, track, and manage key objectives.

**Current Status:**
Due to initial project time constraints, the core functionality for managing goals and milestones is not yet fully implemented. Users are currently able to view goals and milestones, but the interactive ability to modify them (editing, adding, and removing) is unavailable.

**Planned Features:**
- **Editing and Deletion:** Users will have full control to **edit**, **add**, and **remove** goals and milestones after they have been created.
- **Progress Tracking:** Future updates will include a more robust system for tracking and visualizing the progress of each goal.
- **Intuitive UI:** An interactive user interface will be developed to make the process of creating and managing goals and milestones seamless and efficient.

Video Link: https://youtu.be/1Tm40zkdA8w




