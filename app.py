import os
import requests
import openai
from dotenv import load_dotenv
import dash
from dash import html, dcc, Input, Output
from dash.dependencies import State
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Define categories and their search queries
CATEGORIES = {
    "EHR News": "EHR OR 'Electronic Health Records' OR 'EHR systems' OR 'EHR implementation'",
    "Healthcare Technology": "healthcare technology OR digital health",
    "Medical Research": "medical research OR clinical trials",
    "Health Policy": "health policy OR healthcare reform",
    "Pharmaceuticals": "pharmaceuticals OR drug development",
    "Public Health": "public health OR disease prevention"
}

# Function to fetch recent health news
def fetch_health_news(selected_categories, search_term=None):
    url = "https://newsapi.org/v2/everything"
    all_articles = []
    
    # If no categories selected and no search term, return empty list
    if not selected_categories and not (search_term and search_term.strip()):
        return []
    
    # If search term is provided, include it in the query
    search_query = f"{search_term} AND " if (search_term and search_term.strip()) else ""
    
    # If no categories selected, just use the search term
    if not selected_categories:
        categories = ["Search Results"]
        query = f"{search_query}(healthcare OR health OR medical OR EHR OR EMR OR technology OR business)"
    else:
        categories = selected_categories
        # Build query with search term (if any) and categories
        query = search_query + " OR ".join([f"({CATEGORIES[cat]})" for cat in categories if cat in CATEGORIES])
        query += " AND (healthcare OR health OR medical OR EHR OR EMR)"
    
    # Fetch articles
    for category in categories:
        # Skip if category doesn't exist (for search-only queries)
        if category != "Search Results" and category not in CATEGORIES:
            continue
        
        params = {
            "q": query,
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5  # Limit to 5 articles for search, 3 for categories
        }
        
        logging.debug(f"Fetching news with query: {query}")
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            
            # Add category to each article
            for article in articles:
                article['category'] = category
                all_articles.append(article)
            
            logging.debug(f"Found {len(articles)} articles")
                
        except Exception as e:
            logging.error(f"Error fetching news: {str(e)}")
            continue
    
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
    content = "Please summarize the following news articles. For each article, provide a concise bullet point that captures the main point. Focus on the key information that would be relevant to healthcare professionals and IT staff. If the article is about a specific company or technology, mention that. Keep each bullet point to 1-2 sentences maximum.\n\n"
    
    for category, category_articles in articles_by_category.items():
        content += f"## {category}\n"
        for article in category_articles[:5]:  # Limit to 5 articles per category
            title = article.get('title', 'No title')
            description = article.get('description', 'No description available')
            content += f"Title: {title}\nDescription: {description}\n\n"
    
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    # Create a chat completion
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news articles in a clear, concise bullet-point format. Focus on extracting the most important information from each article and present it in an easy-to-scan format. Each bullet point should be 1-2 sentences maximum. If the article is about a specific company, technology, or development, highlight that at the beginning of the bullet point."},
                {"role": "user", "content": content}
            ],
            temperature=0.3  # Lower temperature for more focused, deterministic output
        )
        
        # Extract and format the response content
        summary = response.choices[0].message.content
        
        # Ensure the summary is properly formatted with bullet points
        if not summary.startswith(('•', '-', '*')):
            # If the response doesn't start with bullets, add them
            points = [p.strip() for p in summary.split('\n') if p.strip()]
            summary = '\n'.join(f"• {p}" for p in points)
            
        return summary
        
    except Exception as e:
        logging.error(f"Error generating summary: {str(e)}")
        return "Error generating summary. Please try again later."

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Healthcare News Summarizer", style={'textAlign': 'center', 'color': '#2c3e50'}),
        
        # Search Section
        html.Div([
            html.H3("Search for Specific Terms:", style={'marginBottom': '10px'}),
            dcc.Input(
                id='search-term',
                type='text',
                value='',  # Ensure controlled input
                placeholder='e.g., Apple, MSFT, Epic EHR',
                style={
                    'width': '100%',
                    'padding': '10px',
                    'marginBottom': '20px',
                    'border': '1px solid #ddd',
                    'borderRadius': '4px',
                    'fontSize': '16px'
                }
            ),
            html.Div(style={'height': '20px'}),  # Spacer
            
            # Categories Section
            html.Div([
                html.H3("Or Select Categories:", style={'marginBottom': '10px'}),
                dcc.Checklist(
                    id='category-selector',
                    options=[{'label': cat, 'value': cat} for cat in CATEGORIES.keys()],
                    value=[],
                    labelStyle={
                        'display': 'inline-block',  # Changed from 'block' to 'inline-block'
                        'width': 'auto',  # Explicitly set width
                        'minWidth': '200px',  # Add minimum width
                        'margin': '8px 0',
                        'padding': '8px',
                        'borderRadius': '4px',
                        'backgroundColor': '#f8f9fa',
                        'cursor': 'pointer'
                    }
                ),
            ]),
            
            # Fetch Button
            html.Div(style={'height': '20px'}),  # Spacer
            html.Button(
                'Fetch News',
                id='fetch-news',
                n_clicks=0,
                type='button',
                disabled=True,
                className='fetch-button',
                style={
                    'width': '100%',
                    'padding': '12px',
                    'backgroundColor': '#4a89dc',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '4px',
                    'fontSize': '16px',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'position': 'relative',
                    'zIndex': '1',
                    'overflow': 'hidden',
                    'outline': 'none'
                }
            ),
        ], style={
            'maxWidth': '800px',
            'margin': '0 auto',
            'padding': '20px',
            'backgroundColor': 'white',
            'borderRadius': '8px',
            'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
        }),
        
        # Loading and Results Section
        dcc.Loading(
            id="loading-1",
            type="default",
            style={'marginTop': '20px'},
            children=html.Div(id="loading-output-1"),
        ),
        
        html.Div(id='news-output', style={'marginTop': '30px'}),
        html.Div(id='summary-output', style={'marginTop': '30px'}),
        
        # Store for articles data
        dcc.Store(id='articles-store')
    ], style={
        'fontFamily': 'Arial, sans-serif',
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'backgroundColor': '#f5f7fa'
    })
])

# Enable/disable fetch button based on selection or search term
@app.callback(
    [Output('fetch-news', 'style'),
     Output('fetch-news', 'disabled')],
    [Input('category-selector', 'value'),
     Input('search-term', 'value')]
)
def update_button(selected_categories, search_term):
    # Enable if either categories are selected or search term is provided
    has_categories = selected_categories and len(selected_categories) > 0
    has_search = search_term and search_term.strip()
    has_input = has_categories or has_search
    
    logging.debug(f"update_button - has_categories: {has_categories}, has_search: {has_search}")
    
    button_style = {
        'width': '100%',
        'padding': '12px',
        'border': 'none',
        'borderRadius': '4px',
        'fontSize': '16px',
        'cursor': 'pointer' if has_input else 'not-allowed',
        'transition': 'all 0.3s',
        'backgroundColor': '#4a89dc' if has_input else '#e9ecef',
        'color': 'white' if has_input else '#adb5bd',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }
    
    # Add hover effect only when button is enabled
    if has_input:
        button_style.update({
            ':hover': {
                'backgroundColor': '#357bd8',
                'boxShadow': '0 4px 8px rgba(0,0,0,0.15)',
                'transform': 'translateY(-1px)'
            },
            ':active': {
                'transform': 'translateY(0)',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            }
        })
    
    return button_style, not has_input

# Fetch and display news
@app.callback(
    [Output('news-output', 'children'),
     Output('summary-output', 'children'),
     Output('articles-store', 'data')],
    [Input('fetch-news', 'n_clicks')],
    [State('category-selector', 'value'),
     State('search-term', 'value')],
    prevent_initial_call=True
)
def fetch_and_display_news(n_clicks, selected_categories, search_term):
    # Get the callback context to see what triggered the update
    ctx = dash.callback_context
    if not ctx.triggered:
        logging.error("Callback triggered but no context available")
        return "Error: No callback context available.", "", None
        
    # Log what triggered the callback
    trigger_component = ctx.triggered[0]['prop_id'].split('.')[0]
    logging.debug(f"Callback triggered by: {trigger_component}, n_clicks: {n_clicks}")
    logging.debug(f"Selected categories: {selected_categories}")
    logging.debug(f"Search term: {search_term}")
    
    # Check if we have either categories selected or a search term
    has_categories = selected_categories and len(selected_categories) > 0
    has_search = search_term and search_term.strip()
    
    # If no input, return early
    if not has_categories and not has_search:
        logging.warning("No categories selected and no search term provided")
        return "Select categories or enter a search term and click 'Fetch News' to begin.", "", None
    
    try:
        # Fetch articles based on selection or search
        articles = fetch_health_news(selected_categories or [], search_term)
        
        if not articles:
            return "No articles found. Please try different categories or search terms.", "", None
        
        # Display articles with category labels
        news_output = []
        for article in articles:
            news_output.append(
                html.Div([
                    # Category/Search label
                    html.Div([
                        html.Span(
                            article['category'],
                            style={
                                'background-color': '#4a89dc',
                                'color': 'white',
                                'padding': '4px 12px',
                                'border-radius': '12px',
                                'font-size': '0.8em',
                                'fontWeight': '500',
                                'display': 'inline-block',
                                'marginBottom': '10px'
                            }
                        ),
                    ]),
                    
                    # Article title
                    html.H3(
                        article.get('title', 'No title'), 
                        style={
                            'margin': '0 0 10px 0',
                            'color': '#2c3e50',
                            'fontSize': '1.3em',
                            'lineHeight': '1.4'
                        }
                    ),
                    
                    # Article description
                    html.P(
                        article.get('description', 'No description available'),
                        style={
                            'color': '#555',
                            'margin': '0 0 15px 0',
                            'lineHeight': '1.6'
                        }
                    ),
                    
                    # Read more link
                    html.Div(
                        html.A(
                            'Read full article →', 
                            href=article.get('url', '#'), 
                            target='_blank',
                            style={
                                'color': '#4a89dc',
                                'textDecoration': 'none',
                                'fontWeight': '500',
                                'display': 'inline-block',
                                'transition': 'all 0.2s',
                                ':hover': {
                                    'color': '#2a6fc9',
                                    'textDecoration': 'underline'
                                }
                            }
                        ),
                        style={'marginBottom': '25px'}
                    ),
                    
                    # Divider
                    html.Hr(style={
                        'border': 'none',
                        'height': '1px',
                        'backgroundColor': '#eee',
                        'margin': '20px 0'
                    })
                ], 
                style={
                    'backgroundColor': 'white',
                    'padding': '25px',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                    'marginBottom': '20px',
                    'transition': 'transform 0.2s, box-shadow 0.2s',
                    ':hover': {
                        'transform': 'translateY(-2px)',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.1)'
                    }
                })
            )
        
        # Generate summary of all articles
        summary = summarize_news(articles)
        
        # Format the summary with proper line breaks and bullet points
        summary_content = []
        if summary:
            # Split the summary into lines and format as list items
            lines = [line.strip() for line in summary.split('\n') if line.strip()]
            for line in lines:
                # Remove any existing bullet points and add our own consistent ones
                clean_line = line.lstrip('•-* ').strip()
                if clean_line:  # Only add non-empty lines
                    summary_content.append(html.Li(clean_line, style={'marginBottom': '10px'}))
        
        # Create the summary output with proper styling
        summary_output = html.Div([
            html.H3(
                "AI-Generated Summary", 
                style={
                    'margin': '30px 0 20px 0',
                    'color': '#2c3e50',
                    'paddingBottom': '10px',
                    'borderBottom': '2px solid #f0f0f0'
                }
            ),
            html.Div(
                html.Ul(
                    summary_content,
                    style={
                        'listStyleType': 'none',
                        'paddingLeft': '15px',
                        'margin': '0',
                        'fontSize': '1.1em',
                        'lineHeight': '1.7',
                        'color': '#333'
                    }
                ),
                style={
                    'backgroundColor': 'white',
                    'padding': '25px',
                    'borderRadius': '8px',
                    'boxShadow': '0 2px 10px rgba(0,0,0,0.05)',
                    'borderLeft': '4px solid #0d6efd',
                    'fontSize': '16px',
                    'lineHeight': '1.6',
                    'marginTop': '20px'
                }
            )
        ]) if summary_content else html.Div()
        
        return news_output, summary_output, articles
        
    except Exception as e:
        error_msg = f"An error occurred while fetching news: {str(e)}"
        logging.error(error_msg)
        return error_msg, "", None

if __name__ == "__main__":
    app.run(debug=True, port=5002)
