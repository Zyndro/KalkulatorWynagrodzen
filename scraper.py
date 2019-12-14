from bs4 import BeautifulSoup
import requests
import re


def netto(brutto):
    brutto=str(brutto)
    with requests.Session() as c:
        table=[]
        url = "https://zarobki.pracuj.pl/kalkulator-wynagrodzen?Salary="+brutto+"&SalaryType=1"
        r = c.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html5lib')
            for table_data in soup.find_all('span', {'class': 'value smaller'}):
                table.append(table_data)

            netto=table[0]
            output = re.findall('\d+', str(netto))
            output1 = "".join(output)
        else:
            raise requests.HTTPError

    return(output1)



