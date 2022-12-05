import time
import finnhub
import csv
from csv import writer
from csv import reader

TOKEN = ''
finnhub_client = finnhub.Client(api_key=TOKEN)


def getStocks():
    count = 0
    data = finnhub_client.earnings_calendar(_from="2021-07-26", to="2021-07-28", symbol="", international=False)
    count += 1
    with open('stocks.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Time', 'Date', 'Exchange', 'Name', 'Ticker', 'Mkt Cap'])
        for i in data['earningsCalendar']:
            if i['date'] == '2021-07-27' and i['revenueEstimate'] is not None:
                companydata = finnhub_client.company_profile2(symbol=i['symbol'])
                count += 1
                if companydata['exchange'] == 'NASDAQ NMS - GLOBAL MARKET' or companydata[
                    'exchange'] == 'NEW YORK STOCK EXCHANGE, INC.' or companydata['exchange'] == 'NYSE MKT LLC':
                    csvwriter.writerow([i['hour'], i['date'], companydata['exchange'], companydata['name'], i['symbol'],
                                        companydata['marketCapitalization'] * 1000])
            if count > 58:
                print("sleep time")
                time.sleep(61)
                count = 0
                print("wake time")
    print("Excel Fully Populated")


def epsMath(a3, e3, a4, e4):
    score = 0
    try:
        if a3 > e3:
            score += 0.5
        else:
            score -= 0.5
        if a4 > e4:
            score += 0.5
        else:
            score -= 0.5
    except:
        return "N/A"
    return score


def earningsReview():
    count = 0
    with open('stocks.csv', 'r') as read_obj, \
            open('result.csv', 'w', newline='') as write_obj:
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)
        for row in csv_reader:
            if row[4] == 'Ticker':
                row.append('EPS')
                csv_writer.writerow(row)
                continue
            epsdata = finnhub_client.company_earnings(row[4])
            count += 1
            eps = []
            for i in epsdata:
                eps.append(i['actual'])
                eps.append(i['estimate'])
            row.append(str(epsMath(eps[4], eps[5], eps[6], eps[7])))
            csv_writer.writerow(row)
            if count > 58:
                print("sleep time")
                time.sleep(61)
                count = 0
                print("wake time")
    print("Excel Fully Calculated")


if __name__ == '__main__':
    earningsReview()