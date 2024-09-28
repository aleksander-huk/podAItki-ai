from openai import OpenAI

def validate_topic(client: OpenAI, history: list) -> bool:
    """
    Validates if the conversation history is related to taxes.
    
    Args:
        client (OpenAI): An instance of the OpenAI API client.
        history (list): A list containing the conversation history.

    Returns:
        bool: Returns True if the topic is tax-related, False otherwise.
    """
    
    system_prompt = f'''
    Jesteś systemem filtrujcym treści zwracajacym wartość '0' lub '1'.
    Twoim zadaniem jest przeanalizować wiadomość od użytkownika. Jeżeli temat o jaki pyta użytkownik nie jest w żadnym stopniu
    powizany z podatkami lub formularzami do podatków to zwróć 0. Jeżeli w tekście znajduja się przekleństwa zwróć 0.
    Jeżeli użytkownik podejmuje temat powizany z podatkami lub formularzami do podatków zwróć 1.
    Historia chatu: {history}
    '''
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role" : "user", "content": system_prompt}]
    )

    is_tex_related = completion.choices[0].message.content
    
    return is_tex_related != '0'