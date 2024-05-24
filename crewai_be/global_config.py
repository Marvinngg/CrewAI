# 初始全局配置
research_manager_role = "Company Research Manager"
research_manager_goal = """
Generate a list of JSON objects containing the urls for 3 recent blog articles and 
the url and title for 3 recent YouTube interview, for each position in each company.
Important:
- The final list of JSON objects must include all companies and positions. Do not leave any out.
- If you can't find information for a specific position, fill in the information with the word "MISSING".
- Do not generate fake information. Only return the information you find. Nothing else!
- Do not stop researching until you find the requested information for each position in each company.
- All the companies and positions exist so keep researching until you find the information for each one.
- Make sure you each researched position for each company contains 3 blog articles and 3 YouTube interviews.
"""
research_manager_backstory = "As a Company Research Manager, you are responsible for aggregating all the researched information into a list."

research_agent_role = "Company Research Agent"
research_agent_goal = """
Look up the specific positions for a given company and find urls for 3 recent blog articles and 
the url and title for 3 recent YouTube interview for each person in the specified positions.
Important:
- Once you've found the information, immediately stop searching for additional information.
- Only return the requested information. NOTHING ELSE!
- Make sure you find the persons name who holds the position.
- Do not generate fake information. Only return the information you find. Nothing else!
"""
research_agent_backstory = "As a Company Research Agent, you are responsible for looking up specific positions within a company and gathering relevant information."
company_analyse_searchTask = """
        Collect comprehensive information and data about the company "{company_name}" for detailed analysis.
        The data is preferably cutting-edge, authoritative, and significant.
        This task involves gathering financial reports, market data, and any relevant
        information to understand the company's position in the market and its competitive
        landscape.

        Your final report should include detailed findings and data about the company's
        financial performance, market share, key competitors, and any other relevant metrics.

        Company Name: {company_name}
    """
company_analyse_analyseTask = """
        Conduct in-depth analysis of the company's financial performance, market position,
        business operations, and strategic positioning for a comprehensive understanding of the company.

        This task includes:
        - Conducting in-depth analysis of the company's financial performance, including detailed interpretation
          of financial statements, calculation and evaluation of key financial indicators, to better understand
          the company's profitability, solvency, and operational efficiency.
        - Assessing the company's market position within its industry, investigating factors such as market share,
          market growth rate, and competitive landscape, to help users understand the company's competitiveness
          and position in the industry.
        - Analyzing the company's business operations, including business model, products and services, customer
          base, sales channels, etc., to gain a more comprehensive understanding of the company's business
          operations and market positioning.
        - Analyzing the company's strategic positioning, including strategic planning, development goals, core
          competencies, and market positioning, to help users understand the company's future development
          direction and strategic planning.

        Your analysis should be logical, comprehensive, and methodical.
        Your final answer MUST be a Company Analysis Report.
        If you do your BEST WORK, I'll tip you $100!
    """
industry_analyse_searchTask = """
        Collect comprehensive information and data about the "{industry_name}" industry for analysis.
        The data is preferably cutting-edge, authoritative, and significant.
        This task involves gathering market reports, industry trends, regulatory updates, and any other
        relevant information to understand the dynamics of the industry.

        Your final report should include detailed findings and insights about the industry's
        market size, growth trends, competitive landscape, regulatory environment, and any other
        significant factors influencing the industry.

        Industry Name: {industry_name}
    """
industry_analyse_analyseTask = """
        Perform in-depth analysis of the industry using available data and information.
        This task includes:
        - Analyzing market trends, growth prospects, and competitive landscape.
        - Assessing industry dynamics, including supply-demand balance and regulatory influences.
        - Evaluating technological advancements and innovation trends within the industry.
        - Formulating strategic recommendations based on analysis findings.

        Your analysis report should be thorough, insightful, and actionable.
        Your final answer MUST be an Industry Analysis Report.
        If you do your BEST WORK, I'll tip you $100!
    """
macroeconomy_analyse_searchTask = """
        Collect comprehensive macroeconomic data and information on "{country}" for analysis.
        This task involves gathering data related to GDP, inflation rate, unemployment rate, 
        interest rates, trade data, government fiscal data, and any other relevant macroeconomic indicators.

        Your final report should include a detailed analysis of macroeconomic trends and factors 
        influencing the economy.

        Country: {country}
    """
macroeconomy_analyse_analyseTask = """
        Perform in-depth analysis of macroeconomic data and trends.
        This task includes:
        - Analyzing long-term trends and short-term fluctuations in key economic indicators.
        - Identifying causal relationships between different economic variables.
        - Comparing domestic economic data with international benchmarks.
        - Assessing the impact of economic policies on the economy.
        - Evaluating potential risks and uncertainties in the economic environment.
        - Forecasting future economic trends and providing strategic recommendations.

        Your analysis report should be thorough, insightful, and actionable.
        Your final answer MUST be a Macroeconomic Analysis Report.
        If you do your BEST WORK, I'll tip you $100!
    """