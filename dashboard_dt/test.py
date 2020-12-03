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




app = Flask(__name__)
airline = pd.read_csv('train_2.csv')
def category_plot(
    cat_plot = 'histplot',
    cat_x = 'Month_num', cat_y = 'ASKs',
    estimator = 'count', hue = 'City2'):


    # jika menu yang dipilih adalah histogram
    if cat_plot == 'histplot':
        # siapkan list kosong untuk menampung konfigurasi hist
        data = []
        # generate config histogram dengan mengatur sumbu x dan sumbu y
        for val in airline[hue].unique():
            hist = go.Histogram(
                x=airline[airline[hue]==val][cat_x],
                y=airline[airline[hue]==val][cat_y],
                histfunc=estimator,
                name=val
            )
            #masukkan ke dalam array
            data.append(hist)
        #tentukan title dari plot yang akan ditampilkan
        title='Bar Plot'
    elif cat_plot == 'boxplot':
        data = []

        for val in airline[hue].unique():
            box = go.Box(
                x=airline[airline[hue] == val][cat_x], #series
                y=airline[airline[hue] == val][cat_y],
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
            yaxis=dict(title='tes'),
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/category')
def index():
    plot = category_plot()
    # dropdown menu
    # kita lihat pada halaman dashboard terdapat menu dropdown
    # terdapat lima menu dropdown, sehingga kita mengirimkan kelima variable di bawah ini
    # kita mengirimnya dalam bentuk list agar mudah mengolahnya di halaman html menggunakan looping
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('Month_num', 'Month'), ('City2', 'Destination')]
    list_y = [('ASKs', 'Available Seat Kilometers'),('Aircraft_Trips','Aircraft Trips'),('Passenger_Trips','Passenger'),('est_daily_TOC','Daily Operational Cost'),('load_factor','Load Factor')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('City2', 'Destination')]

    return render_template(
        # file yang akan menjadi response dari API
        'category.html',
        # plot yang akan ditampilkan
        plot=plot,
        # menu yang akan tampil di dropdown 'Jenis Plot'
        focus_plot='histplot',
        # menu yang akan muncul di dropdown 'sumbu X'
        focus_x='Month_num',

        # untuk sumbu Y tidak ada, nantinya menu dropdown Y akan di disable
        # karena pada histogram, sumbu Y akan menunjukkan kuantitas data

        # menu yang akan muncul di dropdown 'Estimator'
        focus_estimator='count',
        # menu yang akan tampil di dropdown 'Hue'
        focus_hue='City2',
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
        cat_x = 'Month_num'
        cat_y = 'ASKs'
        estimator = 'count'
        hue = 'City2'
    
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
        cat_y = 'ASKs'

    # Dropdown menu
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('Month_num', 'Month'), ('City2', 'Destination')]
    list_y = [('ASKs', 'Available Seat Kilometers'),('Aircraft_Trips','Aircraft Trips'),('Passenger_Trips','Passenger'),('est_daily_TOC','Daily Operational Cost'),('load_factor','Load Factor')]
    list_est = [('count', 'Count'), ('avg', 'Average'), ('max', 'Max'), ('min', 'Min')]
    list_hue = [('City2', 'Destination')]

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

@app.route('/pred_lr')
## Menampilkan Dataset
def pred_lr():
    tips = pd.read_csv('train_2.csv')
    return render_template('predict.html', data=tips)


@app.route('/pred_result', methods=['POST', 'GET'])
def pred_result():
    df_cat = pd.read_csv('category.csv')
    ## Untuk Predict
    try:
        if request.method == 'POST':
            input = request.form
            city1 = str(input['city1'])
            city2 = str(input['city2'])
            month = int(input['month'])
            load_factor = int(input['load_factor'])
            seat = int(input['available_seat'])
            citypair = city1+city2
            citypair = citypair.upper()
            encode = df_cat[df_cat['city_pair_copy']==citypair].head(1)
            encode = encode.values.tolist()
            encode = encode[0][1:]
            encode[0:0] = [month,load_factor,seat]
        
            
            pred = (model.predict([encode])[0]).round()
            return render_template('result.html',
            route=f"{city1} - {city2}",
            month=month,
            load_factor=load_factor,
            av_seat=seat,
            tip_pred = pred
            )
            
    except :
        return render_template('result_error.html',
            route="Sorry, Your Route is not Available ",
            month=0,
            load_factor=0,
            av_seat=0,
            tip_pred = 0
            )
        

        

@app.route('/category')
def category():
    return render_template('category.html')

if __name__ == "__main__":
    tips = pd.read_csv('train_2.csv')
    ## Load Model
    model = joblib.load('ModelAusAirline')
    app.run(debug=True)
