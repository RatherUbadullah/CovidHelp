from os import truncate

from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import lxml.html as lh
import bs4

from DashboardCovid.models import topCountries, jkData


def dashboard(request):
    # Get data of Top 5 affected countries....
    page = requests.get("https://www.worldometers.info/coronavirus/")
    doc = lh.fromstring(page.content)
    # Country names
    tr_elements = doc.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr[*]/td[2]/a')
    cnames = []
    i = 1
    for n in tr_elements:
        if i == 6:
            break
        cnames.append(n.text)
        i+=1
    # Total cases...
    total_cases = doc.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr[*]/td[3]')
    total_cases = total_cases[8::]
    all_cases =[]
    j = 1
    for n in total_cases:
        if j == 6:
            break
        all_cases.append(n.text)
        j += 1
    #New cases...
    new_cases = doc.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr[*]/td[4]')
    new_cases = new_cases[8::]
    new_ones =[]
    j = 1
    for n in new_cases:
        if j == 6:
            break
        new_ones.append(n.text)
        j += 1
    #Recovered  cases...
    recover_cases = doc.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr[*]/td[7]')
    recover_cases = recover_cases[8::]
    recover_ones =[]
    j = 1
    for n in recover_cases:
        if j == 6:
            break
        recover_ones.append(n.text)
        j += 1
    #Total deaths...
    death_cases = doc.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr[*]/td[5]')
    death_cases = death_cases[8::]
    death_ones =[]
    j = 1
    for n in death_cases:
        if j == 6:
            break
        death_ones.append(n.text)
        j += 1
    # Integrating data in modal class..
    obgList = []
    i =0
    for cn in cnames:
        obj = topCountries()
        obj.countrynames  = cnames[i]
        obj.total_cases = all_cases[i]
        obj.new_cases = new_ones[i]
        obj.total_recovered = recover_ones[i]
        obj.total_deaths  = death_ones[i]
        obgList.append(obj)
        i += 1

    page = requests.get("https://coronaclusters.in/")
    doc = lh.fromstring(page.content)

    total = doc.xpath('//*[@id="state-data-table"]/tbody/tr[11]/td[1]')
    total = total[0].text

    newCases = doc.xpath('//*[@id="state-data-table"]/tbody/tr[11]/td[2]')
    newCases = newCases[0].text

    activeCases = doc.xpath('//*[@id="state-data-table"]/tbody/tr[11]/td[6]')
    activeCases = activeCases[0].text

    totalDeaths = doc.xpath('//*[@id="state-data-table"]/tbody/tr[11]/td[3]')
    totalDeaths = totalDeaths[0].text

    newDeaths = doc.xpath('//*[@id="state-data-table"]/tbody/tr[11]/td[4]')
    newDeaths = newDeaths[0].text

    recovered = doc.xpath('//*[@id="state-data-table"]/tbody/tr[11]/td[5]')
    recovered = recovered[0].text

    deathRate = int(totalDeaths)/int(total) * 100
    deathRate = round(deathRate, 3)

    lastUpdated = doc.xpath('//*[@id="state-data-table"]/tbody/tr[11]/td[7]')
    lastUpdated = lastUpdated[0].text

    jkDetails = jkData()
    jkDetails.total_cases = total
    jkDetails.new_cases = newCases
    jkDetails.active_cases = activeCases
    jkDetails.total_deaths = totalDeaths
    jkDetails.recovered_cases = recovered
    jkDetails.new_deaths = newDeaths
    jkDetails.death_rate = deathRate
    jkDetails.last_updated = lastUpdated


    return render(request, "dashboard.html", {'alldata': obgList, 'jkcases': jkDetails})

