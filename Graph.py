import folium
from pyecharts import Pie, Geo, Bar

def draw_distribution_map(world_geo, df_gp_index, string, save_path):
    star_map = folium.Map(location=[-121, 38.5], tiles='Mapbox Bright', zoom_start=3.5)
    star_map.choropleth(geo_data=world_geo, data=df_gp_index,
                        columns=[string, 'count'],
                        key_on='feature.properties.POSTAL',
                        threshold_scale=[0, 2000, 5000, 9000, 12000, 15000],
                        fill_color='YlOrRd', fill_opacity=0.6, line_opacity=0.3,
                        legend_name='Amount of Starbucks in the country')
    star_map.save(save_path)
#     os.path.join('D:\\file\starbucks',


def bar_pic(df_gp_index, name, x_label, y_label):
    bar = Bar(name)
    attr = []
    v = []
    for index, value in enumerate(df_gp_index[x_label]):
        attr.append(df_gp_index[x_label][index])
        v.append(df_gp_index[y_label][index])
    bar.add(name, attr, v)
    return bar


def pie_pic(df_gp_index, name, x_label, y_label):
    pie = Pie(name)
    attr = []
    v = []
    for index, value in enumerate(df_gp_index[x_label]):
        attr.append(df_gp_index[x_label][index])
        v.append(df_gp_index[y_label][index])
    pie.add(name, attr, v, is_label_show=True, radius=[30, 55], rosetype='radius')
    return pie



def geo_formatter(params):
    return params.name


def draw_map(df, map_html):
    geo = Geo("星巴克店铺分布图",
              title_color="#fff", title_pos="center",
              width=1200, height=500, background_color='#404a59')

    geo_cities_coords = {df.iloc[i]['Store Name']: [df.iloc[i]['lon'], df.iloc[i]['lat']] for i in range(len(df))}
    value = list(df['Average Score'])
    attr = list(df['Store Name'])

    geo.add("", attr, value,
            visual_range=[0, 10], visual_text_color="#fff",
            visual_split_number=5,
            maptype="world",
            is_visualmap=True, is_piecewise=True,
            geo_formatter=geo_formatter,
            symbol_size=5, center=(113, 23),
            geo_cities_coords=geo_cities_coords)
    geo.render(map_html)


def draw_timezone_map(df, map_html):
    geo = Geo("星巴克时区分布地图",
              title_color="#fff", title_pos="center",
              width=1200, height=500, background_color='#404a59')
    geo_cities_coords = {df.iloc[i]['Store Name']: [df.iloc[i]['lon'], df.iloc[i]['lat']] for i in range(len(df))}
    attr = list(df['Store Name'])
    value = list(df['timezone_amount'])
    geo.add("", attr, value, visual_text_color="#fff",
            maptype="world",
            visual_range=[0, 2000],
            is_visualmap=True,
            symbol_size=5, center=(-121, 38.5),
            tooltip_formatter=geo_formatter,
            geo_cities_coords=geo_cities_coords)
    geo.render(map_html)


