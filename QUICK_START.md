# 🚀 QUICK START GUIDE

## Installation & Launch (2 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Dashboard
```bash
streamlit run streamlit_dashboard.py
```

### Step 3: View in Browser
The app will automatically open at `http://localhost:8501`

---

## What You'll See

### Executive Summary
Key metrics upfront: Total Users, Avg Daily Screen Time, Productive Usage %, YouTube Views

### 4 Consumer Personas
- 💼 **Highly Productive** (40%+ productivity app usage)
- 🎬 **Entertainment-Heavy** (35%+ entertainment consumption)  
- 👥 **Social-First** (35%+ social media usage)
- ⚖️ **Balanced** (distributed across all)

Each persona includes:
- Percentage of user base
- Description
- Recommended marketing strategy
- Optimal channels & content types

### Usage Patterns & Timing
- Daily trend visualization (90-day journey)
- Weekly patterns (which days see peak engagement)
- Category distribution over time
- Optimal ad timing recommendations

### Content Engagement
- YouTube engagement metrics
- Correlation analysis (what drives views/engagement)
- Screen time vs views relationship
- Interactive filters to explore deeper

### Segment Explorer
- Filter by consumer segment
- View segment-specific metrics  
- Explore screen time distributions
- Analyze by category

---

## Key Features for Marketing Agencies

✅ **Story-Driven Narrative** - Tells cohesive consumer story  
✅ **Segment Strategy Guides** - Pre-written marketing approaches for each persona  
✅ **Data-Backed Insights** - Every recommendation grounded in analysis  
✅ **Interactive Exploration** - Dive into data with filters & custom views  
✅ **Professional Design** - Polished, client-ready presentation  
✅ **Actionable Recommendations** - Specific next steps for campaigns  

---

## How to Use for Client Presentations

1. **Open the dashboard** - Run the streamlit command above
2. **Walk through the narrative** - Start from hero section, move through each part
3. **Highlight your segment** - Use segment explorer tabs for customized views
4. **Show the strategy** - Tab section has pre-written strategies per persona
5. **Share data** - All charts are interactive (hover, zoom, etc.)
6. **Ask questions** - Interactive explorer lets you answer "what if" questions live

---

## Data Insights Summary

📊 **What the data shows:**
- 3 months of real consumer mobile usage
- 100+ users tracked daily
- 4 distinct consumer archetypes
- Clear timing patterns
- Strong video engagement

💡 **Why it matters for marketing:**
- Understand WHERE your audience spends time
- Know WHEN they're most receptive
- Discover WHAT content drives engagement
- Learn HOW to reach each segment differently

---

## File Structure

```
streamlit_dashboard.py          ← Run this file with `streamlit run`
Mobile_Usage_Analysis.ipynb     ← Original analysis (dashboard removed)
Data Raw/
  └─ screen_time_app_usage_dataset.csv  ← Data source
README_DASHBOARD.md             ← Full documentation
requirements.txt                ← Python dependencies
QUICK_START.md                  ← This file
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No such file or directory: Data Raw/..." | Make sure you're running from the project directory |
| Streamlit not found | Run `pip install streamlit` |
| Slow performance on first load | App caches data - 2nd load will be faster |
| Graphs look cut off | Try expanding your browser window or refreshing |

---

## Next Steps

After reviewing the dashboard:

1. **Share with stakeholders** - Open the dashboard and present the story
2. **Customize for your agency** - Edit segment strategies in the code
3. **Add your own data** - Replace CSV with your actual campaign data
4. **Create campaigns** - Use insights to execute segment-specific campaigns
5. **Track results** - Compare performance to predicted patterns

---

## Need Help?

- Check `README_DASHBOARD.md` for detailed documentation
- Review `Mobile_Usage_Analysis.ipynb` for underlying analysis & calculations
- All Streamlit features are fully documented at https://docs.streamlit.io

Happy analyzing! 📊
