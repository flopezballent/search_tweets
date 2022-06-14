from django.shortcuts import redirect, render, HttpResponse
import twint
from .models import Search
from django.core.files import File
import os
import pandas as pd

# Create your views here.

def searchTweets(search_id):
    search = Search.objects.get(id=search_id)
    keywords = search.keywords
    initial_date = str(search.initial_date)
    final_date = str(search.final_date)

    columns = ['timezone']

    if search.date_col == 1:
        columns.append('date')
    if search.time_col == 1:
        columns.append('time')
    if search.username_col == 1:
        columns.append('username')
    if search.name_col == 1:
        columns.append('name')
    if search.tweet_col == 1:
        columns.append('tweet')
    if search.photos_col == 1:
        columns.append('photos')
    
    try:
        c = twint.Config()
        c.Since = initial_date
        c.Search = keywords
        c.Until = final_date
        c.Limit = 5
        c.Custom["tweet"] = columns
        c.Store_csv = True
        c.Pandas = True
        filename = keywords.replace(' ', '_')
        c.Output = f"App/exports/{filename}.csv"
        twint.run.Search(c)

        c = twint.Config()
        c.Since = initial_date
        c.Search = keywords
        c.Until = final_date
        c.Limit = 2
        c.Custom["tweet"] = columns
        c.Pandas = True
        twint.run.Search(c)

        Tweets_df = twint.storage.panda.Tweets_df

        return True, filename, Tweets_df
    
    except:
        print('no esta funcionando twint')
        return False, filename

def home(request):
    if request.method=='POST':
        newSearch = Search(keywords=request.POST.get('keywords'), 
                        initial_date=request.POST.get('initial_date'),
                        final_date=request.POST.get('final_date'),
                        date_col=request.POST.get('date_col'),
                        time_col=request.POST.get('time_col'),
                        username_col=request.POST.get('username_col'),
                        name_col=request.POST.get('name_col'),
                        tweet_col=request.POST.get('tweet_col'),
                        photos_col=request.POST.get('photos_col'))
        newSearch.save()
        return redirect('/export')
  
    return render(request, "App/index.html")

def export(request):
    search_id = Search.objects.latest('id').id
    export = searchTweets(search_id)
    filename, df = export[1], export[2]
    df = pd.DataFrame(df)
    if df.empty:
        return render(request, "App/error.html")
    df_html = df.to_html(f"App/templates/App/tabla.html", 
                            columns=['timezone', 'date', 'username', 'name', 'tweet'],
                            classes='table',
                            justify='left',
                            col_space='10rem',
                            index=False)
    if request.method=='POST':
        if export[0]:
            f = open(f"App/exports/{export[1]}.csv", 'r', encoding="utf8")
            file = File(f)
            response = HttpResponse(file, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={filename}.csv'
            print('Se exporto correctamente!')
            os.remove(f"App/exports/{filename}.csv")
            return response
        else:
            HttpResponse('No se encontraron resultados')
            #return redirect('/export/?error')
    context = {
        'df': df_html
    }
    return render(request, "App/export.html", context)
