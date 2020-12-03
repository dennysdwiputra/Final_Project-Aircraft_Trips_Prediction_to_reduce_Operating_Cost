# Flask : library utama untuk membuat API
# render_template : agar dapat memberikan respon file html
# request : untuk membaca data yang diterima saat request datang
from flask import Flask, render_template, request
# plotly dan plotly.graph_objs : membuat plot
import plotly
import plotly.graph_objs as go
# pandas : untuk membaca csv dan men-generate dataframe
import pandas as pd
import json
from sqlalchemy import create_engine

## Joblib untuk Load Model
import joblib

# untuk membuat route
app = Flask(__name__)

###################
## CATEGORY PLOT ##
###################

## IMPORT DATA USING pd.read_csv
# tips = pd.read_csv('./static/tips.csv')

# IMPORT DATA USING pd.read_sql
# sqlengine = create_engine('mysql+pymysql://kal:s3cret123@127.0.0.1/flaskapp', pool_recycle=3605)
# dbConnection = sqlengine.connect()
# engine = sqlengine.raw_connection()
# cursor = engine.cursor()
# tips = pd.read_sql("select * from tips", dbConnection)

# category plot function
def category_plot(
    cat_plot = 'histplot',
    cat_x = 'sex', cat_y = 'total_bill',
    estimator = 'count', hue = 'smoker'):

    # generate dataframe tips.csv
    # tips = pd.read_csv('./static/tips.csv')



    # jika menu yang dipilih adalah histogram
    if cat_plot == 'histplot':
        # siapkan list kosong untuk menampung konfigurasi hist
        data = []
        # generate config histogram dengan mengatur sumbu x dan sumbu y
        for val in tips[hue].unique():
            hist = go.Histogram(
                x=tips[tips[hue]==val][cat_x],
                y=tips[tips[hue]==val][cat_y],
                histfunc=estimator,
                name=val
            )
            #masukkan ke dalam array
            data.append(hist)
        #tentukan title dari plot yang akan ditampilkan
        title='Histogram'
    elif cat_plot == 'boxplot':
        data = []

        for val in tips[hue].unique():
            box = go.Box(
                x=tips[tips[hue] == val][cat_x], #series
                y=tips[tips[hue] == val][cat_y],
                name = val
            )
            data.append(box)
        title='Box'
    # menyiapkan config layout tempat plot akan ditampilkan
    # menentukan nama sumbu x dan sumbu y
    if cat_plot == 'histplot':
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title='person'),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    else:
        layout = go.Layout(
            title=title,
            xaxis=dict(title=cat_x),
            yaxis=dict(title=cat_y),
            # boxmode group digunakan berfungsi untuk mengelompokkan box berdasarkan hue
            boxmode = 'group'
        )
    #simpan config plot dan layout pada dictionary
    result = {'data': data, 'layout': layout}

    #json.dumps akan mengenerate plot dan menyimpan hasilnya pada graphjson
    graphJSON = json.dumps(result, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

# akses halaman menuju route '/' untuk men-test
# apakah API sudah running atau belum
@app.route('/')
def index():

    plot = category_plot()
    # dropdown menu
    # kita lihat pada halaman dashboard terdapat menu dropdown
    # terdapat lima menu dropdown, sehingga kita mengirimkan kelima variable di bawah ini
    # kita mengirimnya dalam bentuk list agar mudah mengolahnya di halaman html menggunakan looping
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('sex', 'Sex'), ('smoker', 'Smoker'), ('day', 'Day'), ('time', 'Time')]
    list_y = [('total_bill', 'Bill'), ('tip', 'Tip'), ('size', 'Size')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('sex', 'Sex'), ('smoker', 'Smoker'), ('day', 'Day'), ('time', 'Time')]

    return render_template(
        # file yang akan menjadi response dari API
        'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot='histplot',
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x='sex',

        # untuk sumbu Y tidak ada, nantinya menu dropdown Y akan di disable
        # karena pada histogram, sumbu Y akan menunjukkan kuantitas data

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator='count',
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue='smoker',
        # list yang akan digunakan looping untuk membuat dropdown 'Jenis Plot'
        drop_plot= list_plot,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu X'
        drop_x= list_x,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu Y'
        drop_y= list_y,
        # list yang akan digunakan looping untuk membuat dropdown 'Estimator'
        drop_estimator= list_est,
        # list yang akan digunakan looping untuk membuat dropdown 'Hue'
        drop_hue= list_hue)

# ada dua kondisi di mana kita akan melakukan request terhadap route ini
# pertama saat klik menu tab (Histogram & Box)
# kedua saat mengirim form (saat merubah salah satu dropdown) 
@app.route('/cat_fn/<nav>')
def cat_fn(nav):

    # saat klik menu navigasi
    if nav == 'True':
        cat_plot = 'histplot'
        cat_x = 'sex'
        cat_y = 'total_bill'
        estimator = 'count'
        hue = 'smoker'
    
    # saat memilih value dari form
    else:
        cat_plot = request.args.get('cat_plot')
        cat_x = request.args.get('cat_x')
        cat_y = request.args.get('cat_y')
        estimator = request.args.get('estimator')
        hue = request.args.get('hue')

    # Dari boxplot ke histogram akan None
    if estimator == None:
        estimator = 'count'
    
    # Saat estimator == 'count', dropdown menu sumbu Y menjadi disabled dan memberikan nilai None
    if cat_y == None:
        cat_y = 'total_bill'

    # Dropdown menu
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('sex', 'Sex'), ('smoker', 'Smoker'), ('day', 'Day'), ('time', 'Time')]
    list_y = [('total_bill', 'Bill'), ('tip', 'Tip'), ('size', 'Size')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('sex', 'Sex'), ('smoker', 'Smoker'), ('day', 'Day'), ('time', 'Time')]

    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)
    return render_template(
        # file yang akan menjadi response dari API
        'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot=cat_plot,
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x=cat_x,
        focus_y=cat_y,

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator=estimator,
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue=hue,
        # list yang akan digunakan looping untuk membuat dropdown 'Jenis Plot'
        drop_plot= list_plot,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu X'
        drop_x= list_x,
        # list yang akan digunakan looping untuk membuat dropdown 'Sumbu Y'
        drop_y= list_y,
        # list yang akan digunakan looping untuk membuat dropdown 'Estimator'
        drop_estimator= list_est,
        # list yang akan digunakan looping untuk membuat dropdown 'Hue'
        drop_hue= list_hue
    )

##################
## SCATTER PLOT ##
##################

# scatter plot function
def scatter_plot(cat_x, cat_y, hue):


    data = []

    for val in tips[hue].unique():
        scatt = go.Scatter(
            x = tips[tips[hue] == val][cat_x],
            y = tips[tips[hue] == val][cat_y],
            mode = 'markers',
            name = val
        )
        data.append(scatt)

    layout = go.Layout(
        title= 'Scatter',
        title_x= 0.5,
        xaxis=dict(title=cat_x),
        yaxis=dict(title=cat_y)
    )

    result = {"data": data, "layout": layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/scatt_fn')
def scatt_fn():
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')
    hue = request.args.get('hue')

    # WAJIB! default value ketika scatter pertama kali dipanggil
    if cat_x == None and cat_y == None and hue == None:
        cat_x = 'total_bill'
        cat_y = 'tip'
        hue = 'sex'

    # Dropdown menu
    list_x = [('total_bill', 'Bill'), ('tip', 'Tip'), ('size', 'Size')]
    list_y = [('total_bill', 'Bill'), ('tip', 'Tip'), ('size', 'Size')]
    list_hue = [('sex', 'Sex'), ('smoker', 'Smoker'), ('day', 'Daytime'), ('time', 'Time')]

    plot = scatter_plot(cat_x, cat_y, hue)

    return render_template(
        'scatter.html',
        plot=plot,
        focus_x=cat_x,
        focus_y=cat_y,
        focus_hue=hue,
        drop_x= list_x,
        drop_y= list_y,
        drop_hue= list_hue
    )

##############
## PIE PLOT ##
##############

def pie_plot(hue = 'sex'):
    


    vcounts = tips[hue].value_counts()

    labels = []
    values = []

    for item in vcounts.iteritems():
        labels.append(item[0])
        values.append(item[1])
    
    data = [
        go.Pie(
            labels=labels,
            values=values
        )
    ]

    layout = go.Layout(title='Pie', title_x= 0.48)

    result = {'data': data, 'layout': layout}

    graphJSON = json.dumps(result,cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/pie_fn')
def pie_fn():
    hue = request.args.get('hue')

    if hue == None:
        hue = 'sex'

    list_hue = [('sex', 'Sex'), ('smoker', 'Smoker'), ('day', 'Day'), ('time', 'Time')]

    plot = pie_plot(hue)
    return render_template('pie.html', plot=plot, focus_hue=hue, drop_hue= list_hue)

###############
## UPDATE DB ##
###############
### Menampilkan data dari SQL
# @app.route('/db_fn')
# def db_fn():
#     sqlengine = create_engine('mysql+pymysql://kal:s3cret123@127.0.0.1/flaskapp', pool_recycle=3605)
#     engine = sqlengine.raw_connection()
#     cursor = engine.cursor()
#     cursor.execute("SELECT * FROM tips")
#     data = cursor.fetchall()
#     return render_template('update.html', data=data)

@app.route('/update_fn', methods=['POST', 'GET'])
def update_fn():

    if request.method == 'POST':
        input = request.form
        
        sex = ''
        if input['sex'] == 'male':
            sex = 'Male'
        else:
            sex = 'Female'

        smoker = ''
        if input['smoker'] == 'smoker_yes':
            smoker = 'Yes'
        else:
            smoker = 'No'

        day = ''
        if input['day'] == 'thur':
            day = 'Thur'
        elif input['day'] == 'fri':
            day = 'Fri'
        elif input['day'] == 'sat':
            day = 'Sat'
        else:
            day = 'Sun'

        time = ''
        if input['time'] == 'lunch':
            time = 'Lunch'
        else:
            time = 'Dinner'
        ## Memasukkan data ke Tabel SQL
        new_df = pd.DataFrame({
            'total_bill' : [float(input['bill'])],
            'tip' : [float(input['tip'])],
            'sex' : [sex],
            'smoker' : [smoker],
            'day' : [day],
            'time' : [time],
            'size' : [int(input['size'])]
        })
        new_df.to_sql('tips', con=dbConnection, if_exists='append', index=False)
        return render_template('success.html',
            total_bill=float(input['bill']),
            tip=float(input['tip']),
            sex=sex,
            smoker=smoker,
            day=day,
            time=time,
            size=int(input['size'])
            )


@app.route('/pred_lr')
## Menampilkan Dataset
def pred_lr():
    tips = pd.read_csv('train_2.csv')
    return render_template('predict.html', data=tips)

@app.route('/pred_result', methods=['POST', 'GET'])
def pred_result():

    if request.method == 'POST':
    ## Untuk Predict
        input = request.form
        
        sex = ''
        if input['sex'] == 'male':
            sex = 1
        else:
            sex = 0

        smoker = ''
        if input['smoker'] == 'smoker_yes':
            smoker = 1
        else:
            smoker = 0

        day = ''
        if input['day'] == 'thur':
            day = 3
        elif input['day'] == 'fri':
            day = 0
        elif input['day'] == 'sat':
            day = 1
        else:
            day = 2

        time = ''
        if input['time'] == 'lunch':
            time = 1
        else:
            time = 0
        bill=float(input['bill'])
        size = int(input['size'])

        pred = model.predict([[bill, sex, smoker, day, time, size]])[0].round(2)

        ## Untuk Isi Data
        sex_dt = ''
        if input['sex'] == 'male':
            sex_dt = 'Male'
        else:
            sex_dt = 'Female'

        smoker_dt = ''
        if input['smoker'] == 'smoker_yes':
            smoker_dt = 'Yes'
        else:
            smoker_dt = 'No'

        day_dt = ''
        if input['day'] == 'thur':
            day_dt = 'Thur'
        elif input['day'] == 'fri':
            day_dt = 'Fri'
        elif input['day'] == 'sat':
            day_dt = 'Sat'
        else:
            day_dt = 'Sun'

        time_dt = ''
        if input['time'] == 'lunch':
            time_dt = 'Lunch'
        else:
            time_dt = 'Dinner'



        return render_template('result.html',
            total_bill=float(input['bill']),
            sex=sex_dt,
            smoker=smoker_dt,
            day=day_dt,
            time=time_dt,
            size=int(input['size']),
            tip_pred = pred
            )

if __name__ == '__main__':
    tips = pd.read_csv('train_2.csv')
    ## Load Model
    model = joblib.load('ModelAusAirline')
    app.run(debug=True)