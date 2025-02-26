# EHR Regulatory News Summarization App

This application fetches and summarizes the latest EHR regulatory and interoperability news using OpenAI's GPT API and displays it via a Dash-based web interface. It's designed for healthcare IT professionals, EHR developers, and compliance officers who need to stay updated on regulatory changes and industry trends.

## Features

- **Categorized News Retrieval**: Automatically fetches news from multiple healthcare IT categories:
  - Regulatory & Compliance (ONC, HHS, CMS, EHR certification)
  - FHIR & Interoperability (HL7 FHIR, SMART on FHIR, health data exchange)
  - Government Policies (Executive Orders, Federal Register, healthcare policy)
  - AI in Healthcare (AI/ML applications, predictive analytics, automation)
  - Market Trends (EHR vendors, health tech startups, M&A activity)

- **AI-Powered Summarization**: Uses OpenAI's GPT models to create concise, relevant summaries of complex healthcare IT news.

- **User-Friendly Interface**: Clean, responsive web interface with categorized summaries and loading indicators.

## Installation

### Prerequisites
- Python 3.8+
- An OpenAI API key
- A News API key

### Steps

1. **Clone this repository**:
   ```sh
   git clone https://github.com/your-repo/ehr-news-summarizer.git
   cd ehr-news-summarizer
   ```

2. **Set up a virtual environment**:
   ```sh
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   - On macOS and Linux:
     ```sh
     source venv/bin/activate
     ```
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```

4. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

5. **Create an environment file**:
   - Copy the `.env.example` file to `.env`
   - Add your API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key
     NEWS_API_KEY=your_news_api_key
     ```

## Running the Application

1. **Start the application**:
   ```sh
   python app.py
   ```
   - To use a different port (if 8050 is in use):
     ```sh
     python app.py --port 8051
     ```

2. **Access the dashboard**:
   - Open your web browser and navigate to `http://localhost:8050` (or the port you specified)
   - Click the "Fetch Latest News" button to retrieve and summarize the latest healthcare IT news

## How It Works

1. The application sends targeted queries to the News API to fetch relevant healthcare IT news articles.
2. Articles are categorized and filtered to ensure relevance to healthcare IT.
3. OpenAI's GPT model summarizes the news by category, focusing on the most important updates for EHR developers.
4. The summarized information is presented in a clean, organized interface.

## Customization

You can customize the news categories and search queries by modifying the `categories` dictionary in the `fetch_health_it_news` function in `app.py`.

## Troubleshooting

- **API Key Issues**: Ensure your API keys are correctly set in the `.env` file.
- **Port Conflicts**: If port 8050 is already in use, specify a different port using the `--port` parameter.
- **No News Found**: Check your internet connection and verify that your News API key is valid.

## License

[Your License Information]

## Acknowledgements

- [OpenAI](https://openai.com/) for providing the GPT API
- [News API](https://newsapi.org/) for the news retrieval service
- [Dash](https://dash.plotly.com/) for the web application framework
