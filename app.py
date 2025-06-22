import os
import requests
import openai
from dotenv import load_dotenv
import dash
from dash import html, dcc
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Function to fetch recent health IT news
def fetch_health_it_news():
    url = "https://newsapi.org/v2/everything"
    
    # Define categories and their search queries
    categories = {
        "Regulatory & Compliance": "ONC OR 'Health IT' OR HealthIT.gov OR USCDI OR 'FHIR compliance' OR 'HHS regulations' OR CMS OR 'EHR certification' OR 'healthcare compliance' OR 'EHR regulations'",
        "FHIR & Interoperability": "FHIR OR 'HL7 FHIR' OR 'FHIR R5' OR 'SMART on FHIR' OR 'healthcare interoperability' OR 'health data exchange' OR 'EHR interoperability'",
        "Government Policies": "'healthcare Executive Order' OR 'healthcare Federal Register' OR 'healthcare policy' OR 'White House healthcare' OR 'HHS policy' OR 'healthcare regulation'",
        "AI in Healthcare": "'AI healthcare' OR 'machine learning healthcare' OR 'OpenAI healthcare' OR 'LLM healthcare' OR 'predictive analytics EHR' OR 'AI medical' OR 'healthcare automation'",
        "Market Trends": "'Epic EHR' OR 'Cerner EHR' OR 'Athenahealth EHR' OR 'Meditech EHR' OR 'EHR vendor' OR 'health tech startup' OR 'healthcare investment' OR 'healthcare M&A'"
    }
    
    all_articles = []
    
    # Fetch articles for each category
    for category, query in categories.items():
        params = {
            "q": query + " AND (healthcare OR health OR medical OR EHR OR EMR)",  # Add healthcare context to all queries
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5  # Limit to 5 articles per category
        }
        
        logging.debug(f"Fetching news for category: {category} with query: {query}")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            # Add category to each article
            for article in articles:
                article['category'] = category
            all_articles.extend(articles)
            logging.debug(f"Found {len(articles)} articles for category: {category}")
        else:
            logging.error(f"Failed to fetch articles for category {category}: {response.status_code}")
    
    # Sort all articles by published date (newest first)
    all_articles.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
    
    return all_articles

# Function to summarize news using ChatGPT
def summarize_news(articles):
    if not articles:
        return "No recent news found."
    
    # Group articles by category
    articles_by_category = {}
    for article in articles:
        category = article.get('category', 'Uncategorized')
        if category not in articles_by_category:
            articles_by_category[category] = []
        articles_by_category[category].append(article)
    
    # Create a structured content string with categories
    content = "Please summarize the following EHR regulatory and interoperability news by category. Focus ONLY on healthcare IT, EHR systems, and health technology news. Ignore any news not directly related to healthcare:\n\n"
    
    for category, category_articles in articles_by_category.items():
        content += f"## {category}\n"
        for article in category_articles[:3]:  # Limit to 3 articles per category
            content += f"- {article['title']}: {article.get('description', 'No description available')}\n"
        content += "\n"
    
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    # Create a chat completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in healthcare IT, EHR systems, and regulatory compliance. Summarize ONLY healthcare IT related news in a concise, informative manner for EHR developers and healthcare IT professionals. Ignore any news not directly related to healthcare IT, EHR systems, or health technology."},
            {"role": "user", "content": content}
        ]
    )
    
    # Extract the response content
    return response.choices[0].message.content

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("EHR Regulatory News Summary", style={'textAlign': 'center', 'marginBottom': '30px'}),
    html.Div([
        html.Button("Fetch Latest News", id="fetch-news-button", n_clicks=0, 
                   style={'backgroundColor': '#4CAF50', 'color': 'white', 'padding': '10px 20px',
                          'border': 'none', 'borderRadius': '4px', 'cursor': 'pointer'}),
        html.Div(id="loading-indicator", children=[
            html.Div(id="loading-text", children="", style={'marginLeft': '15px', 'display': 'inline-block'})
        ], style={'display': 'inline-block'})
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    html.Div(id="news-summary", style={'margin': '20px', 'padding': '15px', 'backgroundColor': '#f9f9f9', 'borderRadius': '5px'})
])

@app.callback(
    [dash.Output("news-summary", "children"),
     dash.Output("loading-text", "children")],
    [dash.Input("fetch-news-button", "n_clicks")]
)
def update_summary(n_clicks):
    logging.debug("Update summary called with n_clicks: %d", n_clicks)
    if n_clicks > 0:
        try:
            # Show loading message
            return html.Div("Fetching news..."), "Loading..."
        except Exception as e:
            logging.error("Error updating summary: %s", str(e))
            return html.Div("An error occurred while fetching the news summary."), ""
    return html.Div("Click the button to fetch the latest news summary."), ""

@app.callback(
    [dash.Output("news-summary", "children", allow_duplicate=True),
     dash.Output("loading-text", "children", allow_duplicate=True)],
    [dash.Input("fetch-news-button", "n_clicks")],
    prevent_initial_call=True
)
def fetch_and_display_news(n_clicks):
    if n_clicks > 0:
        try:
            articles = fetch_health_it_news()
            logging.debug(f"Fetched {len(articles)} total articles")
            
            if not articles:
                return html.Div("No recent news found."), ""
            
            summary = summarize_news(articles)
            logging.debug("Generated summary")
            
            # Convert markdown to HTML for better formatting
            summary_parts = summary.split('\n\n')
            summary_components = []

            for part in summary_parts:
                if part.startswith('##'):
                    # This is a category header
                    category = part.replace('##', '').strip()
                    summary_components.append(html.H3(category, style={'marginTop': '20px', 'color': '#2c3e50', 'fontWeight': 'bold'}))
                elif part.startswith('#'):
                    # Handle single # headers too
                    category = part.replace('#', '').strip()
                    summary_components.append(html.H3(category, style={'marginTop': '20px', 'color': '#2c3e50', 'fontWeight': 'bold'}))
                else:
                    # This is content
                    summary_components.append(html.P(part, style={'fontSize': '16px', 'lineHeight': '1.5'}))

            return html.Div(summary_components), ""
        except Exception as e:
            logging.error("Error fetching and displaying news: %s", str(e))
            return html.Div("An error occurred while processing the news."), ""
    return html.Div("Click the button to fetch the latest news summary."), ""

if __name__ == "__main__":
    app.run(debug=True, port=8051)
