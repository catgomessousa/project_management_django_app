# Production Planning Web App

A user-friendly production planning tool that dynamically generates a Gantt chart based on customer orders, tasks, and dependencies. Designed for small manufacturing companies, it provides a visual, interactive way to manage production schedules, along with a robust database for storing orders and customer information.

## Key Features

- **Dynamic Gantt Charts:** Easily visualize production timelines, dependencies, and order progress at a glance.
- **Centralized Database:** Store and manage customer orders, tasks, and related data in one place.
- **Easy Administration:** Manage data, update orders, and configure settings through a clean admin interface.
- **Scalable & Flexible:** Built with Django and modern frontend tooling, making it easy to adapt and extend.

## Screenshots

![front end](https://i.imgur.com/VTFvWRq.png)

![admin](https://i.imgur.com/CF4QnXU.png)


## How to run

### Prerequisites

- **Python 2.7**
- **Node.js & Yarn**

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/catgomessousa/project_management_django_app.git
   cd your-repo
2. **Set Up Python Dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Install Frontend Dependencies:**
   ```bash
   yarn install
4. **Build Frontend Assets:**
   ```bash
   yarn run dev
5. **Start the Development Server:**
   ```bash
   python manage.py runserver

