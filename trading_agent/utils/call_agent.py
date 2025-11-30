from google.genai import types

async def _process_agent_response(event):
    if event.content and event.content.parts:        
        
        final_response = None
        if event.is_final_response():
            if (event.content and event.content.parts and
                hasattr(event.content.parts[0], "text")):
                final_response = event.content.parts[0].text.strip()

        raw_products = []
        function_response = getattr(event.content.parts[0], "function_response", None)
        if function_response and hasattr(function_response, "response"):
            raw_products = function_response.response.get("products")
        
        return final_response, raw_products
    
async def call_agent_async(runner, user_id, session_id, query):
    content = types.Content(
        role="user", parts=[types.Part(text=query)]
    )
    final_response_text = None
    final_raw_products = None

    try:
        
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            response, raw_products = await _process_agent_response(event)
            
            if response:
                final_response_text = response
            
            if raw_products:
                final_raw_products = raw_products

        return final_response_text, final_raw_products
            

    except Exception as e:
        print("Error during agent call:", str(e))
        return None, None