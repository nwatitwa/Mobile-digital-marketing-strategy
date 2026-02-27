# 📱 Consumer Mobile Behavior Analytics Dashboard

## Overview
This is a **fully functional Streamlit dashboard** designed to tell a compelling story about consumer mobile usage behaviors. It's specifically crafted to help marketing agencies understand digital consumer behavior patterns and develop data-driven marketing strategies.

## Features

### 🎯 The Story-Driven Narrative
The dashboard is structured as a flowing story in 5 parts:

1. **Part 1: The Behavioral Tapestry** - Four distinct consumer archetypes with unique marketing opportunities
2. **Part 2: Usage Patterns** - When and how consumers engage with their devices  
3. **Part 3: Content Consumption** - Deep dive into video engagement and content consumption
4. **Part 4: Marketing Opportunities** - Actionable insights and recommendations
5. **Part 5: Interactive Explorer** - Tools to dive deeper into the data

### 📊 Key Visualizations
- Consumer Segmentation (4 distinct personas)
- Daily & Weekly Usage Trends
- Category Distribution Analysis
- YouTube Engagement Deep Dive
- Correlation Analysis
- Interactive Data Explorer

### 👥 Consumer Personas Identified
1. **Highly Productive** (💼) - Work-focused professionals  
2. **Entertainment-Heavy** (🎬) - Content consumers
3. **Social-First** (👥) - Community-driven users
4. **Balanced** (⚖️) - Versatile across categories

## Installation & Setup

### Prerequisites
- Python 3.8+
- Streamlit
- Pandas
- Plotly

### Install Dependencies
```bash
pip install streamlit pandas numpy plotly scikit-learn scipy
```

### Run the Dashboard
```bash
streamlit run streamlit_dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## File Structure
```
├── streamlit_dashboard.py          # Main Streamlit application
├── Mobile_Usage_Analysis.ipynb      # Original analysis notebook (dashboard removed)
├── Data Raw/
│   └── screen_time_app_usage_dataset.csv  # Source data
└── README.md                        # This file
```

## What Changed

### From the Jupyter Notebook
The following components were **removed** from the notebook:
- Dashboard Creation Section (Section 8)
- 8-panel integrated visualization
- Key Insights & Summary sections

**These are now in the Streamlit app** where they can be:
- More interactive and engaging
- Better formatted for presenting to clients
- Easier to update and maintain
- More visually compelling

### The Streamlit App Includes
✅ Executive summary with key metrics  
✅ Four consumer persona profiles with strategic recommendations  
✅ Detailed usage pattern analysis  
✅ YouTube engagement deep dive  
✅ Actionable marketing recommendations  
✅ Interactive data explorer for custom analysis  
✅ Business-focused language and formatting  

## Marketing Story Arc

The dashboard tells a complete story for marketing agencies:

```
INTRODUCTION
↓
"Here are your 4 target consumer types..."
↓
"Here's when and how they engage..."
↓
"Here's what content drives engagement..."
↓
"Here's how to reach each segment..."
↓
ACTIONABLE INSIGHTS & STRATEGIES
```

## Key Insights for Agencies

**Segment Size & Characteristics:**
- Each segment represents different marketing approaches
- Different optimal timing for campaigns
- Different channel preferences
- Different content types that resonate

**Engagement Drivers:**
- Video content (YouTube) drives massive engagement
- Entertainment apps command 25%+ of screen time
- Social media is critical for community engagement
- Productivity apps show specific weekday patterns

**Campaign Recommendations:**
- Schedule ads during peak engagement times
- Create segment-specific messaging
- Invest in multi-platform campaigns
- Leverage video marketing heavily

## Data Source
- **3 months** of anonymized mobile usage data
- **100+ users** tracked daily
- **3000+ records** of app usage sessions
- Real consumer behavior patterns

## Technical Notes

- **Caching**: Data loading and processing is cached with `@st.cache_data` for performance
- **Interactive Filters**: Segment explorer, category analysis, and engagement filters
- **Responsive Design**: Works on desktop and tablet displays
- **Color Scheme**: Professional gradient design (#667eea primary color)

## Customization

You can customize the dashboard by:
1. Modifying segment definitions in `calculate_user_metrics()`
2. Adjusting color schemes in the CSS section
3. Changing marketing strategies in the tabs section
4. Adding new insights or metrics

## Troubleshooting

**Issue**: Dashboard won't load  
**Solution**: Ensure all dependencies are installed and data file path is correct

**Issue**: Visualizations are slow  
**Solution**: The app uses caching - first load may be slower, subsequent loads are fast

**Issue**: Missing data in explorers  
**Solution**: Check that `Data Raw/screen_time_app_usage_dataset.csv` is in the correct location

## Contact & Support
For questions or customizations, refer to the analysis in `Mobile_Usage_Analysis.ipynb` for the underlying data processing logic.

---
**Created for**: Marketing agencies seeking to understand consumer mobile behaviors  
**Data Coverage**: January 1 - March 31, 2024 (90 days)  
**Technology**: Streamlit + Plotly + Pandas
