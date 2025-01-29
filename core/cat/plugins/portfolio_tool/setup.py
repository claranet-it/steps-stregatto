from cat.mad_hatter.decorators import hook, tool
from cat.plugins.portfolio_tool.services.brickly_service_factory import (
    BricklyServiceFactory,
)


@tool(
    examples=[
        "Tell me who is free from april",
        "Who has <= 50 effort from april?",
        "I'm looking for developers who have at least 40% effort available for the month of may",
        "Can you show me the data of the people effort?",
        "show me developers free from May",
        "show me someone who is available from june",
        "give me someone who is free from April",
        "give me someone available from may",
        "Can you show me developers who are free from April and have skills in Python?",
        "Who has <= 50 effort from April and knows PHP?",
        "I'm looking for developers who have at least 40% effort available for the month of May and are skilled in "
        "JavaScript.",
        "Can you show me the data of the people who know Python and their availability in April?",
        "Show me developers free from May who have skills in PHP.",
        "Is there someone available from June who knows Elixir?",
        "Can you give me someone who is free from April and knows JavaScript?",
        "Show me developers who are available from May and have skills in Python.",
        "Can you show me developers who have at least 40% effort available for the month of May and are skilled in "
        "Python?",
        "Who has <= 50 effort from April and is available in June?",
        "I'm looking for developers who are free from April and have skills in PHP.",
        "Can you show me the data of the people who know JavaScript and their availability in May?",
        "Show me developers free from May who have skills in Elixir.",
        "Is there someone available from June who knows Python?",
        "Can you give me someone who is free from April and has skills in Java?",
        "Show me developers who are available from May and have skills in Ruby.",
        "show me developers with skills in python",
        "show me developers with skills in php",
        "developers with javascript skills",
        "show me who knows python",
        "give me someone that knows php",
        "is there someone that knows elixir",
    ]
)
def get_data(skill_month, cat):
    """
    Useful for finding developers with skills in certain programming languages and their available effort
    Input is a string formatted as: programmingLanguage-month
    If programmingLanguage is not provided it will be None-month
    If month is not provided it will be programmingLanguage-None
    """

    # settings = cat.mad_hatter.get_plugin().load_settings()

    inputs = skill_month.split("-")
    programming_language = inputs[0]
    month = inputs[1]

    result = {}

    skills_service = BricklyServiceFactory.get_brickly_skills_service(
        cat.portfolio_token
    )
    effort_service = BricklyServiceFactory.get_brickly_effort_service(
        cat.portfolio_token
    )
    # networking_service = BricklyServiceFactory.get_brickly_networking_service(
    #     cat.portfolio_token
    # )

    result["Skills"] = skills_service.get_result(programming_language)
    result["Available Effort"] = effort_service.get_result(month)

    # if settings["include_networking"]:
    #     result["External companies"] = networking_service.get_result(
    #         programming_language
    #     )

    return result


@hook(priority=1)
def agent_prompt_prefix(prefix, cat):
    prefix += """Your task is to assist in identifying suitable individuals within a developer team for a specific 
    project, based on the skills and available time of each team member. You are not permitted to invent information, 
    search the web for answers. Instead, you should only use the data provided by the 
    assistant. The available time of each developer is defined by the "effort" parameter, 
    which is expressed on a monthly basis. An effort value of 100 indicates that the developer has 100% of their time 
    available for new projects, while an effort value of 0 indicates that they have no available time. When providing 
    a list of potential matches, you should include the name of the developer, their skill level (which ranges from 0 
    to 3), and their available effort as a percentage. You should only consider developers with a skill level of 2 or 
    3 for the project. Your list should be as complete as possible, including all potential matches within the team. 
    """
    # Additionally, you may be provided with data from external companies. If there is a match with an external
    # company, you should include this as an option in your list, along with a brief description of the company. You
    # don't need to provide details about the name and skills of the developers from the external company."""

    return prefix
