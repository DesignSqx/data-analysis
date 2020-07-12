import numpy as np
import pandas as pd
from pyecharts.charts import Bar, Line, Grid, Bar3D, Map, Scatter
from pyecharts import options as opts
import random
import re

df5 = None
df6 = None


# 各市房源累计数量
def one(df):
    df1 = df.city.value_counts()
    df1 = df1.sort_index()
    bar = Bar(init_opts=opts.InitOpts(width="1800px", height='800px'))
    bar.add_xaxis(df1.index.tolist())
    bar.add_yaxis("房源数量", df1.tolist())
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="各城市房源数量"),
        datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
    )
    bar.render("./result/1.html")


# 评论数数量和占比
def two(df):
    df1 = df.groupby('city').agg({'comment': np.mean})
    df11 = df1.agg({"comment": lambda x: format(x, '.0f')})
    x_data = df11.index.tolist()

    df2 = df.groupby('city').size()
    df21 = df[df.comment >= 100].groupby('city').size()
    df22 = df2.apply(lambda x: x == 0)
    df23 = df21.add(df22, fill_value=0)
    df24 = (df23 * 100 / df2).agg({"comment": lambda x: format(x, '.2f')}).tolist()

    bar = Bar(init_opts=opts.InitOpts(width="1800px", height='1000px'))
    bar.add_xaxis(x_data)
    bar.add_yaxis(
        "各个城市平均评论数",
        df11.comment.tolist(),
        yaxis_index=0,
        color="#5793f3",
        itemstyle_opts=opts.ItemStyleOpts(
            opacity='0.5'
        )

    ).extend_axis(
        yaxis=opts.AxisOpts(
            type_='value',
            name='百分比',

            position='right',
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#d14a61", )
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} %"),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    bar.set_global_opts(

        title_opts=opts.TitleOpts(title="各城市房源评论数"),
        datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        yaxis_opts=opts.AxisOpts(
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#5793f3", opacity='0.5')
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} 条"),

        ),
    )

    line = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis(
            "大于100评论数的占比",
            y_axis=df24,
            yaxis_index=1,
            color="#5793f3",
        )
    )
    bar.overlap(line)
    grid = Grid(init_opts=opts.InitOpts(width="1800px", height='800px'))
    grid.add(bar, opts.GridOpts(pos_left="5%", pos_right="5%"), is_control_axis_index=True)
    grid.render("./result/2.html")


# 规格居的数量
def three(df):
    df1 = df.groupby('province').size()
    x_data = df1.index.tolist()

    # df21 = df.iloc[:, 9].str.contains('1居')
    # df22 = df.iloc[:, 9].str.contains('2居')
    # df23 = df.iloc[:, 9].str.contains('3居')
    # df24 = df.iloc[:, 9].str.contains('4居')
    # df25 = df.iloc[:, 9].str.contains('5居')

    df2 = df[df['specs'].notnull()]
    df21 = df2[df2.specs.str.contains('1居')].groupby('province').size()
    df22 = df2[df2.specs.str.contains('2居')].groupby('province').size()
    df23 = df2[df2.specs.str.contains('3居')].groupby('province').size()
    df24 = df2[df2.specs.str.contains('4居')].groupby('province').size()
    df25 = df2[df2.specs.str.contains('5居')].groupby('province').size()

    df3 = df1.apply(lambda x: x == 0)
    df211 = df21.add(df3, fill_value=0).values.tolist()
    df221 = df22.add(df3, fill_value=0).values.tolist()
    df231 = df23.add(df3, fill_value=0).values.tolist()
    df241 = df24.add(df3, fill_value=0).values.tolist()
    df251 = df25.add(df3, fill_value=0).values.tolist()

    data = []
    for i in range(31):
        data.append([i, 0, df211[i]])
    for i in range(31):
        data.append([i, 1, df221[i]])
    for i in range(31):
        data.append([i, 2, df231[i]])
    for i in range(31):
        data.append([i, 3, df241[i]])
    for i in range(31):
        data.append([i, 4, df251[i]])

    c = (
        Bar3D(init_opts=opts.InitOpts(width="1800px", height='1000px'))
            .add(
            "",
            data,
            xaxis3d_opts=opts.Axis3DOpts(x_data, type_="category", interval=0),
            yaxis3d_opts=opts.Axis3DOpts(['1居', '2居', '3居', '4居', '5居'], type_="category"),
            zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=50),
            title_opts=opts.TitleOpts(title="规格分布"),
        )
            .set_series_opts(**{"stack": "stack"})
            .render("./result/3.html")
    )


# 在售和待售的比例
def four(df):
    df1 = df.groupby('province').size()
    x_data = df1.index.tolist()

    df2 = df[df['sale'].notnull()]
    df21 = df2[df2.sale.str.contains('在售')].groupby('province').size()
    df31 = df2[df2.sale.str.contains('待售')].groupby('province').size()

    df3 = df1.apply(lambda x: x == 0)
    df22 = df21.add(df3, fill_value=0)
    df32 = df31.add(df3, fill_value=0)

    df23 = (df22 * 100 / df1).agg({"comment": lambda x: format(x, '.2f')}).tolist()
    df33 = (df32 * 100 / df1).agg({"comment": lambda x: format(x, '.2f')}).tolist()

    c = (
        Line(init_opts=opts.InitOpts(width="1800px", height='800px'))
            .add_xaxis(x_data)
            .add_yaxis(
            "在售百分比",
            df23,
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
        )
            .add_yaxis(
            "待售百分比",
            df33,
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各省份在售与待售各自比例"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")], )
            .render("./result/4.html")
    )


# 各城市房价单价平均
def f_five(x):
    a = re.findall(r'[0-9]+', str(x))
    return int(a[0])


def five(df):
    df1 = df.groupby('city').size()
    x_data = df1.index.tolist()

    df2 = df[df['price'].notnull()]
    df21 = df2.loc[df2.price.str.contains('㎡'), {'city', 'price'}]
    df22 = df21.price.apply(f_five).to_frame().join(df21.city)
    df23 = df22.groupby("city").agg({'price': np.mean}).agg({"price": lambda x: format(x, '.2f')})

    global df5
    df5 = df23
    c = (
        Map(init_opts=opts.InitOpts(width="1800px", height='800px'))
            .add(
            "城市",
            [list(z) for z in zip(df23.index.tolist(), df23.values.tolist())],
            "china-cities",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各城市房价均值 元/㎡"),
            visualmap_opts=opts.VisualMapOpts(max_=20000, is_piecewise=True),
        )
            .render("./result/5.html")
    )


# 城市面积平均值
def f_six(x):
    # a = re.findall(r'[0-9]+', str(x))
    a = str(x).split('平米')[0].split('~')
    return int(a[0])


def six(df):
    df1 = df.groupby('city').size()
    x_data = df1.index.tolist()

    df2 = df[df['area'].notnull()]
    df21 = df2.loc[df2.area.str.contains('平米'), {'city', 'area'}]
    df22 = df21.area.apply(f_six).to_frame().join(df21.city)
    df23 = df22.groupby("city").agg({'area': np.mean}).agg({"area": lambda x: format(x, '.2f')})
    global df6
    df6 = df23
    c = (
        Map(init_opts=opts.InitOpts(width="1800px", height='800px'))
            .add(
            "城市",
            [list(z) for z in zip(df23.index.tolist(), df23.values.tolist())],
            "china-cities",
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各城市最低房源面积均值  平米"),
            visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True),
        )
            .render("./result/6.html")
    )


# 房源均值跟面积均值关系
def seven(df):
    df1 = df.groupby('city').size()
    x_data = df1.index.tolist()
    df1 = df5
    df2 = df6
    df3 = df1.join(df2)
    line = (
        Line(init_opts=opts.InitOpts(width="1800px", height='800px'))
            .add_xaxis(x_data)
            .add_yaxis("各城市最低房源面积均值  平米", df2.values.tolist(), yaxis_index=0)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="房源均值跟面积均值关系"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    ).extend_axis(
        yaxis=opts.AxisOpts(
            type_='value',
            name='房价',

            position='right',
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#d14a61", )
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} 元/㎡"),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    scatter = (
        Scatter()
            .add_xaxis(x_data)
            .add_yaxis("各城市房价均值 元/㎡", df1.values.tolist(), yaxis_index=1)
    )
    line.overlap(scatter)
    line.render("./result/7.html")


if __name__ == '__main__':
    df_read = pd.read_csv('./dashuju1.csv', encoding='utf-8')
    df_deal = df_read.dropna(subset=['address'])
    print(len(df_deal))
    one(df_deal)
    two(df_deal)
    three(df_deal)
    four(df_deal)
    five(df_deal)
    six(df_deal)
    seven(df_deal)
