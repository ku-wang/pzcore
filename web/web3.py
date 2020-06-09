import requests
import pygal
from decorator_module import retry
from log_module import log_m
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

logger = log_m.logger
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)

# 将API响应存储在一个变量中
response_dict = r.json()
print("Total repositories:", response_dict['total_count'])
# 研究有关仓库的信息
repo_dicts = response_dict['items']
names, stars = [], []

for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    stars.append(repo_dict['stargazers_count'])

my_style = LS('#333366', base_style=LCS)

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000
chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most-Starred Python Projects on GitHub'
chart.x_labels = names
chart.add('', stars)
chart.render_to_file('python_repos.svg')