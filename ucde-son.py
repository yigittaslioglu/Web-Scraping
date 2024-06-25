import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from io import StringIO, BytesIO
import streamlit.components.v1 as components
import json
import time as ts
from IPython.core.display import HTML
df1 = pd.read_excel("HAZIRAN-24.06.2024-STOK-RAPORU.xlsx")

# tüm kolonlardaki tüm veriler büyük harfle düzeltildi ve bir standarda oturtuldu
for column in df1.columns:
    if df1[column].dtype == 'object' or df1[column].dtype == 'datetime64':
        df1[column] = df1[column].str.upper()
        
df1["MODEL"] = df1["MODEL"].str.replace("IPHONE", "İPHONE")
        
df = df1[["ARIZAID","MARKA","MODEL","STATU","TOPLAM ISLEM MALIYETI","SMART ALIM GRADE","CIKIS SEVIYE","CAGRI KAYIT TARIHI","SON ISLEM TARIHI"]]


st.set_page_config(page_title="Raporlar", page_icon=":bar_chart:", layout="wide")  # bulamadım şimdilik

st.sidebar.header("Sayfa Seçin")  # sidebar ana naşlık

page = st.sidebar.radio(                                                         
   "Sayfalar:",                                                               # sidebar alt başlık ve burada oluşturmak istediğim raporları yazıyorum ve sayfarı oluşturuyor. 
  ("STOK RAPORLARI", "SATIS RAPORLARI", "YEDEK PARCA MALIYET RAPORLARI", "PERSONEL RAPORLARI","ONAYLANMASI GEREKEN CIHAZLAR")      # radio metodu yuvarlak seçenek seçtirerek ayrı ayrı sayfalar oluşturuyor.  
)

if page == "STOK RAPORLARI":

    ######################################################################################################################
    ######################################################################################################################
    ############################### MARKA DAĞILIM VE ADETLERİ


    st.write("Bu rapor, Marka, Model ve Çıkış Seviyesi adetleri hakkında bilgi sağlar. Aşağıda detaylı analiz ve grafikler yer almaktadır.")

    st.title("MARKA DAĞILIM ve ADETLERİ")

    # Marka bazında gruplama
    grouped_data = df['MARKA'].value_counts().reset_index()
    grouped_data.columns = ['MARKA', 'ADET']

    # DataFrame'i JavaScript formatına dönüştür
    chart_data = grouped_data.to_dict(orient='records')

    # chart_data'yı JSON formatında stringe çevir
    chart_data_json = json.dumps(chart_data)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
        am4core.ready(function() {{

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart3D);

        // Add data
        chart.data = {chart_data_json};

        // Create axes
        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "MARKA";
        categoryAxis.renderer.labels.template.rotation = 270;
        categoryAxis.renderer.labels.template.hideOversized = false;
        categoryAxis.renderer.minGridDistance = 20;
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.tooltip.label.rotation = 270;
        categoryAxis.tooltip.label.horizontalCenter = "right";
        categoryAxis.tooltip.label.verticalCenter = "middle";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "ADET";
        valueAxis.title.fontWeight = "bold";

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries3D());
        series.dataFields.valueY = "ADET";
        series.dataFields.categoryX = "MARKA";
        series.name = "Adet";
        series.tooltipText = "{{categoryX}}: [bold]{{valueY}}[/]";
        series.columns.template.fillOpacity = .8;

        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        columnTemplate.stroke = am4core.color("#FFFFFF");

        columnTemplate.adapter.add("fill", function(fill, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        columnTemplate.adapter.add("stroke", function(stroke, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        // Add labels on columns
        var labelBullet = series.bullets.push(new am4charts.LabelBullet());
        labelBullet.label.text = "{{valueY}}";
        labelBullet.label.dy = -10;
        labelBullet.label.hideOversized = false;
        labelBullet.label.truncate = false;

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.lineX.strokeOpacity = 0;
        chart.cursor.lineY.strokeOpacity = 0;

        }}); // end am4core.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

    st.write("---------------------------------------------------------------------------------")

    ################################# labelBullet.label.text = "{---{valueY}---}"; EKSİK OLDUĞUNDA BİR TANE DAHA SÜSLÜ PARANTEZ EKLE, BİR TANE SÜSLÜ PARANTEZ EKSİK GELİYOR GENELDE 

    ######################################################################################################################
    ######################################################################################################################
    ############################### MODEL DAĞILIM VE ADETLERİ

    st.title("MODEL DAĞILIM ve ADETLERİ")

    # Marka bazında gruplama
    grouped_data = df['MODEL'].value_counts().head(20).reset_index()
    grouped_data.columns = ['MODEL', 'ADET']

    # DataFrame'i JavaScript formatına dönüştür
    chart_data = grouped_data.to_dict(orient='records')

    # chart_data'yı JSON formatında stringe çevir
    chart_data_json = json.dumps(chart_data)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
        am4core.ready(function() {{

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart3D);

        // Add data
        chart.data = {chart_data_json};

        // Create axes
        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "MODEL";
        categoryAxis.renderer.labels.template.rotation = 270;
        categoryAxis.renderer.labels.template.hideOversized = false;
        categoryAxis.renderer.minGridDistance = 20;
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.tooltip.label.rotation = 270;
        categoryAxis.tooltip.label.horizontalCenter = "right";
        categoryAxis.tooltip.label.verticalCenter = "middle";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "ADET";
        valueAxis.title.fontWeight = "bold";

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries3D());
        series.dataFields.valueY = "ADET";
        series.dataFields.categoryX = "MODEL";
        series.name = "Adet";
        series.tooltipText = "{{categoryX}}: [bold]{{valueY}}[/]";
        series.columns.template.fillOpacity = .8;

        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        columnTemplate.stroke = am4core.color("#FFFFFF");

        columnTemplate.adapter.add("fill", function(fill, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        columnTemplate.adapter.add("stroke", function(stroke, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        // Add labels on columns
        var labelBullet = series.bullets.push(new am4charts.LabelBullet());
        labelBullet.label.text = "{{valueY}}";
        labelBullet.label.dy = -10;
        labelBullet.label.hideOversized = false;
        labelBullet.label.truncate = false;

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.lineX.strokeOpacity = 0;
        chart.cursor.lineY.strokeOpacity = 0;

        }}); // end am4core.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

    st.write("---------------------------------------------------------------------------------")



    ######################################################################################################################
    ######################################################################################################################
    ############################### SMART ALIM GRADE DAĞILIM VE ADETLERİ

    st.title("SMART ALIM GRADE DAĞILIM ve ADETLERİ")

    # Marka bazında gruplama
    grouped_data = df['SMART ALIM GRADE'].value_counts().reset_index()
    grouped_data.columns = ['SMART ALIM GRADE', 'ADET']

    # DataFrame'i JavaScript formatına dönüştür
    chart_data = grouped_data.to_dict(orient='records')

    # chart_data'yı JSON formatında stringe çevir
    chart_data_json = json.dumps(chart_data)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
        am4core.ready(function() {{

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart3D);

        // Add data
        chart.data = {chart_data_json};

        // Create axes
        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "SMART ALIM GRADE";
        categoryAxis.renderer.labels.template.rotation = 270;
        categoryAxis.renderer.labels.template.hideOversized = false;
        categoryAxis.renderer.minGridDistance = 20;
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.tooltip.label.rotation = 270;
        categoryAxis.tooltip.label.horizontalCenter = "right";
        categoryAxis.tooltip.label.verticalCenter = "middle";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "ADET";
        valueAxis.title.fontWeight = "bold";

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries3D());
        series.dataFields.valueY = "ADET";
        series.dataFields.categoryX = "SMART ALIM GRADE";
        series.name = "Adet";
        series.tooltipText = "{{categoryX}}: [bold]{{valueY}}[/]";
        series.columns.template.fillOpacity = .8;

        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        columnTemplate.stroke = am4core.color("#FFFFFF");

        columnTemplate.adapter.add("fill", function(fill, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        columnTemplate.adapter.add("stroke", function(stroke, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        // Add labels on columns
        var labelBullet = series.bullets.push(new am4charts.LabelBullet());
        labelBullet.label.text = "{{valueY}}";
        labelBullet.label.dy = -10;
        labelBullet.label.hideOversized = false;
        labelBullet.label.truncate = false;

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.lineX.strokeOpacity = 0;
        chart.cursor.lineY.strokeOpacity = 0;

        }}); // end am4core.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

    st.write("---------------------------------------------------------------------------------")


    ######################################################################################################################
    ######################################################################################################################
    ############################### CIKIS SEVIYE DAĞILIM VE ADETLERİ

    st.title("CIKIS SEVIYE DAĞILIM ve ADETLERİ")

    # Marka bazında gruplama
    grouped_data = df['CIKIS SEVIYE'].value_counts().reset_index()
    grouped_data.columns = ['CIKIS SEVIYE', 'ADET']

    # DataFrame'i JavaScript formatına dönüştür
    chart_data = grouped_data.to_dict(orient='records')

    # chart_data'yı JSON formatında stringe çevir
    chart_data_json = json.dumps(chart_data)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
        am4core.ready(function() {{

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart3D);

        // Add data
        chart.data = {chart_data_json};

        // Create axes
        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "CIKIS SEVIYE";
        categoryAxis.renderer.labels.template.rotation = 0;
        categoryAxis.renderer.labels.template.hideOversized = false;
        categoryAxis.renderer.minGridDistance = 20;
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.tooltip.label.rotation = 270;
        categoryAxis.tooltip.label.horizontalCenter = "right";
        categoryAxis.tooltip.label.verticalCenter = "middle";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "ADET";
        valueAxis.title.fontWeight = "bold";

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries3D());
        series.dataFields.valueY = "ADET";
        series.dataFields.categoryX = "CIKIS SEVIYE";
        series.name = "Adet";
        series.tooltipText = "{{categoryX}}: [bold]{{valueY}}[/]";
        series.columns.template.fillOpacity = .8;

        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        columnTemplate.stroke = am4core.color("#FFFFFF");

        columnTemplate.adapter.add("fill", function(fill, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        columnTemplate.adapter.add("stroke", function(stroke, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        // Add labels on columns
        var labelBullet = series.bullets.push(new am4charts.LabelBullet());
        labelBullet.label.text = "{{valueY}}";
        labelBullet.label.dy = -10;
        labelBullet.label.hideOversized = false;
        labelBullet.label.truncate = false;

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.lineX.strokeOpacity = 0;
        chart.cursor.lineY.strokeOpacity = 0;

        }}); // end am4core.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

    st.write("---------------------------------------------------------------------------------")


    ######################################################################################################################
    ######################################################################################################################
    ############################### MARKA BAZLI DAĞILIM VE ADETLERİ
    ############################### APPLE


    st.title("MARKA BAZLI DAĞILIM ve ADETLERİ")
    st.title("APPLE")


    # Marka bazında gruplama
    grouped_data = df[df["MARKA"] == "APPLE"]["CIKIS SEVIYE"].value_counts().reset_index()
    grouped_data.columns = ['CIKIS SEVIYE', 'ADET']

    # DataFrame'i JavaScript formatına dönüştür
    chart_data = grouped_data.to_dict(orient='records')

    # chart_data'yı JSON formatında stringe çevir
    chart_data_json = json.dumps(chart_data)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
        am4core.ready(function() {{

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart3D);

        // Add data
        chart.data = {chart_data_json};

        // Create axes
        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "CIKIS SEVIYE";
        categoryAxis.renderer.labels.template.rotation = 0;
        categoryAxis.renderer.labels.template.hideOversized = false;
        categoryAxis.renderer.minGridDistance = 20;
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.tooltip.label.rotation = 270;
        categoryAxis.tooltip.label.horizontalCenter = "right";
        categoryAxis.tooltip.label.verticalCenter = "middle";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "ADET";
        valueAxis.title.fontWeight = "bold";

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries3D());
        series.dataFields.valueY = "ADET";
        series.dataFields.categoryX = "CIKIS SEVIYE";
        series.name = "Adet";
        series.tooltipText = "{{categoryX}}: [bold]{{valueY}}[/]";
        series.columns.template.fillOpacity = .8;

        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        columnTemplate.stroke = am4core.color("#FFFFFF");

        columnTemplate.adapter.add("fill", function(fill, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        columnTemplate.adapter.add("stroke", function(stroke, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        // Add labels on columns
        var labelBullet = series.bullets.push(new am4charts.LabelBullet());
        labelBullet.label.text = "{{valueY}}";
        labelBullet.label.dy = -10;
        labelBullet.label.hideOversized = false;
        labelBullet.label.truncate = false;

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.lineX.strokeOpacity = 0;
        chart.cursor.lineY.strokeOpacity = 0;

        }}); // end am4core.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

    st.write("---------------------------------------------------------------------------------")


    ######################################################################################################################
    ######################################################################################################################
    ############################### MARKA BAZLI DAĞILIM VE ADETLERİ
    ############################### SAMSUNG

    st.title("SAMSUNG")


    # Marka bazında gruplama
    grouped_data = df[df["MARKA"] == "SAMSUNG"]["CIKIS SEVIYE"].value_counts().reset_index()
    grouped_data.columns = ['CIKIS SEVIYE', 'ADET']

    # DataFrame'i JavaScript formatına dönüştür
    chart_data = grouped_data.to_dict(orient='records')

    # chart_data'yı JSON formatında stringe çevir
    chart_data_json = json.dumps(chart_data)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
        am4core.ready(function() {{

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart3D);

        // Add data
        chart.data = {chart_data_json};

        // Create axes
        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "CIKIS SEVIYE";
        categoryAxis.renderer.labels.template.rotation = 0;
        categoryAxis.renderer.labels.template.hideOversized = false;
        categoryAxis.renderer.minGridDistance = 20;
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.tooltip.label.rotation = 270;
        categoryAxis.tooltip.label.horizontalCenter = "right";
        categoryAxis.tooltip.label.verticalCenter = "middle";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "ADET";
        valueAxis.title.fontWeight = "bold";

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries3D());
        series.dataFields.valueY = "ADET";
        series.dataFields.categoryX = "CIKIS SEVIYE";
        series.name = "Adet";
        series.tooltipText = "{{categoryX}}: [bold]{{valueY}}[/]";
        series.columns.template.fillOpacity = .8;

        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        columnTemplate.stroke = am4core.color("#FFFFFF");

        columnTemplate.adapter.add("fill", function(fill, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        columnTemplate.adapter.add("stroke", function(stroke, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        // Add labels on columns
        var labelBullet = series.bullets.push(new am4charts.LabelBullet());
        labelBullet.label.text = "{{valueY}}";
        labelBullet.label.dy = -10;
        labelBullet.label.hideOversized = false;
        labelBullet.label.truncate = false;

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.lineX.strokeOpacity = 0;
        chart.cursor.lineY.strokeOpacity = 0;

        }}); // end am4core.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

    st.write("---------------------------------------------------------------------------------")

    ######################################################################################################################
    ######################################################################################################################
    ############################### MARKA BAZLI DAĞILIM VE ADETLERİ
    ############################### XIAOMI

    st.title("XIAOMI")


    # Marka bazında gruplama
    grouped_data = df[df["MARKA"] == "XIAOMI"]["CIKIS SEVIYE"].value_counts().reset_index()
    grouped_data.columns = ['CIKIS SEVIYE', 'ADET']

    # DataFrame'i JavaScript formatına dönüştür
    chart_data = grouped_data.to_dict(orient='records')

    # chart_data'yı JSON formatında stringe çevir
    chart_data_json = json.dumps(chart_data)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
        am4core.ready(function() {{

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart3D);

        // Add data
        chart.data = {chart_data_json};

        // Create axes
        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "CIKIS SEVIYE";
        categoryAxis.renderer.labels.template.rotation = 0;
        categoryAxis.renderer.labels.template.hideOversized = false;
        categoryAxis.renderer.minGridDistance = 20;
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.tooltip.label.rotation = 270;
        categoryAxis.tooltip.label.horizontalCenter = "right";
        categoryAxis.tooltip.label.verticalCenter = "middle";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "ADET";
        valueAxis.title.fontWeight = "bold";

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries3D());
        series.dataFields.valueY = "ADET";
        series.dataFields.categoryX = "CIKIS SEVIYE";
        series.name = "Adet";
        series.tooltipText = "{{categoryX}}: [bold]{{valueY}}[/]";
        series.columns.template.fillOpacity = .8;

        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        columnTemplate.stroke = am4core.color("#FFFFFF");

        columnTemplate.adapter.add("fill", function(fill, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        columnTemplate.adapter.add("stroke", function(stroke, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        // Add labels on columns
        var labelBullet = series.bullets.push(new am4charts.LabelBullet());
        labelBullet.label.text = "{{valueY}}";
        labelBullet.label.dy = -10;
        labelBullet.label.hideOversized = false;
        labelBullet.label.truncate = false;

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.lineX.strokeOpacity = 0;
        chart.cursor.lineY.strokeOpacity = 0;

        }}); // end am4core.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

    st.write("---------------------------------------------------------------------------------")



     ######################################################################################################################
    ######################################################################################################################
    ############################### MARKA BAZLI DAĞILIM VE ADETLERİ
    ############################### OPPO

    st.title("OPPO")


    # Marka bazında gruplama
    grouped_data = df[df["MARKA"] == "OPPO"]["CIKIS SEVIYE"].value_counts().reset_index()
    grouped_data.columns = ['CIKIS SEVIYE', 'ADET']

    # DataFrame'i JavaScript formatına dönüştür
    chart_data = grouped_data.to_dict(orient='records')

    # chart_data'yı JSON formatında stringe çevir
    chart_data_json = json.dumps(chart_data)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
        am4core.ready(function() {{

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart3D);

        // Add data
        chart.data = {chart_data_json};

        // Create axes
        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "CIKIS SEVIYE";
        categoryAxis.renderer.labels.template.rotation = 0;
        categoryAxis.renderer.labels.template.hideOversized = false;
        categoryAxis.renderer.minGridDistance = 20;
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.tooltip.label.rotation = 270;
        categoryAxis.tooltip.label.horizontalCenter = "right";
        categoryAxis.tooltip.label.verticalCenter = "middle";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "ADET";
        valueAxis.title.fontWeight = "bold";

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries3D());
        series.dataFields.valueY = "ADET";
        series.dataFields.categoryX = "CIKIS SEVIYE";
        series.name = "Adet";
        series.tooltipText = "{{categoryX}}: [bold]{{valueY}}[/]";
        series.columns.template.fillOpacity = .8;

        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        columnTemplate.stroke = am4core.color("#FFFFFF");

        columnTemplate.adapter.add("fill", function(fill, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        columnTemplate.adapter.add("stroke", function(stroke, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        // Add labels on columns
        var labelBullet = series.bullets.push(new am4charts.LabelBullet());
        labelBullet.label.text = "{{valueY}}";
        labelBullet.label.dy = -10;
        labelBullet.label.hideOversized = false;
        labelBullet.label.truncate = false;

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.lineX.strokeOpacity = 0;
        chart.cursor.lineY.strokeOpacity = 0;

        }}); // end am4core.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

    st.write("---------------------------------------------------------------------------------")



    ######################################################################################################################
    ######################################################################################################################
    ############################### MARKA BAZLI DAĞILIM VE ADETLERİ
    ############################### HUAWEI

    st.title("HUAWEI")


    # Marka bazında gruplama
    grouped_data = df[df["MARKA"] == "HUAWEI"]["CIKIS SEVIYE"].value_counts().reset_index()
    grouped_data.columns = ['CIKIS SEVIYE', 'ADET']

    # DataFrame'i JavaScript formatına dönüştür
    chart_data = grouped_data.to_dict(orient='records')

    # chart_data'yı JSON formatında stringe çevir
    chart_data_json = json.dumps(chart_data)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
        am4core.ready(function() {{

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart3D);

        // Add data
        chart.data = {chart_data_json};

        // Create axes
        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "CIKIS SEVIYE";
        categoryAxis.renderer.labels.template.rotation = 0;
        categoryAxis.renderer.labels.template.hideOversized = false;
        categoryAxis.renderer.minGridDistance = 20;
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.tooltip.label.rotation = 270;
        categoryAxis.tooltip.label.horizontalCenter = "right";
        categoryAxis.tooltip.label.verticalCenter = "middle";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "ADET";
        valueAxis.title.fontWeight = "bold";

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries3D());
        series.dataFields.valueY = "ADET";
        series.dataFields.categoryX = "CIKIS SEVIYE";
        series.name = "Adet";
        series.tooltipText = "{{categoryX}}: [bold]{{valueY}}[/]";
        series.columns.template.fillOpacity = .8;

        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        columnTemplate.stroke = am4core.color("#FFFFFF");

        columnTemplate.adapter.add("fill", function(fill, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        columnTemplate.adapter.add("stroke", function(stroke, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        // Add labels on columns
        var labelBullet = series.bullets.push(new am4charts.LabelBullet());
        labelBullet.label.text = "{{valueY}}";
        labelBullet.label.dy = -10;
        labelBullet.label.hideOversized = false;
        labelBullet.label.truncate = false;

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.lineX.strokeOpacity = 0;
        chart.cursor.lineY.strokeOpacity = 0;

        }}); // end am4core.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

    st.write("---------------------------------------------------------------------------------")



    ######################################################################################################################
    ######################################################################################################################
    ############################### MODEL BAZLI DAĞILIMLAR
    ############################### APPLE
    ############################### İPHONE 14

    st.title("APPLE")
    st.title("Iphone 14")

    def plot_cat_summary_amcharts(dataframe, col_name, model_filter=None):
        # Model filtresi uygulanması
        if model_filter:
            filtered_df = dataframe[dataframe['MODEL'].str.contains(model_filter, case=False)]
        else:
            filtered_df = dataframe

        # Kategorik değerlerin adet ve yüzde oranlarını hesaplayalım ve en çok satandan en aza doğru sıralayalım
        value_counts = filtered_df[col_name].value_counts().head(15).sort_values(ascending=False)
        total_count = len(filtered_df)
        percentages = (value_counts / total_count) * 100

        # Veriyi AMCharts için uygun bir formata dönüştür
        data = [{'MODEL': category, 'ADET': count, 'percentage': percent} for category, count, percent in zip(value_counts.index, value_counts, percentages)]
        chart_data_json = json.dumps(data, ensure_ascii=False)

        return chart_data_json

    chart_data_json = plot_cat_summary_amcharts(df, "MODEL", model_filter="IPHONE 14")
    print(chart_data_json)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/4/core.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/charts.js"></script>
    <script src="https://cdn.amcharts.com/lib/4/themes/animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
        am4core.ready(function() {{

        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end

        // Create chart instance
        var chart = am4core.create("chartdiv", am4charts.XYChart3D);

        // Add data
        chart.data = {chart_data_json};

        // Create axes
        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "MODEL";
        categoryAxis.renderer.labels.template.rotation = 270;
        categoryAxis.renderer.labels.template.fontSize = 15;  // Yazı tipi boyutunu küçült
        categoryAxis.renderer.labels.template.hideOversized = false;
        categoryAxis.renderer.minGridDistance = 25;  // Barlar arasındaki mesafeyi artır
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.tooltip.label.rotation = 270;
        categoryAxis.tooltip.label.horizontalCenter = "right";
        categoryAxis.tooltip.label.verticalCenter = "middle";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "ADET";
        valueAxis.title.fontWeight = "bold";

        // Create series
        var series = chart.series.push(new am4charts.ColumnSeries3D());
        series.dataFields.valueY = "ADET";
        series.dataFields.categoryX = "MODEL";
        series.name = "Adet";
        series.tooltipText = "{{categoryX}}: [bold]{{valueY}}[/]";
        series.columns.template.fillOpacity = .8;

        var columnTemplate = series.columns.template;
        columnTemplate.strokeWidth = 2;
        columnTemplate.strokeOpacity = 1;
        columnTemplate.stroke = am4core.color("#FFFFFF");

        columnTemplate.adapter.add("fill", function(fill, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        columnTemplate.adapter.add("stroke", function(stroke, target) {{
            return chart.colors.getIndex(target.dataItem.index);
        }});

        // Add labels on columns
        var labelBullet = series.bullets.push(new am4charts.LabelBullet());
        labelBullet.label.text = "{{valueY}}";
        labelBullet.label.dy = -10;
        labelBullet.label.hideOversized = false;
        labelBullet.label.truncate = false;

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.lineX.strokeOpacity = 0;
        chart.cursor.lineY.strokeOpacity = 0;

        }}); // end am4core.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

    st.write("---------------------------------------------------------------------------------")

    ############################### İPHONE 14 ÇOKLU GRAFİK

    # Veri işleme fonksiyonları
    def marka_model_sayisi(df, marka=None):
        if not marka:
            model_sayilari = df['MODEL'].value_counts().to_dict()
        else:
            marka_filtresi = df['MODEL'].str.contains(marka, case=False)
            model_sayilari = df[marka_filtresi]['MODEL'].value_counts().to_dict()
        return model_sayilari

    def marka_grade_sayisi(df, marka=None):
        if not marka:
            grade_sayilari = df.groupby(['MODEL', 'CIKIS SEVIYE']).size().reset_index(name='COUNT')
        else:
            marka_filtresi = df['MODEL'].str.contains(marka, case=False)
            grade_sayilari = df[marka_filtresi].groupby(['MODEL', 'CIKIS SEVIYE']).size().reset_index(name='COUNT')
        return grade_sayilari

    # Kullanıcı tarafından seçilecek marka
    istenen_marka = 'İPHONE 14'

    # Filtrelenmiş verileri alalım
    filtrelenmis_modeller_sayilari = marka_model_sayisi(df, istenen_marka)
    filtrelenmis_grade_sayilari = marka_grade_sayisi(df, istenen_marka)

    print(f"\n{istenen_marka} Marka-Grade Listesi:")
    print(filtrelenmis_grade_sayilari)

    # Veriyi amCharts için uygun formata dönüştürme
    # Filtrelenmiş grade sayılarını alalım
    chart_data = [
        {"model": model, "grade": grade, "count": count}
        for model, grade, count in zip(filtrelenmis_grade_sayilari['MODEL'], filtrelenmis_grade_sayilari['CIKIS SEVIYE'], filtrelenmis_grade_sayilari['COUNT'])
    ]

    chart_data_json = json.dumps(chart_data, ensure_ascii=False)

    # amCharts grafiği için HTML ve JavaScript kodu
    amchart_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.amcharts.com/lib/5/index.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/xy.js"></script>
    <script src="https://cdn.amcharts.com/lib/5/themes/Animated.js"></script>
    <style>
        #chartdiv {{
        width: 100%;
        height: 500px;
        font-family: 'Roboto', sans-serif;
        }}
    </style>
    </head>
    <body>
    <div id="chartdiv"></div>
    <script>
    am5.ready(function() {{

    // Create root element
    var root = am5.Root.new("chartdiv");

    // Set themes
    root.setThemes([am5themes_Animated.new(root)]);

    // Create chart
    var chart = root.container.children.push(am5xy.XYChart.new(root, {{
    panX: false,
    panY: false,
    paddingLeft: 0,
    wheelX: "panX",
    wheelY: "zoomX",
    layout: root.verticalLayout
    }}));

    // Add legend
    var legend = chart.children.push(am5.Legend.new(root, {{
    centerX: am5.p50,
    x: am5.p50
    }}));

    // Chart data
    var data = {chart_data_json};

    // Create axes
    var xRenderer = am5xy.AxisRendererX.new(root, {{
    cellStartLocation: 0.1,
    cellEndLocation: 0.9,
    minorGridEnabled: true,
    orientation: "horizontal"
    }});
    var xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {{
    categoryField: "model",
    renderer: xRenderer,
    tooltip: am5.Tooltip.new(root, {{}}),
    }}));
    xRenderer.grid.template.setAll({{ location: 1 }});
    xAxis.data.setAll(data);

    var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {{
    renderer: am5xy.AxisRendererY.new(root, {{
    strokeOpacity: 0.1
    }})
    }}));

    // Add series
    function makeSeries(name, fieldName) {{
    var series = chart.series.push(am5xy.ColumnSeries.new(root, {{
    name: name,
    xAxis: xAxis,
    yAxis: yAxis,
    valueYField: "count",
    categoryXField: "model"
    }}));

    series.columns.template.setAll({{
    tooltipText: "{{name}}, {{categoryX}}:{{valueY}}",
    width: am5.percent(90),
    tooltipY: 0,
    strokeOpacity: 0
    }});

    // Filter data for this series
    var seriesData = data.filter(function(item) {{
    return item.grade === name;
    }});

    series.data.setAll(seriesData);

    // Make stuff animate on load
    series.appear();

    series.bullets.push(function () {{
    return am5.Bullet.new(root, {{
    locationY: 0,
    sprite: am5.Label.new(root, {{
    text: "{{valueY}}",
    fill: root.interfaceColors.get("alternativeText"),
    centerY: 0,
    centerX: am5.p50,
    populateText: true
    }})
    }});
    }});

    legend.data.push(series);
    }}

    // Make sure to call makeSeries for each grade you have in your data
    makeSeries("A", "A");
    makeSeries("B", "B");
    makeSeries("C", "C");

    // Make stuff animate on load
    chart.appear(1000, 100);

    }}); // end am5.ready()
    </script>
    </body>
    </html>
    """

    # Streamlit bileşeni olarak HTML/JavaScript kodunu yerleştir
    components.html(amchart_code, height=600)

