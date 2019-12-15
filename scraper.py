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

#Przekazano formularz w niepoprawny sposób(nie mogę określic poprawnego sposobu)
'''
def netto1(brutto):
    headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
            }
    
    url = "https://wynagrodzenia.pl/kalkulator-wynagrodzen"
    url2 = "https://wynagrodzenia.pl/kalkulator-wynagrodzen/wyniki"
    table = []
    with requests.Session() as c:
        r = c.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        for table_data in soup.find_all('input', {'name': 'sedlak_calculator[_token]'}):
            table.append(str(table_data))
            m = re.findall('"(.*?)"', table[0])
            csrf = m[3]
            print(csrf)

    payload = {
                "sedlak_calculator[contractType]": "work",
                "sedlak_calculator[calculateWay]": "gross",
                "sedlak_calculator[earnings]": str(brutto),
                "sedlak_calculator[year]": "2019",
                "sedlak_calculator[mandateModels]": "otherCompany",
                "sedlak_calculator[theSameCity]": "1",
                "sedlak_calculator[freeCost]": "1",
                "sedlak_calculator[constantEarnings]": "1",
                "work_end26Year": "on",
                "sedlak_calculator[monthlyEarnings][0]": str(brutto),
                "sedlak_calculator[monthlyEarnings][1]": str(brutto),
                "sedlak_calculator[monthlyEarnings][2]": str(brutto),
                "sedlak_calculator[monthlyEarnings][3]": str(brutto),
                "sedlak_calculator[monthlyEarnings][4]": str(brutto),
                "sedlak_calculator[monthlyEarnings][5]": str(brutto),
                "sedlak_calculator[monthlyEarnings][6]": str(brutto),
                "sedlak_calculator[monthlyEarnings][7]": str(brutto),
                "sedlak_calculator[monthlyEarnings][8]": str(brutto),
                "sedlak_calculator[monthlyEarnings][9]": str(brutto),
                "sedlak_calculator[monthlyEarnings][10]": str(brutto),
                "sedlak_calculator[monthlyEarnings][11]": str(brutto),
                "sedlak_calculator[selfEmployer]": "1",
                "sedlak_calculator[rentAndAnnuityCost]": "1",
                "sedlak_calculator[sicknesCost]": "1",
                "sedlak_calculator[healthCost]": "1",
                "sedlak_calculator[FPCost]": "1",
                "sedlak_calculator[FGSPCost]": "1",
                "mandate_end26Year": "on",
                "sedlak_calculator[accidentPercent]": "1.67",
                "sedlak_calculator[end26Year]": "1",
                "sedlak_calculator[employeePercent]": "2",
                "sedlak_calculator[employerPercent]": "1.5",
                "sedlak_calculator[octoberIncome]": "1",
                "sedlak_calculator[businessExpenses]": "0",
                "work_accidentPercent": "1.67",
                "nonwork_accidentPercent": "1.67",
                "sedlak_calculator[save]": "",
                "sedlak_calculator[_token]": str(csrf)
                }

    response = requests.post(url2, headers=headers, data=payload, allow_redirects=True)
    print(response.text)
    print(payload)
    with open("output1.html", "w") as file:
       file.write(response.text)

netto1(2550)

'''
