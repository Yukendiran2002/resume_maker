import streamlit as st
import random
from streamlit_chat import message
from langchain.agents import AgentExecutor, create_tool_calling_agent, create_structured_chat_agent, create_openai_tools_agent, create_self_ask_with_search_agent, create_openai_functions_agent, create_json_chat_agent
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langgraph.prebuilt import create_react_agent
import google.generativeai as genai
from tools import  extract_content, write_text_to_md, write_md_to_pdf, write_md_to_word, display_pdf, duckduckgo_general_search, duckduckgo_image_search, duckduckgo_news_search, duckduckgo_video_search, scrape_jobs_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
import asyncio
import nest_asyncio
import sys
nest_asyncio.apply()
# Streamlit Interface for Tool Management

display_pdf_tool = Tool(
    name="DisplayPDF",
    func=lambda path: display_pdf(path),
    description="Displays a PDF file. Input: File path of the PDF.",
)
write_md_tool = Tool(
    name="WriteMarkdown",
    func=lambda text: asyncio.run(write_text_to_md(text, "output")),  # Replace "output" with your desired path
    description="Writes text to a Markdown file. Input: Text content. Output: File path of the Markdown file.",
)
write_pdf_tool = Tool(
    name="WritePDF",
    func=lambda text: asyncio.run(write_md_to_pdf(text, "output")),
    description="Converts Markdown text to a PDF file. Input: Markdown text. Output: File path of the PDF file.",
)
write_word_tool = Tool(
    name="WriteWord",
    func=lambda text: asyncio.run(write_md_to_word(text, "output")),
    description="Converts Markdown text to a Word document. Input: Markdown text. Output: File path of the Word file.",
)

system = '''
    # **You are a Advanced ATS-Friendly Resume Builder with Keyword Matching and Skill Integration**
    You are a professional Resume Builder specializing in creating ATS-friendly, personalized resumes. Follow these steps and rules to create a tailored, consistent, and highly relevant resume for the user.

    ---

    ## **Core Rules**

    1. **Gather and Validate User Details**:
    - Collect information about the user, including full name, contact details, professional experience, skills, education, certifications, achievements, and any additional data the user wants to highlight.
    - Only include details that the user has explicitly provided. Do **not** update or add skills that the user has not mentioned, even if they are required in the job description.

    2. **Job Selection and Keyword Matching**:
    - Provide the user with a list of job titles (e.g., Data Analyst, Software Engineer) and let them select the most relevant job description.
    - Extract relevant keywords (skills, qualifications, tools, certifications, responsibilities) from the job description and categorize them into:
        - **Mandatory Keywords**: Essential skills or qualifications critical to the role.
        - **Preferred Keywords**: Skills or tools that add value but are not mandatory.
    - Match these keywords to the user’s provided skills, experiences, and qualifications.
    - For matched keywords:
        - Integrate them naturally into relevant sections, such as **Professional Summary**, **Key Skills**, or **Experience**.
    - For unmatched but critical keywords:
        - Create a dedicated section, such as **Eager to Learn** or **Professional Development Goals**, and include proactive language to showcase the user’s willingness to learn and grow.

    3. **Proactive Skill Integration**:
    - If a critical skill from the job description is missing:
        - Add a section like **Eager to Learn** and include proactive statements, such as:
        - *"Proactively pursuing proficiency in [missing skill/tool] to enhance capabilities for [specific job function]."*
    - Highlight the user’s commitment to acquiring these skills through training, certifications, or hands-on experience.
    - For preferred but less critical skills, include them only if they align with the user’s career goals and demonstrate honesty.

    4. **Ensure ATS Compatibility**:
    - Avoid complex formatting, graphics, tables, or design elements. Stick to clean, standard layouts with clear section headings.
    - Use ATS-friendly formatting, such as **bold** section titles and bullet points for clarity.
    - Ensure contact details include the full URL (not hidden by hyperlink text) and are clickable in the PDF version.

    5. **Resume Structure**:
    - **Header Section**:
        - Use **H1 format** for the user’s **Name** and center-align it at the top.
        - Center-align the **name** at the top of the resume in **H1** format (e.g., **JOHN DOE**).
        - Add contact details below the name, such as phone number, email, LinkedIn, GitHub, or any other relevant link.
        - Show the full URL instead of hyperlinking with text in contact details.
        - Ensure that contact details links are clickable in the PDF version.
        - Ensure that the contact details are clearly visible and well-organized at the top of the document and center aligned.
        - Center-align contact details below the name, showing phone, email, LinkedIn, GitHub, or other relevant URLs in full (e.g., https://linkedin.com/in/username).
    - **Professional Summary**:
        - Write a concise summary integrating relevant keywords from the job description and the user’s experience.
        - Use **H2 format** for the section title.
    - **Key Skills**:
        - List only skills the user has explicitly provided and that match the job description.
        - Use **H2 format** for the section title.
    - **Experience**:
        - Include job titles, company names, employment dates, and achievements in reverse-chronological order.
        - Use bullet points to describe responsibilities and accomplishments, ensuring keywords are incorporated naturally.
    - **Education**:
        - Include the user’s degree, institution, and graduation date.
        - Mention relevant coursework or projects if applicable.
    - **Certifications and Projects**:
        - Include certifications and significant projects relevant to the job description.
        - Use **H2 format** for section titles.
    - **Additional Sections (Optional)**:
        - Create additional sections like **Languages**, **Volunteer Work**, or **Awards**, based on user input.

    6. **ATS Score and Explanation**:
    - Calculate an **ATS Score** (0% to 100%) based on how closely the resume matches the job description keywords.
    - Provide a clear explanation of the score:
        - Highlight well-aligned sections and keywords.
        - Suggest areas for improvement, such as missing keywords or skills.

    7. **Minimize Blank Space**:
    - Fit the content on **one page** where possible, ensuring no unnecessary blank spaces.
    - Avoid extending the document for minor details or small sections.

    8. **Resume Format**:
    - Generate the resume in **Markdown Format** first for easy review and editing.
    - Convert the finalized Markdown resume into a **PDF Format** that maintains the clean, professional layout and ATS-friendly formatting.

    ---

    ## **Step-by-Step Resume Creation Process**

    1. **Collect User Information**: Gather details about the user’s skills, experience, and career goals.
    2. **Keyword Extraction**: Analyze the job description to identify and categorize mandatory and preferred keywords.
    3. **Match and Integrate Keywords**: Match relevant keywords with the user’s details, and incorporate them into appropriate sections.
    4. **Proactive Integration for Unmatched Skills**: Address unmatched keywords in a dedicated section like **Eager to Learn**, with honest and proactive language.
    5. **Optimize for ATS**: Ensure all content is ATS-compatible, including formatting and keyword placement.
    6. **ATS Score Calculation**: Evaluate the resume’s ATS alignment and provide actionable feedback for improvements.

    ---

    ## **Final Notes**
    - Ensure honesty and integrity by not falsely claiming expertise.
    - Use the dedicated **Eager to Learn** section to demonstrate adaptability for missing but critical skills.
    - Maintain consistency and professionalism throughout the resume.
    - Recreate and refine the resume with any updates or changes to ensure accuracy and relevance.
    - Ensure proper formatting, so the resume is professional, well-structured, and doesn't have unnecessary blank space. Aim for a **half or 3/4 page length** for a professional look.
    - Recreate the resume with any changes made to ensure consistency and accuracy in the final document.
    - Must follow the **Core Rules** and **Step-by-Step Process** to create a high-quality, tailored resume for the user.

    You have access to the following tools:
    {tools}
    Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).
    Valid "action" values: "Final Answer" or {tool_names}
    Provide only ONE action per $JSON_BLOB, as shown:
    ```
    {{
    "action": $TOOL_NAME,
    "action_input": $INPUT
    }}
    ```
    Follow this format:
    Question: input question to answer
    Thought: consider previous and subsequent steps
    Action:
    ```
    $JSON_BLOB
    ```
    Observation: action result
    ... (repeat Thought/Action/Observation N times)
    Thought: I know what to respond
    Action:
    ```
    {{
    "action": "Final Answer",
    "action_input": "Final response to human"
    }}
    Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools to ensure the answer is valid. Don't Respond directly even also it is appropriate. Format is Action:```$JSON_BLOB```then Observation'''

human = '''{input}
    {agent_scratchpad}
    (reminder to respond in a JSON blob no matter what)'''

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", human),
    ]
)
st.subheader("Search Chatbot")
if "model_list" not in st.session_state:
    st.session_state["model_list"] = []
if "api" not in st.session_state:
    st.session_state["api"] = None
if "memory" not in st.session_state:
    st.session_state["memory"] = InMemoryChatMessageHistory(session_id="test-session")
if "model" not in st.session_state:
    st.session_state['model'] = None
def model_list():
    if st.session_state.api is not None:
        genai.configure(api_key=st.session_state.api)
        data = genai.list_models()
        for model in data:
            if 'generateContent' in model.supported_generation_methods:
                if 'vision' not in model.name.lower():
                    if 'flash' in model.name.lower():
                        st.session_state.model_list.append(model.name.split('/')[-1])
st.sidebar.title("API")
st.session_state.api = st.sidebar.text_input("Enter your API key")
if st.session_state.model_list == []:
    try:
        model_list()
    except:
        pass
if len(st.session_state["model_list"]) > 1:
    st.session_state["model"] = st.sidebar.selectbox(
        "Select Model",
        st.session_state["model_list"],
        index=st.session_state["model_list"].index(st.session_state.get("model", st.session_state["model_list"][0])) if st.session_state.get("model") else 0,
        key="model_select",
    )
chat_container = st.container()
class ToolRegistry:# Add a method to get active tools in ToolRegistry
    def __init__(self):
        self._registry = {}
        self._active_tools = set()  # To track enabled tools

    def register_tool(self, name: str, func):
        """Registers a tool function with a given name."""
        if name in self._registry:
            raise ValueError(f"Tool with name '{name}' is already registered.")
        self._registry[name] = func
        self._active_tools.add(name)  # By default, tools are active

    def get_tool(self, name: str):
        """Retrieves a tool function by name."""
        return self._registry.get(name, None)

    def get_tools(self):
        """Get all currently active tool functions."""
        return [self._registry[name] for name in self._active_tools]
    
    def list_tools_name(self):
        """Lists all registered tools."""
        return list(self._registry.keys())

    def toggle_tool(self, name: str, enable: bool):
        """Enable or disable a tool."""
        if name not in self._registry:
            raise ValueError(f"Tool with name '{name}' is not registered.")
        if enable:
            self._active_tools.add(name)
        else:
            self._active_tools.discard(name)

# Instantiate a global tool registry
tool_registry = ToolRegistry()
def register_tools():
    if not hasattr(tool_registry, "_is_registered"):
        tool_registry.register_tool("extract_content", extract_content)
        tool_registry.register_tool("write_md_tool", write_md_tool)
        tool_registry.register_tool("write_pdf_tool", write_pdf_tool)
        tool_registry.register_tool("write_word_tool", write_word_tool)
        tool_registry.register_tool("display_pdf_tool", display_pdf_tool)
        tool_registry.register_tool("duckduckgo_general_search", duckduckgo_general_search)
        tool_registry.register_tool("duckduckgo_image_search", duckduckgo_image_search)
        tool_registry.register_tool("duckduckgo_news_search", duckduckgo_news_search)
        tool_registry.register_tool("duckduckgo_video_search", duckduckgo_video_search)
        tool_registry.register_tool("scrape_jobs_tool", scrape_jobs_tool)
        # Mark as registered
        tool_registry._is_registered = True

# Register the tools if not already registered
register_tools()
enabled = tool_registry.list_tools_name()
for tool_name in tool_registry.list_tools_name():
    tool_registry.toggle_tool(tool_name, tool_name in enabled)
# Load the tools from the registry
tools = tool_registry.get_tools()
def process_input(user_input):
    llm = ChatGoogleGenerativeAI(
        model=st.session_state.model,
        timeout=10,
        max_retries=2,
        api_key=st.session_state.api
    )
    agent = create_structured_chat_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools,return_intermediate_steps=True, early_stopping_method="force", verbose=False,handle_parsing_errors=True)
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: st.session_state["memory"],
        input_messages_key="input",
        history_messages_key="chat_history"
    )
    config = {"configurable": {"session_id": "test-session"}}
    response = agent_with_chat_history.invoke({"input":f"{user_input}"}, config)
    if "output" in response:
        # Handle file paths if the tool response includes them
        file_path = response["output"]
    return response

user_input = st.chat_input("Type your message and press Enter to send.")
if user_input:
    response = process_input(user_input)
    with chat_container:
        for i in range(len(response['chat_history'])):
            if response['chat_history'][i].type == 'human':
                chat_container.chat_message("user").write(response['chat_history'][i].content)
            if response['chat_history'][i].type == 'ai':
                chat_container.chat_message("assistant").write(response['chat_history'][i].content)
        chat_container.chat_message("user").write(user_input)
        chat_container.chat_message("assistant").write(response['output'])
