# Healthcare IT News Summarizer

A modern web application that fetches and summarizes the latest healthcare IT, EHR, and regulatory news using OpenAI's GPT API. The app provides a clean, intuitive interface for healthcare IT professionals, developers, and decision-makers to stay informed about industry developments.

## ✨ Features

- **Flexible Search Options**:
  - Search by specific terms (e.g., company names, technologies)
  - Browse predefined categories
  - Combine search terms with categories for precise results

- **Comprehensive News Coverage**:
  - Regulatory & Compliance (ONC, HHS, CMS, EHR certification)
  - FHIR & Interoperability (HL7 FHIR, SMART on FHIR, health data exchange)
  - Government Policies (Executive Orders, Federal Register, healthcare policy)
  - AI in Healthcare (AI/ML applications, predictive analytics, automation)
  - Market Trends (EHR vendors, health tech startups, M&A activity)
  - EHR News (Electronic Health Records updates and developments)

- **AI-Powered Summarization**:
  - Concise, bullet-point summaries of complex healthcare IT news
  - Focus on key information and actionable insights
  - Context-aware processing of healthcare-specific terminology

- **Modern User Interface**:
  - Clean, responsive design
  - Interactive category selection
  - Real-time feedback during searches
  - Mobile-friendly layout
  - Intuitive search and filtering options

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- [OpenAI API key](https://platform.openai.com/)
- [News API key](https://newsapi.org/)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sum1Solutions/EHR-news-summarizer.git
   cd EHR-news-summarizer
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install all required packages including:
   - Dash 3.0.4
   - Flask 3.0.3
   - OpenAI 1.82.1+
   - Python-dotenv 1.1.0+
   - Other necessary dependencies

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   NEWS_API_KEY=your_newsapi_key_here
   ```

## 🖥️ Using the Application

1. **Start the server**:
   ```bash
   python app.py
   ```
   - The application runs on port 5002 by default
   - Access it at: http://127.0.0.1:5002/
   - Use `--port` to specify a different port if needed
   - Example: `python app.py --port 8051`

2. **Access the web interface**:
   - Open your browser to `http://localhost:5002` (or your specified port)
   - The application loads with search interface ready for use

### How to Search

1. **Search by term**:
   - Enter keywords in the search box (e.g., "Epic EHR", "Cerner")
   - Click "Fetch News" button
   - The button will be enabled when there's valid input

2. **Browse by category**:
   - Select one or more categories from the list
   - Click "Fetch News" button
   - The button will be enabled when at least one category is selected

3. **Combine search methods**:
   - Enter search terms AND/OR select categories
   - Click "Fetch News" to see combined results
   - The button will be enabled when there's any valid input

### Troubleshooting

- **Port already in use**: If you see a port conflict, either:
  - Terminate the existing process using the port:
    ```bash
    # On macOS/Linux
    lsof -i :5002 | grep LISTEN | awk '{print $2}' | xargs -r kill -9
    ```
  - Or start the app on a different port:
    ```bash
    python app.py --port 8051
    ```

- **Missing dependencies**: If you encounter import errors:
  ```bash
  pip install -r requirements.txt
  ```

- **API key issues**: Ensure your API keys are correctly set in the `.env` file and have proper permissions.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Dash](https://dash.plotly.com/) and [Flask](https://flask.palletsprojects.com/)
- Powered by [OpenAI](https://openai.com/) and [News API](https://newsapi.org/)
- Icons by [Font Awesome](https://fontawesome.com/)

### Understanding the Results

- Articles are displayed with source, title, and summary
- AI-generated summaries appear below the article list
- Click "Read full article" to view the original source

## 🛠️ Development

### Customization

1. **Modify categories**:
   Edit the `CATEGORIES` dictionary in `app.py` to add or modify news categories and their search queries.

2. **Adjust summarization**:
   Modify the `summarize_news` function to change how articles are processed and summarized.

3. **UI Customization**:
   The application uses Dash with custom CSS. Edit the layout in `app.py` to change the appearance.

### Troubleshooting

| Issue | Solution |
|-------|----------|
| API Key Errors | Verify keys in `.env` and ensure they're properly quoted |
| No Results | Check your internet connection and API key limits |
| Port in Use | Use `--port` flag to specify a different port |
| Module Not Found | Run `pip install -r requirements.txt` |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [OpenAI](https://openai.com/) - For the powerful GPT API
- [News API](https://newsapi.org/) - For comprehensive news coverage
- [Dash](https://dash.plotly.com/) - For the reactive web framework
- [Plotly](https://plotly.com/) - For visualization components

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
