from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 7 lines"
    if length == "Medium":
        return "8 to 15 lines"
    if length == "Long":
        return "16 to 25 lines"

def get_structure_template(structure):
    if structure == "Bullet Points":
        return "\nFormat the content using bullet points (•) for main ideas."
    elif structure == "Numbered List":
        return "\nFormat the content as a numbered list for main points."
    return ""

def get_cta_prompt(include_cta):
    if include_cta:
        return "\nEnd with a clear call-to-action that encourages engagement (like, comment, share) or professional connection."
    return ""

def generate_post(length, language, tag, tone="Professional", structure="Regular", include_cta=True):
    prompt = get_prompt(length, language, tag, tone, structure, include_cta)
    response = llm.invoke(prompt)
    return response.content

def get_prompt(length, language, tag, tone, structure, include_cta):
    length_str = get_length_str(length)
    structure_template = get_structure_template(structure)
    cta_prompt = get_cta_prompt(include_cta)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    4) Tone: {tone} - maintain this tone throughout the post
    {structure_template}
    {cta_prompt}

    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    
    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "\n5) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: 
            break

    return prompt
