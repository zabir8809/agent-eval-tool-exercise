from textwrap import dedent
import argparse
import sys

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st
from agno.models.ollama import Ollama

# Import evaluation utilities
from eval_utils import TravelAgentEvaluator

# Set up the Streamlit app
st.title("AI Travel Planner using Deepseek R1 ✈️")
st.caption("Plan your next adventure with AI Travel Planner by researching and planning a personalized itinerary on autopilot using local Deepseek R1")

# Create Researcher agent with DuckDuckGoTools
researcher = Agent(
    name="Researcher",
    role="Searches for travel destinations, activities, and accommodations based on user preferences",
    model=Ollama(id="deepseek-r1:1.5b-qwen-distill-fp16"),
    description=dedent(
        """
        You are a world-class travel researcher. Given a travel destination and the number of days the user wants to travel for,
        generate a list of search terms for finding relevant travel activities and accommodations.
        Then search the web for each term, analyze the results, and return the 10 most relevant results.
        """
    ),
    instructions=[
        "Given a travel destination and the number of days the user wants to travel for, first generate a list of 3 search terms related to that destination and the number of days.",
        "For each search term, `search_duckduckgo` and analyze the results.",
        "From the results of all searches, return the 10 most relevant results to the user's preferences.",
        "Remember: the quality of the results is important.",
    ],
    tools=[DuckDuckGoTools()],
    add_datetime_to_instructions=True,
)

# Create Planner agent
planner = Agent(
    name="Planner",
    role="Generates a draft itinerary based on user preferences and research results",
    model=Ollama(id="deepseek-r1:1.5b-qwen-distill-fp16"),
    description=dedent(
        """
        You are a senior travel planner. Given a travel destination, the number of days the user wants to travel for, and a list of research results,
        your goal is to generate a draft itinerary that meets the user's needs and preferences.
        """
    ),
    instructions=[
        "Given a travel destination, the number of days the user wants to travel for, and a list of research results, generate a draft itinerary that includes suggested activities and accommodations.",
        "Ensure the itinerary is well-structured, informative, and engaging.",
        "Ensure you provide a nuanced and balanced itinerary, quoting facts where possible.",
        "Remember: the quality of the itinerary is important.",
        "Focus on clarity, coherence, and overall quality.",
        "Never make up facts or plagiarize. Always provide proper attribution.",
    ],
    add_datetime_to_instructions=True,
)

def generate_itinerary(destination: str, num_days: int, enable_logging: bool = True):
    """
    Generate an itinerary for the given destination and number of days.
    
    Args:
        destination: Travel destination
        num_days: Number of days for the trip
        enable_logging: Whether to log the interaction for evaluation
        
    Returns:
        Tuple of (cleaned_content, researcher_output)
    """
    # Get the research results (optional: wire as needed for planner prompt)
    # research_results = researcher.run(f"{destination} for {num_days} days").content
    response = planner.run(f"{destination} for {num_days} days", stream=False)
    
    # Remove content within <think></think> tags
    import re
    content = response.content
    # Remove everything between <think> and </think> tags (including the tags themselves)
    cleaned_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
    # Remove any extra whitespace that might be left
    cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content).strip()
    
    # Log the interaction for evaluation if enabled
    if enable_logging:
        evaluator = TravelAgentEvaluator()
        evaluator.log_interaction(
            user_input={"destination": destination, "num_days": num_days},
            planner_output=cleaned_content,
            researcher_output=None,  # Could be enhanced to capture researcher output
            metadata={
                "agent_name": "planner",
                "model": "deepseek-r1:1.5b-qwen-distill-fp16",
                "processing_time": "N/A"  # Could be enhanced to capture timing
            }
        )
    
    return cleaned_content, None

# Check if running in evaluation mode
if len(sys.argv) > 1 and sys.argv[1] == "--eval-mode":
    # Evaluation mode - read from stdin and output to stdout
    import json
    import sys
    
    try:
        # Read input from stdin (evaluation format)
        input_data = json.loads(sys.stdin.read())
        destination = input_data.get("destination", "New York")
        num_days = input_data.get("num_days", 3)
        
        # Generate itinerary without logging (to avoid double logging)
        result, _ = generate_itinerary(destination, num_days, enable_logging=False)
        
        # Output result in evaluation format
        print(json.dumps({"output": result}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
    sys.exit(0)

# Streamlit UI
# Input fields for the user's destination and travel duration
destination = st.text_input("Where do you want to go?")
num_days = st.number_input("How many days do you want to travel for?", min_value=1, max_value=30, value=7)

if st.button("Generate Itinerary"):
    with st.spinner("Processing..."):
        result, _ = generate_itinerary(destination, num_days, enable_logging=True)
        st.write(result)
