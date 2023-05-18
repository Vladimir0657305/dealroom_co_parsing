# dealroom.co parsing

This program does the following:

1. Imports the necessary modules: requests to send HTTP requests, urljoin from urllib.parse to join URLs, BeautifulSoup to parse HTML, time to delay execution, csv to write data to a CSV file, os to work with the operating system, and dotenv to load settings from an .env file.

2. Loads settings from the .env file using the load_dotenv() function.

3. Sets the value of the last_page variable to 91. This is the number of pages to be processed.

4. Sets the base URL and creates an empty firms_data list to store firm data.

5. Gets proxy server credentials from environment variables.

6. Specifies proxy server settings, including host, port, and credentials.

7. Creates a requests.Session() session, sets the session parameters, including the proxy server and disables SSL certificate verification.

8. Disable warnings about insecure requests with requests.packages.urllib3.disable_warnings().

9. Creates a global variable counter to keep track of the number of firms processed.

10. Starts a loop that will iterate through the pages until the last_page variable is reached.

11. Generates the URL of the current page and sends a GET request to get the page's HTML using requests.get().

12. Delays execution by 5 seconds so that the page has time to load.

13. Uses BeautifulSoup to parse HTML code and extract company links.

14. Creates a loop that will iterate over references to firms.

15. Loads the company page using session.get() and delays execution by 5 seconds to load the page.

16. Uses BeautifulSoup to extract business data such as name, description, website, and LinkedIn link.

17. Adds company data to the firms_data list.

18. Displays progress information.

19. Increases the value of the counter counter.

20. Checks the exit condition of the loop.

21. Opens dealroom_data.csv file to record results in CSV format.

22. Creates a csv.DictWriter object to write data to a CSV file.

23. Writes the header (column names) using the writer.writeheader() method.

24. Writes each firm's data to a CSV file using a for loop.

25. Closes the file.

[![trophy](https://github-profile-trophy.vercel.app/?username=Vladimir0657305)]([https://github.com/ryo-ma/github-profile-trophy](https://github.com/Vladimir0657305))

[![Ashutosh's github activity graph](https://github-readme-activity-graph.cyclic.app/graph?username=Vladimir0657305&theme=react)](https://github.com/ashutosh00710/github-readme-activity-graph)

![](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=Vladimir0657305&theme=solarized_dark)

![](https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=Vladimir0657305&theme=solarized_dark)
![](https://github-profile-summary-cards.vercel.app/api/cards/stats?username=Vladimir0657305&theme=solarized_dark)

![](https://komarev.com/ghpvc/?username=Vladimir0657305)
