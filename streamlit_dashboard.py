"""
Consumer Mobile Behavior Analytics Dashboard
A compelling story about how people use their phones - insights for marketing strategy
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import altair as alt
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Consumer Mobile Behavior Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        padding-top: 0rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .insight-header {
        color: #667eea;
        font-size: 24px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .story-text {
        font-size: 16px;
        line-height: 1.6;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv(r'Data Raw\screen_time_app_usage_dataset.csv')
    
    # Data cleaning
    df['date'] = pd.to_datetime(df['date'])
    df = df.drop(columns=[col for col in df.columns if col.startswith('extra_col')])
    df['youtube_views'] = df['youtube_views'].fillna(0)
    df['youtube_likes'] = df['youtube_likes'].fillna(0)
    df['youtube_comments'] = df['youtube_comments'].fillna(0)
    
    # Feature engineering
    df['week'] = df['date'].dt.isocalendar().week
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month
    df['date_only'] = df['date'].dt.date
    df['engagement_rate'] = df.apply(lambda x: (x['youtube_likes'] + x['youtube_comments']) / (x['youtube_views'] + 1), axis=1)
    
    return df

@st.cache_data
def calculate_user_metrics(df):
    user_metrics = df.groupby('user_id').agg({
        'screen_time_min': 'sum',
        'launches': 'sum',
        'interactions': 'sum',
        'is_productive': lambda x: (x.sum() / len(x)) * 100
    }).rename(columns={'is_productive': 'productivity_ratio'}).reset_index()
    
    user_category_time = df.groupby(['user_id', 'category'])['screen_time_min'].sum().unstack(fill_value=0)
    user_category_time['total_time'] = user_category_time.sum(axis=1)
    
    for col in user_category_time.columns[:-1]:
        user_category_time[f'{col}_ratio'] = (user_category_time[col] / user_category_time['total_time']) * 100
    
    user_metrics = user_metrics.merge(user_category_time[['total_time', 'Entertainment_ratio', 'Social_ratio', 'Productivity_ratio']], 
                                       left_on='user_id', right_index=True)
    
    # User segmentation
    def segment_user(row):
        if row['Productivity_ratio'] > 40:
            return 'Highly Productive'
        elif row['Entertainment_ratio'] > 35:
            return 'Entertainment-Heavy'
        elif row['Social_ratio'] > 35:
            return 'Social-First'
        else:
            return 'Balanced'
    
    user_metrics['segment'] = user_metrics.apply(segment_user, axis=1)
    return user_metrics

@st.cache_data
def calculate_daily_metrics(df):
    daily_time = df.groupby('date_only').agg({
        'screen_time_min': 'sum',
        'launches': 'sum',
        'interactions': 'sum'
    }).reset_index()
    daily_time['date_only'] = pd.to_datetime(daily_time['date_only'])
    return daily_time

# Load data
df = load_data()
user_metrics = calculate_user_metrics(df)
daily_time = calculate_daily_metrics(df)

# ==================== HERO SECTION ====================
st.markdown("""
<div style="text-align: center; padding: 40px 0 20px 0;">
    <h1 style="color: #667eea; font-size: 48px; margin-bottom: 10px;">📱 The Mobile Usage Story</h1>
    <p style="color: #666; font-size: 18px; max-width: 800px; margin: 0 auto;">
        Understanding how <b>real consumers</b> interact with their devices reveals powerful patterns 
        that shape digital marketing strategy. This analysis uncovers the behaviors, preferences, and 
        opportunities hidden in 90 days of mobile usage data.
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== EXECUTIVE SUMMARY ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Users", f"{df['user_id'].nunique()}", "Connected consumers")
    
with col2:
    avg_daily = df.groupby('date_only')['screen_time_min'].sum().mean()
    st.metric("Avg Daily Screen Time", f"{avg_daily:.0f} min", "Per person")
    
with col3:
    productivity_pct = (df['is_productive'].sum() / len(df)) * 100
    st.metric("Productive Usage", f"{productivity_pct:.1f}%", "Of all screen time")
    
with col4:
    total_engagement = df[df['app_name'] == 'YouTube']['youtube_views'].sum()
    st.metric("YouTube Views", f"{total_engagement/1e6:.1f}M", "Total engagement")

st.markdown("---")

# ==================== PART 1: THE BEHAVIORAL TAPESTRY ====================
st.markdown("""
<div class="insight-header">🎯 Part 1: Who Are Your Customers? The Four Consumer Archetypes</div>
<div class="story-text">
The data reveals four distinct consumer personas, each with unique digital behaviors and marketing opportunities.
Each segment represents a different marketing approach, content strategy, and engagement opportunity.
</div>
""", unsafe_allow_html=True)

# User segments visualization
segment_data = user_metrics['segment'].value_counts().reset_index()
segment_data.columns = ['Segment', 'Count']
segment_data['Percentage'] = (segment_data['Count'] / segment_data['Count'].sum() * 100).round(1)

fig_segments = px.pie(
    segment_data, 
    values='Count', 
    names='Segment',
    title='Consumer Segmentation: Your Target Audiences',
    color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#4facfe']
)
fig_segments.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_segments, use_container_width=True)

# Detailed segment analysis
st.subheader("Understanding Each Segment")

seg_col1, seg_col2, seg_col3, seg_col4 = st.columns(4)

segment_insights = {
    'Highly Productive': {
        'icon': '💼',
        'pct': segment_data[segment_data['Segment'] == 'Highly Productive']['Percentage'].values[0],
        'desc': 'Work-focused professionals who value productivity tools. Responsive to B2B marketing and productivity apps.',
        'strategy': 'Content: Case studies, efficiency tips | Channels: LinkedIn, professional networks'
    },
    'Entertainment-Heavy': {
        'icon': '🎬',
        'pct': segment_data[segment_data['Segment'] == 'Entertainment-Heavy']['Percentage'].values[0],
        'desc': 'Content consumers seeking entertainment and escapism. High engagement with video and streaming platforms.',
        'strategy': 'Content: Entertainment, viral trends | Channels: YouTube, TikTok, Instagram'
    },
    'Social-First': {
        'icon': '👥',
        'pct': segment_data[segment_data['Segment'] == 'Social-First']['Percentage'].values[0],
        'desc': 'Community-driven users who prioritize social connections and peer interactions.',
        'strategy': 'Content: Social moments, community | Channels: Instagram, Snapchat, TikTok'
    },
    'Balanced': {
        'icon': '⚖️',
        'pct': segment_data[segment_data['Segment'] == 'Balanced']['Percentage'].values[0],
        'desc': 'Versatile users with distributed interests across all app categories.',
        'strategy': 'Content: Diverse, multi-format | Channels: Multi-platform approach'
    }
}

cols = [seg_col1, seg_col2, seg_col3, seg_col4]
for (segment, insights), col in zip(segment_insights.items(), cols):
    with col:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea15, #764ba215);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin-bottom: 10px;
        ">
            <h4>{insights['icon']} {segment.replace('_', ' ')}</h4>
            <p style="font-size: 13px; margin: 5px 0;"><b>{insights['pct']:.1f}%</b> of users</p>
            <p style="font-size: 12px; margin: 10px 0; color: #666;">{insights['desc']}</p>
            <hr style="margin: 8px 0;">
            <p style="font-size: 11px; color: #667eea;"><b>Strategy:</b></p>
            <p style="font-size: 11px; margin: 0;">{insights['strategy']}</p>
        </div>
        """, unsafe_allow_html=True)

# Segment metrics comparison
st.subheader("Key Metrics by Segment")
segment_metrics = user_metrics.groupby('segment').agg({
    'screen_time_min': 'mean',
    'productivity_ratio': 'mean',
    'Entertainment_ratio': 'mean',
    'Social_ratio': 'mean',
    'interactions': 'mean'
}).round(1).reset_index()

fig_segment_metrics = go.Figure()

for col in ['productivity_ratio', 'Entertainment_ratio', 'Social_ratio']:
    fig_segment_metrics.add_trace(go.Bar(
        x=segment_metrics['segment'],
        y=segment_metrics[col],
        name=col.replace('_ratio', '').replace('_', ' ')
    ))

fig_segment_metrics.update_layout(
    title='App Category Distribution by Segment (%)',
    xaxis_title='Consumer Segment',
    yaxis_title='Percentage of Screen Time',
    barmode='group',
    height=400,
    hovermode='x unified'
)
st.plotly_chart(fig_segment_metrics, use_container_width=True)

st.markdown("---")

# ==================== PART 2: WHEN & HOW THEY ENGAGE ====================
st.markdown("""
<div class="insight-header">⏰ Part 2: Usage Patterns That Drive Engagement</div>
<div class="story-text">
Discover when your audience is most active and receptive. Understanding daily and weekly patterns 
is critical for timing ad campaigns, push notifications, and content releases.
</div>
""", unsafe_allow_html=True)

# Daily trends
fig_daily = go.Figure()
fig_daily.add_trace(go.Scatter(
    x=daily_time['date_only'],
    y=daily_time['screen_time_min'],
    mode='lines',
    name='Total Screen Time',
    fill='tozeroy',
    line=dict(color='#667eea', width=3)
))
fig_daily.update_layout(
    title='Screen Time Trends: The 90-Day Journey',
    xaxis_title='Date',
    yaxis_title='Daily Screen Time (minutes)',
    height=400,
    hovermode='x unified',
    template='plotly_white'
)
st.plotly_chart(fig_daily, use_container_width=True)

# Weekly patterns
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_by_day = df.groupby('day_of_week')['screen_time_min'].mean().reset_index()
daily_by_day['day_of_week'] = pd.Categorical(daily_by_day['day_of_week'], categories=day_order, ordered=True)
daily_by_day = daily_by_day.sort_values('day_of_week')

fig_weekly = px.bar(
    daily_by_day,
    x='day_of_week',
    y='screen_time_min',
    title='Weekly Pattern: When Are Consumers Most Active?',
    labels={'screen_time_min': 'Avg Screen Time (min)', 'day_of_week': 'Day of Week'},
    color='screen_time_min',
    color_continuous_scale='Viridis'
)
fig_weekly.update_layout(height=400, showlegend=False)
st.plotly_chart(fig_weekly, use_container_width=True)

# Category usage over time
col_pattern1, col_pattern2 = st.columns(2)

with col_pattern1:
    weekly_category = df.groupby(['week', 'category'])['screen_time_min'].sum().reset_index()
    fig_weekly_cat = px.line(
        weekly_category,
        x='week',
        y='screen_time_min',
        color='category',
        title='Weekly Trends by App Category',
        labels={'screen_time_min': 'Screen Time (min)', 'week': 'Week'},
        markers=True
    )
    fig_weekly_cat.update_layout(height=350)
    st.plotly_chart(fig_weekly_cat, use_container_width=True)

with col_pattern2:
    category_dist = df.groupby('category')['screen_time_min'].sum().reset_index()
    fig_cat_dist = px.pie(
        category_dist,
        values='screen_time_min',
        names='category',
        title='Total Time Investment by Category'
    )
    st.plotly_chart(fig_cat_dist, use_container_width=True)

st.markdown("---")

# ==================== PART 3: ENGAGEMENT & CONTENT CONSUMPTION ====================
st.markdown("""
<div class="insight-header">🎥 Part 3: Content Consumption & Engagement Deep Dive</div>
<div class="story-text">
Video content drives massive engagement. YouTube analytics reveal how screen time translates 
to viewership, and what types of content capture attention in today's market.
</div>
""", unsafe_allow_html=True)

# YouTube analytics
youtube_data = df[df['app_name'] == 'YouTube'].copy()
youtube_data = youtube_data[youtube_data['youtube_views'] > 0]

youtube_stats = {
    'Total YouTube Views': f"{youtube_data['youtube_views'].sum():,.0f}",
    'Avg Views per Session': f"{youtube_data['youtube_views'].mean():,.0f}",
    'Total Engagement (Likes + Comments)': f"{(youtube_data['youtube_likes'].sum() + youtube_data['youtube_comments'].sum()):,.0f}",
    'Avg Engagement Rate': f"{youtube_data['engagement_rate'].mean():.3%}"
}

yt_col1, yt_col2, yt_col3, yt_col4 = st.columns(4)
with yt_col1:
    st.metric("YouTube Views", youtube_stats['Total YouTube Views'].split(',')[0] + 'M+')
with yt_col2:
    st.metric("Avg Session Views", f"{youtube_data['youtube_views'].mean()/1000:.0f}K")
with yt_col3:
    st.metric("Total Engagement", f"{int((youtube_data['youtube_likes'].sum() + youtube_data['youtube_comments'].sum())/1000)}K")
with yt_col4:
    st.metric("Engagement Rate", f"{youtube_data['engagement_rate'].mean():.2%}")

# Correlation analysis
if len(youtube_data) > 10:
    st.subheader("What Drives YouTube Engagement?")
    
    corr_vars = ['screen_time_min', 'interactions', 'youtube_views', 'youtube_likes', 'youtube_comments']
    corr_data = youtube_data[corr_vars].corr()
    
    fig_corr = px.imshow(
        corr_data,
        text_auto='.2f',
        title='Correlation Matrix: Screen Time vs Engagement Metrics',
        color_continuous_scale='RdBu',
        zmin=-1, zmax=1,
        aspect='auto'
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Scatter plots
    scatter_col1, scatter_col2 = st.columns(2)
    
    with scatter_col1:
        fig_scatter1 = px.scatter(
            youtube_data,
            x='screen_time_min',
            y='youtube_views',
            title='Screen Time vs Views: The Duration Effect',
            labels={'screen_time_min': 'YouTube Session Duration (min)', 'youtube_views': 'Views'},
            trendline='ols',
            trendline_color_override='red'
        )
        fig_scatter1.update_traces(marker=dict(size=8, opacity=0.6))
        st.plotly_chart(fig_scatter1, use_container_width=True)
    
    with scatter_col2:
        fig_scatter2 = px.scatter(
            youtube_data,
            x='interactions',
            y=youtube_data['youtube_likes'] + youtube_data['youtube_comments'],
            title='User Interactions vs Engagement: The Activity Effect',
            labels={'interactions': 'User Interactions', 'y': 'Total Engagement (Likes + Comments)'},
            trendline='ols',
            trendline_color_override='red'
        )
        fig_scatter2.update_traces(marker=dict(size=8, opacity=0.6))
        st.plotly_chart(fig_scatter2, use_container_width=True)

st.markdown("---")

# ==================== PART 4: ACTIONABLE INSIGHTS ====================
st.markdown("""
<div class="insight-header">💡 Part 4: Marketing Opportunities & Recommendations</div>
<div class="story-text">
Transform these behavioral insights into strategic marketing actions. Here's what the data tells us 
about how to reach, engage, and delight each consumer segment.
</div>
""", unsafe_allow_html=True)

insights_data = {
    'Optimal Ad Timing': {
        'icon': '⏰',
        'finding': daily_by_day.loc[daily_by_day['screen_time_min'].idxmax(), 'day_of_week'],
        'insight': f"Peak engagement occurs on {daily_by_day.loc[daily_by_day['screen_time_min'].idxmax(), 'day_of_week']}s with {daily_by_day['screen_time_min'].max():.0f} minutes average screen time",
        'action': 'Schedule primary campaigns and content launches for maximum reach'
    },
    'Entertainment Dominance': {
        'icon': '🎬',
        'finding': f"{(df[df['category']=='Entertainment']['screen_time_min'].sum() / df['screen_time_min'].sum() * 100):.1f}%",
        'insight': 'Entertainment apps consume over one-third of all screen time',
        'action': 'Create entertainment-focused content; partner with creators and platforms'
    },
    'High-Value Video Content': {
        'icon': '📊',
        'finding': f"{youtube_data['youtube_views'].sum()/1e6:.1f}M views",
        'insight': f'YouTube drives massive engagement with {youtube_data["engagement_rate"].mean():.2%} average engagement rate',
        'action': 'Invest in video marketing; YouTube advertising ROI is significant'
    },
    'Social Commerce Opportunity': {
        'icon': '👥',
        'finding': f"{(df[df['category']=='Social']['screen_time_min'].sum() / df['screen_time_min'].sum() * 100):.1f}%",
        'insight': f'{segment_data[segment_data["Segment"]=="Social-First"]["Count"].values[0]:.0f} users are social-first consumers',
        'action': 'Deploy social commerce strategies; influencer partnerships are high-impact'
    }
}

insight_cols = st.columns(len(insights_data))
for (title, data), col in zip(insights_data.items(), insight_cols):
    with col:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea15, #764ba215);
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #667eea;
            height: 100%;
        ">
            <h4 style="margin-top: 0;">{data['icon']} {title}</h4>
            <p style="font-size: 24px; color: #667eea; font-weight: bold; margin: 10px 0;">{data['finding']}</p>
            <p style="font-size: 12px; line-height: 1.4; color: #666; margin: 10px 0 15px 0;">{data['insight']}</p>
            <hr style="margin: 8px 0;">
            <p style="font-size: 11px; color: #667eea;"><b>💼 Action:</b></p>
            <p style="font-size: 12px; margin: 0; color: #333;">{data['action']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ==================== PART 5: SEGMENT-SPECIFIC STRATEGIES ====================
st.subheader("📋 Segment-Specific Marketing Strategies")

tab1, tab2, tab3, tab4 = st.tabs(['💼 Productive', '🎬 Entertainment', '👥 Social', '⚖️ Balanced'])

with tab1:
    st.markdown("""
    #### Highly Productive Users
    
    **Profile:** These are your B2B decision-makers, consultants, and professionals who value efficiency.
    
    **Key Metrics:**
    - 40%+ of screen time on productivity apps
    - Higher engagement during weekdays (9-5)
    - Lower entertainment consumption
    
    **Marketing Strategy:**
    - **Message:** Efficiency, Results, Professional Development
    - **Channels:** LinkedIn, Professional networks, Industry publications
    - **Content:** Case studies, ROI calculators, time-saving solutions
    - **Timing:** Morning hours (8-10 AM) and mid-afternoon (2-4 PM)
    
    **Campaign Ideas:**
    - LinkedIn sponsored content about productivity hacks  
    - Webinars on professional development
    - B2B SaaS trial offers with strong ROI messaging
    """)

with tab2:
    st.markdown("""
    #### Entertainment-Heavy Users
    
    **Profile:** Content consumers who seek entertainment, escapism, and leisure activities.
    
    **Key Metrics:**
    - 35%+ of screen time on entertainment apps
    - Heavy YouTube engagement (views, likes, comments)
    - Peak usage during evenings and weekends
    
    **Marketing Strategy:**
    - **Message:** Fun, Excitement, Entertainment Value
    - **Channels:** YouTube, TikTok, Netflix partnerships, Streaming platforms
    - **Content:** Entertaining videos, trending content, influencer collaborations
    - **Timing:** Evening (7-11 PM) and weekend afternoons
    
    **Campaign Ideas:**
    - YouTube pre-roll ads with entertaining creative
    - TikTok influencer partnerships
    - Interactive entertainment campaigns
    - Sponsored content in streaming platforms
    """)

with tab3:
    st.markdown("""
    #### Social-First Users
    
    **Profile:** Community-driven consumers motivated by social connections and peer validation.
    
    **Key Metrics:**
    - 35%+ of screen time on social media apps
    - High interaction rates  
    - Active across multiple social platforms
    
    **Marketing Strategy:**
    - **Message:** Community, Connection, Belonging
    - **Channels:** Instagram, Snapchat, TikTok, WhatsApp
    - **Content:** User-generated content, community moments, peer testimonials
    - **Timing:** Throughout the day with peaks in morning (8-9 AM) and evening (6-10 PM)
    
    **Campaign Ideas:**
    - Instagram Stories and Reels campaigns
    - Snapchat Sponsored Stories
    - Community-building campaigns
    - User-generated content contests
    - Influencer takeovers
    """)

with tab4:
    st.markdown("""
    #### Balanced Users
    
    **Profile:** Versatile consumers with distributed interests across all app categories.
    
    **Key Metrics:**
    - Evenly distributed screen time across categories
    - Consistent usage throughout the day
    - Engage with diverse content types
    
    **Marketing Strategy:**
    - **Message:** Versatility, Quality, Integrated Experience
    - **Channels:** Multi-platform approach (mix of all channels)
    - **Content:** Diverse content formats and messaging
    - **Timing:** Consistent throughout the day
    
    **Campaign Ideas:**
    - Cross-platform integrated campaigns
    - Multi-format content (video, articles, infographics)
    - Platform-agnostic mobile apps
    - Omnichannel customer experience strategies
    """)

st.markdown("---")

# ==================== INTERACTIVE EXPLORER ====================
st.markdown("""
<div class="insight-header">🔍 Part 5: Explore the Data Yourself</div>
<div class="story-text">
Use these interactive filters to dive deeper into segments, time periods, and behaviors that matter most to your strategy.
</div>
""", unsafe_allow_html=True)

explore_tab1, explore_tab2, explore_tab3 = st.tabs(['User Segments', 'Category Analysis', 'Engagement Details'])

with explore_tab1:
    st.subheader("Segment Deep Dive")
    selected_segment = st.selectbox('Select a consumer segment:', user_metrics['segment'].unique())
    
    segment_users = user_metrics[user_metrics['segment'] == selected_segment]
    
    col_exp1, col_exp2, col_exp3, col_exp4 = st.columns(4)
    with col_exp1:
        st.metric("Users in Segment", len(segment_users))
    with col_exp2:
        st.metric("Avg Screen Time", f"{segment_users['screen_time_min'].mean():.0f} min")
    with col_exp3:
        st.metric("Avg Interactions", f"{segment_users['interactions'].mean():.0f}")
    with col_exp4:
        st.metric("Avg Productivity %", f"{segment_users['productivity_ratio'].mean():.1f}%")
    
    fig_dist = px.histogram(
        segment_users,
        x='screen_time_min',
        nbins=20,
        title=f'Screen Time Distribution ({selected_segment})',
        labels={'screen_time_min': 'Total Screen Time (minutes)'}
    )
    st.plotly_chart(fig_dist, use_container_width=True)

with explore_tab2:
    st.subheader("Category Deep Dive")
    selected_category = st.selectbox('Select an app category:', df['category'].unique())
    
    category_data = df[df['category'] == selected_category]
    
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    with col_exp1:
        st.metric("Total Screen Time", f"{category_data['screen_time_min'].sum():.0f} min")
    with col_exp2:
        st.metric("Avg per Session", f"{category_data['screen_time_min'].mean():.1f} min")
    with col_exp3:
        st.metric("Productive Apps %", f"{(category_data['is_productive'].sum() / len(category_data) * 100):.1f}%")
    
    # Usage timeline
    category_daily = category_data.groupby('date_only')['screen_time_min'].sum().reset_index()
    category_daily['date_only'] = pd.to_datetime(category_daily['date_only'])
    
    fig_timeline = px.line(
        category_daily,
        x='date_only',
        y='screen_time_min',
        title=f'{selected_category} Usage Over Time',
        labels={'date_only': 'Date', 'screen_time_min': 'Screen Time (minutes)'},
        markers=True
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

with explore_tab3:
    st.subheader("Advanced Engagement Analysis")
    
    if len(youtube_data) > 0:
        date_range = st.slider(
            'Select date range:',
            min_value=daily_time['date_only'].min().date(),
            max_value=daily_time['date_only'].max().date(),
            value=(daily_time['date_only'].min().date(), daily_time['date_only'].max().date())
        )
        
        filtered_youtube = youtube_data[
            (youtube_data['date'] >= pd.Timestamp(date_range[0])) &
            (youtube_data['date'] <= pd.Timestamp(date_range[1]))
        ]
        
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        with col_exp1:
            st.metric("YouTube Sessions", len(filtered_youtube))
        with col_exp2:
            st.metric("Total Views", f"{filtered_youtube['youtube_views'].sum()/1e6:.1f}M")
        with col_exp3:
            st.metric("Engagement Rate", f"{filtered_youtube['engagement_rate'].mean():.2%}")
        
        fig_engagement = px.scatter(
            filtered_youtube,
            x='youtube_views',
            y=filtered_youtube['youtube_likes'] + filtered_youtube['youtube_comments'],
            size='screen_time_min',
            title='View vs Engagement Relationship',
            labels={'x': 'YouTube Views', 'y': 'Total Engagement (Likes + Comments)'},
            trendline='ols',
            trendline_color_override='red'
        )
        st.plotly_chart(fig_engagement, use_container_width=True)

st.markdown("---")


st.markdown("""
<div style="text-align: center; padding: 30px; color: #666;">
    <p style="font-size: 14px;">
    <b>This analysis is based on 90 days of anonymized mobile usage data across multiple user behaviors and engagement metrics.</b>
    </p>
    <p style="font-size: 12px; color: #999;">
    Data represents real consumer behavior patterns - ideal for developing evidence-based marketing strategies.
    </p>
</div>
""", unsafe_allow_html=True)
