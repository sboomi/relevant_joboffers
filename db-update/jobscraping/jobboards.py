"""
This module has multiple classes for multiple jobboards to webscrap
"""


class JobBoard:
    """
    Defines a jobboard and provides methods to scrap from it
    """
    def __init__(self, name, id_job, url):
        """

        :param name: :type string: The name of the board
        :param id_job: :type string: The ID of the board (ALL CAPS)
        :param url: :type string: The URL of the board
        """
        self.name = name
        self.id = id
        self.url = url
        self.current_page = ""

    def access_page(self, keywords):
        """
        [Must be overridden] Method meant to return the query params

        :param keywords: keywords to evaluate
        """
        pass

    def set_current_url(self, current_url):
        self.current_page = current_url

    def go_to_n_page(self, n_page):
        pass

    def get_url_list(self):
        pass


class Indeed(JobBoard):
    def __init__(self):
        super.__init__("Indeed", "INDEED", "https://www.indeed.com/")
        self.last_element = ("css_selector", "div.pagination")
        self.target_elements = ("css_selector", "h2.title")

    def access_page(self, keywords):
        page_to_access = self.url + "/jobs?q=" + "+".join(keywords) + "&sort=date"
        self.set_current_url(page_to_access)
        return page_to_access

    def go_to_n_page(self, n_page):
        return self.current_url + f"&start={n_page * 10}"

    def get_url_list(self):
        pass


class Monster(JobBoard):
    def __init__(self):
        super.__init__("Monster", "MONSTER", "https://www.monster.com/")

    def access_page(self, keywords):
        pass

    def go_to_n_page(self, n_page):
        pass

    def get_url_list(self):
        pass


class RegionsJob(JobBoard):
    def __init__(self):
        super.__init__("RegionsJob", "REGJOB", "https://www.regionsjob.com/")

    def access_page(self, keywords):
        pass

    def go_to_n_page(self, n_page):
        pass

    def get_url_list(self):
        pass
