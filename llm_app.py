"""
Product Review Analysis with LangChain structured output and database storage.
"""
from pydantic import BaseModel, Field
from models import ProductReviewRate, ProductReview
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model
# from database import create_tables, save_review_analysis
from dotenv import load_dotenv

load_dotenv()

# Initialize the model first
model = init_chat_model(
    model="gemini-2.5-flash-lite",
    model_provider="google_genai",
    max_tokens=500
)

# Create agent with explicit ToolStrategy
agent = create_agent(
    model=model,
    tools=[],
    response_format=ToolStrategy(schema=ProductReview),
    system_prompt="Analyze product reviews and extract structured data."
)

# create_tables()

# Sample review data
sample_reviews = [
    {
        "user": "john_doe",
        "product": "Wireless Headphones XYZ",
        "review": "Amazing product! 5 stars. Quick delivery and great quality, but quite pricey."
    },
    {
        "user": "jane_smith",
        "product": "Smart Watch ABC",
        "review": "Decent watch but battery life is disappointing. 3 stars."
    }
]

for sample in sample_reviews:
    # Test with a product review
    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": f"Analyze this review: '{sample['review']}'"
        }]
    })

    print(f"Review Analysis Result: {result['structured_response']}")

    # saved_review = save_review_analysis(
    #     user_info=sample["user"],
    #     review=sample["review"],
    #     product=sample["product"],
    #     rate=result['structured_response'].rating,
    #     sentiment=result['structured_response'].sentiment,
    #     key_points=result['structured_response'].key_points)

    # print(f"Saved review analysis: {saved_review}")