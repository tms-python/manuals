import requests
from bs4 import BeautifulSoup as BS


def get_html_data(date: str) -> BS:
    """
    :param date: format will be '20191203'
    :return: BS instance
    """
    response = requests.get(f'https://classic.sportsbookreview.com/betting-odds/nhl-hockey/?date={date}')
    content = response.content.decode()
    soup = BS(content)
    return soup


def make_score_list(tag, class_name=None):
    tag = tag.findNext("div", {"class": class_name}).findAll('div')
    tag = [container.text for container in tag]
    return tag


def make_command_list(commands):
    commands_result = {}
    for command in commands.findAll('div', {'class': 'eventLine-value'}):
        try:
            winner = command.find("span", {"class": "icons-winner-arrow"})
            command = command.find("span", {"class": "team-name"})
            command = command.findNext("a").text
            commands_result['WINNER' if winner else 'LOOSER'] = command
        except:
            pass
    return commands_result


def get_result_data(lst):
    RESULT_LIST = []

    for el in lst:
        # print(el.prettify())
        element = el.findNext("div", {"class": "status-complete"})
        time = element.find("div", {"class": "el-div eventLine-time"}).text
        commands = element.find("div", {"class": "el-div eventLine-team"})
        opener = make_score_list(element, "el-div eventLine-opener")
        score = element.findAll("div", {"class": "el-div eventLine-book"})
        # print(score)
        score = [[container.text for container in el] for el in score]

        result_dict = {'date': DATE}
        result_dict['time'] = time
        result_dict['commands'] = make_command_list(commands)
        result_dict['opener'] = opener
        result_dict['score'] = score

        RESULT_LIST.append(result_dict)

    return RESULT_LIST


if __name__ == '__main__':
    """
    ПОМЕНЯТЬ ДАТУ НА ТРЕБУЕМУЮ В ФОРМАТЕ "ГГГГММДД"
    """
    DATE = '20200225'
    SOUP = get_html_data(date=DATE)
    LIST_WITH_FINISHED_MATCH = SOUP.find("div", {"class": "content-final content-complete"})
    RESULT_LIST = get_result_data(LIST_WITH_FINISHED_MATCH)
    print(RESULT_LIST)