from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse

app=FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    try:
        logging.info(query)
        graph=GraphBuilder(model_provider="groq")
        react_app=graph()

        png_graph=react_app.get_graph().draw_mermaid_png()
        with open("planner_graph.png","wb") as f:
            f.write(png_graph)

        logging.info(f"Graph saved as 'planner_graph' in {os.getcwd()}")
        messages={"messages": [query.question]}
        output=react_app.invoke(messages)

        # if result is dictionary with messages
        if isinstance(output, dict) and "messages" in output:
            final_output=output["messages"][-1].content
        else:
            final_output=str(output)

        return {"answer": final_output}
    
    except Exception as e:
        return JSONResponse(status_code=500,content={"error": str(e)})