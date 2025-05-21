# LinkedIn Post Generator

An AI-powered application to generate engaging LinkedIn posts with various features and customization options.

## Features

- Generate professional LinkedIn posts with different tones and styles
- Multiple language support (English and Hinglish)
- Customizable post length and structure
- Smart hashtag suggestions based on topics
- Emoji selector
- Post history tracking
- Copy to clipboard functionality
- Post metrics (character count, word count, line count)
- Best posting time recommendations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aayush992/Post-Generator.git
cd post_generator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run main.py
```

2. Open your browser and navigate to the provided URL (usually http://localhost:8501)

3. Select your preferences:
   - Choose a topic
   - Select tone and structure
   - Choose language
   - Adjust length
   - Add emojis and hashtags

4. Click "Generate Post" to create your LinkedIn post

5. Use the copy button to copy the generated post to your clipboard

## Data

The application uses a curated dataset of LinkedIn posts for better content generation. The data includes:
- Various topics (Technology, Career, Leadership, etc.)
- Different content styles
- Engagement metrics
- Language variations

## Contributing

Feel free to contribute to this project by:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.