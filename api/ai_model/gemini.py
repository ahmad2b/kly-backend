import os
import json
from dotenv import load_dotenv
import google.generativeai as genai  # type: ignore

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


def shorten_url(data: str):
    prompt_parts = [
        "Suggest only a single word (no need for any explanation; give only a single creative word) that best describes the content of the URL, emphasizing on its focused theme or content.",
        'input: "https://www.datacamp.com/podcast/data-storytelling-and-visualization-with-lea-pica-from-present-beyond-measure"',
        'output: {\n"data": "DataViz"\n}',
        'input: "The mathematical groundwork was laid in the 1940s and 1950s (Shannon, Turing). The foundations for today’s generative language applications were elaborated in the 1990s (Hochreiter, Schmidhuber), and the whole field took off around 2018 (Radford, Devlin, et al.). Major milestones in the last few years comprised BERT (Google, 2018), GPT-3 (OpenAI, 2020), Dall-E (OpenAI, 2021), Stable Diffusion (Stability AI, LMU Munich, 2022), ChatGPT (OpenAI, 2022)."',
        'output: {\n"data": "GenerativeAI"\n}',
        'input: "https://medium.com/mlearning-ai/5000x-generative-ai-intro-overview-models-prompts-technology-tools-comparisons-the-best-a4af95874e94"',
        'output: {\n"data": "GenAI"\n}',
        'input: "https://medium.com/@sahintalha1/high-level-system-architecture-of-booking-com-06c199003d94"',
        'output: {\n"data": "BookingArch"\n}',
        'input: "https://oreilly.medium.com/generative-ai-in-the-enterprise-c43d57f0f20c"',
        'output: {\n"data": "GenAI4Enterprise"\n}',
        'input: "https://ldeplano.medium.com/10-rules-i-learned-that-helped-me-outperform-90-of-hedge-funds-over-the-last-6-years-e7eef446a536"',
        'output: {\n"data": "HedgeFundRules"\n}',
        'input: "We developed prompt libraries, redesigned workflows, built GenAI backed features in existing products, and built GenAI apps as well. As we worked through the gamut my teams kept coming back with similar observations, recurring problems and repeatable solutions — all signs alluding to the need for a reference architecture for GenAI apps. We found a ton of interesting papers, articles and blog posts but very few were bold enough to take on the entire stack/landscape. Two that we would like to acknowledge here — Generative AI Lifecycle Patterns by Ali Arsanjani and Emerging Architectures for LLM Applications by Matt Bornstein and Rajko Radovanovic."',
        'output: {\n"data": "GenAIReferenceArch"\n}',
        'input: "https://uxdesign.cc/can-i-keep-my-story-open-and-accessible-to-everyone-to-read-on-medium-ebb91751987"',
        'output: {\n"data": "OpenMediumStories"\n}',
        'input: "If you’ve been publicly sham"ed for anything, what matters most is how you respond next. You can double-down on defensiveness and self-preservation (the wrong answer) or you can approach it with a growth mindset and funnel that energy in a positive direction. I attempted to do the latter with my shame and frustration. I made the A11Y Project because of my own ignorance and difficulty finding up-to-date, easy-to-understand, and forgiving accessibility knowledge. If there’s one thing I believe it’s that most web developers aren’t going to be accessibility experts, but all developers need a working knowledge of accessibility. And the data shows, we’re all making mistakes."',
        'output: {\n"data": "A11YforDevs"\n}',
        'input: "https://www.uottawa.ca/library/copyright/instructors/using-publicly-accessible-websites-digital-media"',
        'output: {\n"data": "PublicDigitalMedia"\n}',
        'input: "https://www.hostinger.com/tutorials/blog-seo"',
        'output: {\n"data": "BlogSEO"\n}',
        f"input: {data}",
        "output: ",
    ]

    response = model.generate_content(prompt_parts)
    response_dict = json.loads(response.text)

    return response_dict["data"]
