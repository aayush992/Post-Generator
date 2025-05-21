import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post
import json
import datetime
import pyperclip
import emoji

# Initialize session state
if 'post_history' not in st.session_state:
    st.session_state.post_history = []

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = ["Professional", "Casual", "Motivational", "Educational", "Story-telling"]
structure_options = ["Regular", "Bullet Points", "Numbered List"]

def save_to_history(post, metadata):
    st.session_state.post_history.append({
        "post": post,
        "metadata": metadata,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def get_hashtag_suggestions(tag):
    base_hashtags = {
        "Technology": ["#tech", "#innovation", "#digital", "#future", "#coding", "#programming", "#developer", "#software", "#techlife"],
        "Career": ["#career", "#jobs", "#professional", "#growth", "#careeradvice", "#jobsearch", "#networking", "#success", "#opportunities"],
        "Leadership": ["#leadership", "#management", "#success", "#business", "#leadershipskills", "#teamwork", "#growthmindset", "#inspiration"],
        "Data Science": ["#datascience", "#analytics", "#machinelearning", "#ai", "#python", "#data", "#technology", "#bigdata"],
        "Artificial Intelligence": ["#ai", "#artificialintelligence", "#machinelearning", "#technology", "#future", "#innovation", "#chatgpt", "#tech"],
        "Mental Health": ["#mentalhealth", "#wellness", "#selfcare", "#mindfulness", "#growth", "#motivation", "#health", "#mindset"],
        "Product Management": ["#productmanagement", "#agile", "#business", "#tech", "#startup", "#innovation", "#strategy", "#product"],
        "Open Source": ["#opensource", "#github", "#coding", "#developer", "#community", "#programming", "#collaboration"],
        "Startup": ["#startup", "#entrepreneurship", "#business", "#innovation", "#startuplife", "#entrepreneur", "#funding"],
        "Personal Development": ["#personaldevelopment", "#growth", "#mindset", "#learning", "#success", "#motivation", "#goals"],
        "Books": ["#books", "#reading", "#learning", "#knowledge", "#education", "#mindset", "#growth", "#wisdom"],
        "Work Culture": ["#workculture", "#workplace", "#hr", "#business", "#culture", "#leadership", "#team", "#companyculture"],
        "Job Search": ["#jobsearch", "#career", "#jobs", "#hiring", "#recruitment", "#interview", "#opportunities", "#resume"],
        "Self Improvement": ["#selfimprovement", "#growth", "#motivation", "#mindset", "#success", "#goals", "#personaldevelopment"],
        "Business": ["#business", "#entrepreneurship", "#success", "#strategy", "#marketing", "#innovation", "#growth"],
        "Influencer": ["#influencer", "#socialmedia", "#marketing", "#branding", "#content", "#digitalmarketing"],
        "Motivation": ["#motivation", "#inspiration", "#success", "#goals", "#mindset", "#growth", "#positivity"],
        "Scams": ["#scamalert", "#awareness", "#security", "#safety", "#cybersecurity", "#fraud", "#protection"]
    }
    
    # Default hashtags that are always relevant for LinkedIn
    default_hashtags = ["#linkedin", "#networking", "#professional", "#career"]
    
    # Get specific hashtags for the tag or use defaults
    specific_hashtags = base_hashtags.get(tag, [])
    
    # Combine specific and default hashtags, remove duplicates
    all_hashtags = list(set(specific_hashtags + default_hashtags))
    
    # Add custom option
    all_hashtags.append("#custom")
    
    return all_hashtags

def main():
    st.title("📱 Enhanced LinkedIn Post Generator")
    
    # Sidebar for history
    with st.sidebar:
        st.header("📜 Post History")
        for idx, item in enumerate(reversed(st.session_state.post_history[-5:])):
            with st.expander(f"Post {len(st.session_state.post_history) - idx}"):
                st.text(f"Generated on: {item['timestamp']}")
                st.text(f"Topic: {item['metadata']['tag']}")
                st.text_area("Content", item['post'], height=100)

    # Main content area
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()
    
    with col1:
        selected_tag = st.selectbox("💡 Topic", options=tags)
        selected_tone = st.selectbox("🎭 Tone", options=tone_options)
    
    with col2:
        selected_length = st.selectbox("📏 Length", options=length_options)
        selected_structure = st.selectbox("📋 Structure", options=structure_options)
    
    with col3:
        selected_language = st.selectbox("🌐 Language", options=language_options)
        include_cta = st.checkbox("Include Call-to-Action", value=True)

    # Emoji selector
    if st.checkbox("🎯 Add Emojis"):
        selected_emojis = st.multiselect(
            "Select Emojis",
            options=list(emoji.EMOJI_DATA.keys())[:100],
            format_func=lambda x: f"{x} {emoji.EMOJI_DATA[x]['en']}"
        )
    else:
        selected_emojis = []

    # Hashtag selector
    suggested_hashtags = get_hashtag_suggestions(selected_tag)
    selected_hashtags = st.multiselect(
        "🏷️ Select Hashtags",
        options=suggested_hashtags,
        default=suggested_hashtags[:3] if len(suggested_hashtags) > 3 else suggested_hashtags
    )

    if "#custom" in selected_hashtags:
        custom_hashtag = st.text_input("Add custom hashtag (include #)")
        if custom_hashtag and custom_hashtag.startswith("#"):
            selected_hashtags = [tag for tag in selected_hashtags if tag != "#custom"] + [custom_hashtag]

    if st.button("✨ Generate Post"):
        with st.spinner("Creating your LinkedIn post..."):
            post = generate_post(
                selected_length,
                selected_language,
                selected_tag,
                tone=selected_tone,
                structure=selected_structure,
                include_cta=include_cta
            )
            
            # Add selected emojis
            if selected_emojis:
                post = " ".join(selected_emojis) + "\n\n" + post
            
            # Add hashtags
            if selected_hashtags:
                post = post + "\n\n" + " ".join(selected_hashtags)
            
            # Save to history
            save_to_history(post, {
                "tag": selected_tag,
                "length": selected_length,
                "language": selected_language,
                "tone": selected_tone
            })
            
            # Display the post with metrics
            st.text_area("Generated Post", post, height=300)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Characters", len(post))
            with col2:
                st.metric("Words", len(post.split()))
            with col3:
                st.metric("Lines", len(post.splitlines()))
            
            # Copy to clipboard button
            if st.button("📋 Copy to Clipboard"):
                pyperclip.copy(post)
                st.success("Post copied to clipboard!")
            
            # Best posting time suggestion
            st.info("📊 Recommended posting time: Tuesday or Thursday between 9:00 AM - 11:00 AM for maximum engagement.")

if __name__ == "__main__":
    main()