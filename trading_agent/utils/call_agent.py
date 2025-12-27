from google.genai import types

async def _process_agent_response(event):
    if event.content and event.content.parts:        
        
        final_response = None
        if event.is_final_response():
            if (event.content and event.content.parts and
                hasattr(event.content.parts[0], "text")):
                final_response = event.content.parts[0].text.strip()
        
        return final_response


async def call_agent_async(runner, user_id, session_id, query):
    content = types.Content(
        role="user", parts=[types.Part(text=query)]
    )
    final_response_text = None
    try:
        
        async for event in runner.run_async(
            user_id=user_id, 
            session_id=session_id, 
            new_message=content
        ):
            response = await _process_agent_response(event)
            
            if response:
                final_response_text = response
            
        return final_response_text
            

    except Exception as e:
        print("Error during agent call:", str(e))
        return None
