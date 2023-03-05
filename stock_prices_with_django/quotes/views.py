from django.shortcuts import render, redirect
import requests, json, cryptocompare
from django.urls import reverse

from .forms import StockForm
from .models import Stock
from django.contrib import messages


def test(request):
    try:
        data = cryptocompare.get_price('eth', currency='usd', full=True)
        # print(data["RAW"]["ETH"]["USD"]["PRICE"])
        # print(data["RAW"]["ETH"]["USD"]['HIGHDAY'])
        # print(data["RAW"]["ETH"]["USD"]['LOWDAY'])

        # -----2
        custom_url = 'https://data-api.cryptocompare.com/asset/v1/data/by/symbol?asset_symbol=BNB'
        currency_data = requests.get(custom_url).text
        # ------3

        url = 'https://min-api.cryptocompare.com/data/price?fsym={currency}&tsyms=USD'

        def get_price_usd(currency):
            resp = requests.get(url.format(currency=currency)).json()
            return (resp['USD'])

        return render(request, 'test_home_page.html', {
            'api': get_price_usd('bnb'),
            'data': data["RAW"]["ETH"]["USD"],
            'currency_data': currency_data
        })
    except Exception as e:
        # except:
        response = 'error!!'
        return render(request, 'test_home_page.html', {'api': response})


# main view
def homepage(request):
    if request.method == 'POST':
        try:
            stock_input = request.POST['stock-input']
            stock_input = stock_input.upper()
            data = cryptocompare.get_price(stock_input, currency='usd', full=True)

            return render(request, 'homepage.html', {
                'data': data["RAW"][stock_input]["USD"],
            })

        except Exception as e:
            response = 'error!!'
            return render(request, 'homepage.html', {'error': response})
    else:
        return render(request, 'homepage.html')


def stocks(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            is_there: bool = Stock.objects.filter(name=name).exists()
            if not is_there:
                form.save()
                messages.success(request, 'stock has been added')
                return redirect(reverse('stock_page'))
            else:
                messages.error(request, 'it was added before!! try another currency')
                return redirect(reverse('stock_page'))
        # else:
        #     return redirect(reverse('stock_page'))

    stock = Stock.objects.all()
    stock_items = []
    for item in stock:
        try:
            stock_input = str(item).upper()
            data = cryptocompare.get_price(stock_input, currency='usd', full=True)
            data = data["RAW"][stock_input]["USD"]
            stock_items.append(data)
        except Exception as e:
            data = 'error!!'
    form = StockForm()
    context = {
        'stocks': stock,
        'form': form,
        'stock_items': stock_items
    }
    return render(request, 'stock_page.html', context)


def delete_stock(request, stock_symbol):
    stock = Stock.objects.filter(name=stock_symbol.lower()).first()
    if stock is None:
        upper_stock = Stock.objects.filter(name=stock_symbol.upper()).first()
        upper_stock.delete()
    else:
        stock.delete()
    messages.success(request, 'the stock deleted successfully')
    return redirect(reverse('stock_page'))
