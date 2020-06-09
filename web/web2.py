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
chart = pygal.Bar(style=my_style, x_label_rotation=45, show_legend=False)
chart.title = 'Most-Starred Python Projects on GitHub'
chart.x_labels = names
chart.add('', stars)
chart.render_to_file('python_repos.svg')
