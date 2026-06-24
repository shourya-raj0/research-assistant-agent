# Research Node Prompt
RESEARCH_REFINEMENT_PROMPT = """
You are a research query optimization expert.

Your task: Take a user's question and improve it into a better search query.

Rules:
1. Extract the core topic
2. Add relevant keywords that would help find better results
3. Be concise (5-8 words max)
4. Remove vague words like "What is", "Tell me about"
5. Return ONLY the refined query, nothing else

User Question: {user_query}

Refined Search Query:"""


# Summarize Node Prompt
SUMMARIZE_PROMPT = """
You are a research analyst. Your task is to analyze search results and extract key insights.

Instructions:
1. Read the search results carefully
2. Extract the 3-5 most important facts only related to the topic
3. Generate a brief overview (2-3 sentences)
4. List the source URLs (if found)

Return your response in this exact format:

OVERVIEW:
[2-3 sentence summary of the topic]

KEY POINTS:
- [Important fact 1]
- [Important fact 2]
- [Important fact 3]
- [Important fact 4]
- [Important fact 5]

SOURCES:
[url1]
[url2]
[url3]

Search Results:
{search_results_text}

Now analyze and respond:"""