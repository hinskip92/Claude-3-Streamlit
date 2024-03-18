## Overview

This project is a multimodal chat project for the Claude-3 API that enables you to switch between models, enter a system message, as well as upload images.

## Getting Started

To get this project up and running on your local machine, follow these steps:

### Prerequisites

- Ensure you have Python installed on your system. You can download Python from [here](https://www.python.org/downloads/).
- An API key is required to access the external services used by this project.

### Installation

1. Clone the repository to your local machine:

`git clone https://github.com/hsinskip92/Claude-3-Streamlit.git`

2. Navigate to the project directory:

`cd your-repo-name`

3. Install the required dependencies:

`pip install -r requirements.txt`

### Setting Up Your API Key

Before running the application, you need to add your API key to your environment variables:

1. Obtain an API key from Anthropic.
2. Set the ANTHROPIC_API_KEY key as an environment variable. Replace `YOUR_API_KEY` with your actual API key.
3. The application is configured to read this environment variable for secure API access.

## Run the app

`streamlit run app.py`


