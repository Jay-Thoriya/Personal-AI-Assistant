# Personal AI Assistant

This is an AI-powered assistant that responds to questions about the user as if it were the user themselves. It's designed to answer personal questions about life story, superpowers, areas for growth, misconceptions, and how the user pushes boundaries.

## Features

- **Personal Responses**: The assistant responds as if it were you
- **Web Interface**: Easy-to-use Streamlit web application
- **Text-based Chat**: Simple and reliable text interface

## Setup

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Obtain an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
4. Add your API key to the `app.py` file (line 10)
5. Run the application:
   ```
   streamlit run app.py
   ```

## How to Use

1. Launch the application
2. Ask questions by typing in the chat input
3. View responses in the chat interface

## Example Questions

- What should we know about your life story in a few sentences?
- What's your #1 superpower?
- What are the top 3 areas you'd like to grow in?
- What misconception do your coworkers have about you?
- How do you push your boundaries and limits?

## Technology Stack

- **Streamlit**: Web application framework
- **OpenAI GPT-3.5**: Large language model for generating responses

## Customization

To personalize the assistant with your own information, edit the `personal_prompt` variable in the `app.py` file. Update the life story, superpower, areas to grow, misconception, and boundary-pushing sections with your own information.