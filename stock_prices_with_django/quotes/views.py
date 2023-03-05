from django.shortcuts import render, redirect
import requests, json, cryptocompare
from django.urls import reverse

from .forms import StockForm
from .models import Stock
from django.contrib import messages


# 1
# def homepage(request):
#     api_req = requests.get(
#         "https://api.iex.cloud/v1/data/core/quote/aapl?token=")
#     try:
#         api = json.loads(api_req.content)
#     except Exception as e:
#         api = 'error!!'
#     return render(request, 'homepage.html', {'api': api})


# 2
# def homepage(request):
#     try:
#         url = "https://graphql.bitquery.io"
#
#         payload = json.dumps({
#             "query": "{\n  ethereum(network: bsc) {\n    dexTrades(\n      "
#                      "options: {desc: [\"block.height\", \"tradeIndex\"], limit: 1}\n      "
#                      "exchangeName: {in: [\"Pancake\", \"Pancake v2\"]}\n      "
#                      "baseCurrency: {is: \"0x6679eB24F59dFe111864AEc72B443d1Da666B360\"}\n      "
#                      "quoteCurrency: {is: \"0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c\"}\n      "
#                      "date: {after: \"2021-04-28\"}\n    ) {\n      "
#                      "transaction {\n        hash\n      }\n      tradeIndex\n      "
#                      "smartContract {\n        address {\n          address\n        }\n        "
#                      "contractType\n        currency {\n          name\n        }\n      }\n      "
#                      "tradeIndex\n      date {\n        date\n      }\n      block {\n        "
#                      "height\n      }\n      buyAmount\n      buyAmountInUsd: buyAmount(in: USD)\n"
#                      "      buyCurrency {\n        symbol\n        address\n      }\n      "
#                      "sellAmount\n      sellAmountInUsd: sellAmount(in: USD)\n      "
#                      "sellCurrency {\n        symbol\n        address\n      }\n      "
#                      "sellAmountInUsd: sellAmount(in: USD)\n      tradeAmount(in: USD)\n      "
#                      "transaction {\n        gasValue\n        gasPrice\n        "
#                      "gas\n      }\n    }\n  }\n}\n",
#             "variables": "{}"
#         })
#         headers = {
#             'Content-Type': 'application/json',
#             'X-API-KEY': ''
#         }
#
#         response = requests.request("POST", url, headers=headers, data=payload)
#         return render(request, 'homepage.html', {'api': response})
#     except Exception as e:
#         # except:
#         response = 'error!!'
#         return render(request, 'homepage.html', {'api': response})

# 3
# def homepage(request):
#     try:
#         url = "https://graphql.bitquery.io"
#
#         payload = json.dumps({
#             "query": "{\n  ethereum(network: bsc) {\n    dexTrades(\n      baseCurrency: {is: \"0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82\"}\n      quoteCurrency: {is: \"0x55d398326f99059ff775485246999027b3197955\"}\n      options: {desc: [\"block.height\", \"transaction.index\"], limit: 1}\n    ) {\n      block {\n        height\n        timestamp {\n          time(format: \"%Y-%m-%d %H:%M:%S\")\n        }\n      }\n      transaction {\n        index\n      }\n      baseCurrency {\n        symbol\n      }\n      quoteCurrency {\n        symbol\n      }\n      quotePrice\n    }\n  }\n}\n",
#             "variables": "{}"
#         })
#         headers = {
#             'Content-Type': 'application/json',
#             'X-API-KEY': ''
#         }
#
#         response = requests.request("POST", url, headers=headers, data=payload)
#
#         api = json.loads(response.content)
#         api = api['data']['ethereum']['dexTrades'][0]
#
#         resp = api
#         return render(request, 'homepage.html', {'api': resp})
#     except Exception as e:
#         # except:
#         response = 'error!!'
#         return render(request, 'homepage.html', {'api': response})
# --- html code
# {{api}}
# < hr >
# {{api.baseCurrency.symbol}}
# < hr >
# {{api.quotePrice}}

# 4

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


# print(data["RAW"]["ETH"]["USD"]["PRICE"])
# print(data["RAW"]["ETH"]["USD"]['HIGHDAY'])
# print(data["RAW"]["ETH"]["USD"]['LOWDAY'])
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


def about(request):
    return render(request, 'about.html', {})


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
    # stock = Stock.objects.get(name=stock_symbol.lower())
    stock = Stock.objects.filter(name=stock_symbol.lower()).first()
    if stock is None:
        upper_stock = Stock.objects.filter(name=stock_symbol.upper()).first()
        upper_stock.delete()
    else:
        stock.delete()
    messages.success(request, 'the stock deleted successfully')
    return redirect(reverse('stock_page'))
