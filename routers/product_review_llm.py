from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from database import get_db
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from models import ProductReview, AnalyzedReview, ProductReviewRate

import json

load_dotenv()
router = APIRouter()


model = init_chat_model(
    model="gemini-2.5-flash-lite",
    model_provider="google_genai",
    max_tokens=500,
)

agent = create_agent(
    model=model,
    tools=[],
    response_format=ToolStrategy(schema=ProductReview),
    system_prompt="Analyze product reviews and extract structured data.",
)


def _to_dict(obj) -> dict:
    """Convert Pydantic/SQLModel objects or dicts to plain dict safely."""
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    # Pydantic v1
    if hasattr(obj, "dict"):
        return obj.dict()
    return {}


def _extract_structured(response) -> dict:
    """
    LangChain agent.invoke dönüşü:
    - response dict olabilir, içinde 'structured_response' dict ya da ProductReview olabilir
    - bazı sürümlerde direkt ProductReview dönebilir
    """
    # 1) response direkt model objesi ise
    if not isinstance(response, dict):
        return _to_dict(response)

    # 2) beklenen alan: structured_response
    sr = response.get("structured_response")
    if sr is not None:
        return _to_dict(sr)

    # 3) fallback: tool_calls içindeki args (bazı versiyonlarda burada bulunur)
    messages = response.get("messages") or []
    for m in reversed(messages):
        tool_calls = None
        if isinstance(m, dict):
            tool_calls = m.get("tool_calls")
        else:
            tool_calls = getattr(m, "tool_calls", None)

        if tool_calls:
            last = tool_calls[-1]
            if isinstance(last, dict) and isinstance(last.get("args"), dict):
                return last["args"]

    return {}


def insert_product_review_analysis(request_dict: dict, response, client_ip: str, db: Session):
    structured = _extract_structured(response)

    
    data = {
        "user_info": request_dict.get("user", "anonymous"),
        "review": request_dict["review"],
        "product": request_dict.get("product", "unknown"),
        "rate": structured.get("rating"),
        "sentiment": structured.get("sentiment"),
        "key_points": json.dumps(structured.get("key_points", []), ensure_ascii=False),
    }

    
    if hasattr(ProductReviewRate, "client_ip"):
        data["client_ip"] = client_ip

    new_review_analysis = ProductReviewRate(**data)

    db.add(new_review_analysis)
    db.commit()
    db.refresh(new_review_analysis)
    return new_review_analysis, structured


@router.post("/llm/chat")
def chat(request: AnalyzedReview, fastapi_req: Request, db: Session = Depends(get_db)):
    
    req_dict = request.model_dump() if hasattr(request, "model_dump") else request.dict()

    response = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "Analyze the following product review and provide a rating (1-5), "
                        "sentiment (positive/negative), and 3 key points: "
                        f"{req_dict['review']}"
                    )
                )
            ]
        }
    )

    db_record, structured = insert_product_review_analysis(
        req_dict,
        response,
        fastapi_req.client.host if fastapi_req.client else "unknown",
        db,
    )

    
    return {
        "analysis": structured,                 
        "db_record": jsonable_encoder(db_record)      
    }
