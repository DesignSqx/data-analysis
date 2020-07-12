from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Pie
from pyecharts.commons.utils import JsCode
import numpy as np
import pandas as pd
import re


# 至少需要本科学历的比例
def eight(df):
    df1 = df.dropna(subset=['educational'])
    df11 = df1[df1.educational.str.contains('本科')]
    b = []
    a = format(len(df11) / len(df1), '.4f')
    b.append(a)

    c = (
        Liquid()
            .add(
            "本科学历占比",
            b,
            label_opts=opts.LabelOpts(
                font_size=50,
                formatter=JsCode(
                    """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
                ),
                position="inside",
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="本科学历占比"))
            .render("./result/8.html")
    )


# 工作经验要求饼图
def nine(df):
    df1 = df.dropna(subset=['experience'])
    df2 = df1[df1.experience.str.contains('工作经验')]
    df3 = df2.groupby('experience').size()
    c = (
        Pie(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add("", [list(z) for z in zip(df3.index.tolist(), df3.values.tolist())]
                 , center=["40%", "50%"], )
            .set_global_opts(title_opts=opts.TitleOpts(title="工作经验要求饼图"),
                             legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"), )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"),
                             )
            .render("./result/9.html")
    )


# 公司规模饼图
def ten(df):
    df1 = df.dropna(subset=['com_insize'])
    df2 = df1[df1.com_insize.str.contains('公司规模')]
    df3 = df2.groupby('com_insize').size()
    c = (
        Pie(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add(
            "",
            [list(z) for z in zip(df3.index.tolist(), df3.values.tolist())],
            radius=["40%", "55%"],
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 16, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="公司规模饼图"),
                             legend_opts=opts.LegendOpts(type_="scroll", pos_left="85%", orient="vertical"), )
            .render("./result/10.html")
    )


# 深圳最高工资的岗位数量
def eleven(df):
    df1 = df.dropna(subset=['experience'])
    df11 = df1.dropna(subset=['address'])
    df12 = df11.dropna(subset=['money'])

    df2 = df12[(df12.money.str.contains('月') & df12.address.str.contains('深圳'))]
    df21 = df2[df2.money.str.contains('千')].groupby('money').size()
    df22 = df2.loc[df2.money.str.contains('万'), 'money']
    df23 = df22.apply(f_eleven).to_frame().groupby('money').size()

    df3 = df23[df23.index <= 2]
    df31 = list(map(lambda x: str(x) + '万/月', df3.index.tolist()))

    df4 = df23[((df23.index > 2) & (df23.index <= 3))]
    df41 = list(map(lambda x: str(x) + '万/月', df4.index.tolist()))

    df5 = df23[df23.index > 3]
    df51 = list(map(lambda x: str(x) + '万/月', df5.index.tolist()))

    c = (
        Pie(init_opts=opts.InitOpts(width="1800px", height='1000px'))
            .add(
            "",
            [list(z) for z in zip(df21.index.tolist(), df21.values.tolist())],
            center=["20%", "30%"],
            radius=[120, 150],
            label_opts=opts.LabelOpts(is_show=False, position="center"),

        )
            .add(
            "",
            [list(z) for z in zip(df31, df3.values.tolist())],
            center=["60%", "30%"],
            radius=[120, 150],

        )
            .add(
            "",
            [list(z) for z in zip(df41, df4.values.tolist())],
            center=["20%", "70%"],
            radius=[120, 150],

        )
            .add(
            "",
            [list(z) for z in zip(df51, df5.values.tolist())],
            center=["60%", "70%"],
            radius=[120, 150],

        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="深圳各城市最高工资数量饼图"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="5%", pos_left="80%", orient="vertical"
            ),
        )
            .render("./result/11.html")
    )


# ----------------------------------------------------------------------------------------------

fn = """
    function(params) {
        if(params.name == '其他')
            return '\\n\\n\\n' + params.name + ' : ' + params.value + '%';
        return params.name + ' : ' + params.value + '%';
    }
    """


def new_label_opts():
    return opts.LabelOpts(formatter=JsCode(fn), position="center")


# -----------------------------------------------------------------------------------------------
def f_eleven(x):
    a = str(x).split('-')
    b = a[1].split('万')[0]
    return float(b)


# 全国和北京公司性质数量比较
def twelve(df):
    df1 = df
    df2 = df1[df1.com_nature.str.contains('公司性质')].groupby('com_nature').size()
    df3 = df1[(df1.com_nature.str.contains('公司性质')) & (df.address.str.contains('北京'))].groupby('com_nature').size()
    df4 = list(map(lambda x: str(x).replace('公司性质：', ''), df2.index.tolist()))

    c = (
        Bar(init_opts=opts.InitOpts(width="1800px", height='800px'))
            .add_xaxis(df4)
            .add_yaxis("全国公司性质", df2.values.tolist())
            .add_yaxis("北京公司性质", df3.values.tolist(), is_selected=False)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="全国与北京的公司规模数量比较"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts={"interval": "0"}
            ),
            yaxis_opts=opts.AxisOpts(max_=10000)
        )
            .render("./result/12.html")
    )


# 广州最高工资岗位数量
def thirteen(df):
    df1 = df
    df11 = df1.dropna(subset=['address'])
    df12 = df11.dropna(subset=['money'])

    df2 = df12[(df12.money.str.contains('月') & df12.address.str.contains('广州'))]
    df21 = df2[df2.money.str.contains('千')].groupby('money').size()
    df22 = df2.loc[df2.money.str.contains('万'), 'money']
    df23 = df22.apply(f_thirteen).to_frame().groupby('money').size()

    df3 = df23[df23.index <= 2]
    df31 = list(map(lambda x: str(x) + '万/月', df3.index.tolist()))

    df4 = df23[((df23.index > 2) & (df23.index <= 3))]
    df41 = list(map(lambda x: str(x) + '万/月', df4.index.tolist()))

    df5 = df23[df23.index > 3]
    df51 = list(map(lambda x: str(x) + '万/月', df5.index.tolist()))

    c = (
        Pie(init_opts=opts.InitOpts(width="1800px", height='1000px'))
            .add(
            "",
            [list(z) for z in zip(df21.index.tolist(), df21.values.tolist())],
            center=["20%", "30%"],
            radius=[80, 150],
            label_opts=opts.LabelOpts(is_show=False, position="center"),

        )
            .add(
            "",
            [list(z) for z in zip(df31, df3.values.tolist())],
            center=["60%", "30%"],
            radius=[80, 150],

        )
            .add(
            "",
            [list(z) for z in zip(df41, df4.values.tolist())],
            center=["20%", "70%"],
            radius=[80, 150],

        )
            .add(
            "",
            [list(z) for z in zip(df51, df5.values.tolist())],
            center=["60%", "70%"],
            radius=[80, 150],

        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="广州各城市最高工资数量饼图"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="5%", pos_left="80%", orient="vertical"
            ),
        )
            .render("./result/13.html")
    )


def f_thirteen(x):
    a = str(x).split('-')
    b = a[1].split('万')[0]
    return float(b)


# 北京最高工资岗位数量
def fourteen(df):
    df1 = df
    df11 = df1.dropna(subset=['address'])
    df12 = df11.dropna(subset=['money'])

    df2 = df12[(df12.money.str.contains('月') & df12.address.str.contains('北京'))]
    df21 = df2[df2.money.str.contains('千')].groupby('money').size()
    df22 = df2.loc[df2.money.str.contains('万'), 'money']
    df23 = df22.apply(f_thirteen).to_frame().groupby('money').size()

    df3 = df23[df23.index <= 2]
    df31 = list(map(lambda x: str(x) + '万/月', df3.index.tolist()))

    df4 = df23[((df23.index > 2) & (df23.index <= 3))]
    df41 = list(map(lambda x: str(x) + '万/月', df4.index.tolist()))

    df5 = df23[df23.index > 3]
    df51 = list(map(lambda x: str(x) + '万/月', df5.index.tolist()))

    c = (
        Pie(init_opts=opts.InitOpts(width="1800px", height='1000px'))
            .add(
            "",
            [list(z) for z in zip(df21.index.tolist(), df21.values.tolist())],
            center=["20%", "30%"],
            radius=[80, 150],
            label_opts=opts.LabelOpts(is_show=False, position="center"),

        )
            .add(
            "",
            [list(z) for z in zip(df31, df3.values.tolist())],
            center=["60%", "30%"],
            radius=[80, 150],

        )
            .add(
            "",
            [list(z) for z in zip(df41, df4.values.tolist())],
            center=["20%", "70%"],
            radius=[80, 150],

        )
            .add(
            "",
            [list(z) for z in zip(df51, df5.values.tolist())],
            center=["60%", "70%"],
            radius=[80, 150],

        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="北京各城市最高工资数量饼图"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="5%", pos_left="80%", orient="vertical"
            ),
        )
            .render("./result/14.html")
    )


def f_fourteen(x):
    a = str(x).split('-')
    b = a[1].split('万')[0]
    return float(b)


# 比较广州房价跟工资
def fifteen(dff, dfj):
    df2 = dff[dff['price'].notnull()]
    df21 = df2.loc[df2.price.str.contains('㎡'), {'city', 'price'}]
    df22 = df21.price.apply(f_fifteen).to_frame().join(df21.city)
    # 两个series
    df23 = df22[(df22.city.str.contains('广州')) & (df22.price < 10000)].agg({'price': np.mean}).agg({"price": lambda x: format(x, '.2f')})
    df24 = df22[(df22.city.str.contains('广州')) & (df22.price >= 10000)].agg({'price': np.mean}).agg({"price": lambda x: format(x, '.2f')})
    a = df23.values[0]
    b = df24.values[0]


    df3 = dfj.dropna(subset=['money'])
    df32 = df3[(df3.money.str.contains('月')) & (df3.address.str.contains('广州')) & (df3.money.str.contains('-'))]
    df41 = df32.loc[df32.money.str.contains('千'), 'money'].apply(f_fifteen1)
    df42 = float(format(df41.mean(), '.6f')) * 1000
    df51 = df32.loc[df32.money.str.contains('万'), 'money'].apply(f_fifteen2)
    df52 = float(format(df51.mean(), '.6f')) * 10000

    c = (
        Bar(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="elasticOut"
                )
            )
        )
            .add_xaxis(['少于10000', '至少10000'])
            .add_yaxis("平均房价", [a, b])
            .add_yaxis("平均工资", [df42, df52])
            .set_global_opts(title_opts=opts.TitleOpts(title="广州房价跟工资的比较", subtitle="都是均值  单位：元（元/平米）"))
            .render("./result/15.html")
    )

def f_fifteen(x):
    a = re.findall(r'[0-9]+', str(x))
    return int(a[0])

def f_fifteen1(x):
    a = str(x).split('-')
    b = a[1].split('千')[0]
    return float(b)

def f_fifteen2(x):
    a = str(x).split('-')
    b = a[1].split('万')[0]
    return float(b)


if __name__ == '__main__':
    df_read = pd.read_csv('./dashuju2.csv', encoding='utf-8')
    df_deal = df_read.dropna(subset=['job_name'])
    df_read1 = pd.read_csv('./dashuju1.csv', encoding='utf-8')
    df_deal1 = df_read1.dropna(subset=['address'])
    print(len(df_deal))
    eight(df_deal)
    nine(df_deal)
    ten(df_deal)
    eleven(df_deal)
    twelve(df_deal)
    thirteen(df_deal)
    fourteen(df_deal)
    fifteen(df_deal1, df_deal)
