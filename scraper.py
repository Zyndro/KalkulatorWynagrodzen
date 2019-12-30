from bs4 import BeautifulSoup
import requests
import re

#get request
def netto(brutto,rodzaj):
    umowa=rodzaj
    brutto=str(brutto)
    with requests.Session() as c:
        table=[]
        url = "https://zarobki.pracuj.pl/kalkulator-wynagrodzen?Salary="+brutto+"&SalaryType=1"
        r = c.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html5lib')
            for table_data in soup.find_all('span', {'class': 'value smaller'}):
                table.append(table_data)

            if umowa == 1:
                netto=table[0]
            if umowa == 2:
                netto=table[1]
            if umowa == 3:
                netto=table[2]

            output = re.findall('\d+', str(netto))
            output1 = "".join(output)


        else:
            raise requests.HTTPError


    return(output1)

#post request
def netto1(brutto):
    headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
            }
    
    url = "https://wynagrodzenia.pl/kalkulator-wynagrodzen"
    url2 = "https://wynagrodzenia.pl/kalkulator-wynagrodzen/wyniki"
    table = []
    with requests.Session() as c:
        #csrf token dla requesta
        r = c.get(url, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html5lib')
            for table_data in soup.find_all('input', {'name': 'sedlak_calculator[_token]'}):
                table.append(str(table_data))
                m = re.findall('"(.*?)"', table[0])
            csrf = m[3]
            print(csrf)

            payload = {
                        "sedlak_calculator[contractType]": "work",
                        "sedlak_calculator[calculateWay]": "gross",
                        "sedlak_calculator[earnings]": brutto,
                        "sedlak_calculator[year]": "2019",
                        "sedlak_calculator[mandateModels]": "otherCompany1",
                        "sedlak_calculator[theSameCity]": "1",
                        "sedlak_calculator[freeCost]": "1",
                        "sedlak_calculator[constantEarnings]": "1",
                        "work_end26Year": "on",
                        "sedlak_calculator[monthlyEarnings][0]": brutto,
                        "sedlak_calculator[monthlyEarnings][1]": brutto,
                        "sedlak_calculator[monthlyEarnings][2]": brutto,
                        "sedlak_calculator[monthlyEarnings][3]": brutto,
                        "sedlak_calculator[monthlyEarnings][4]": brutto,
                        "sedlak_calculator[monthlyEarnings][5]": brutto,
                        "sedlak_calculator[monthlyEarnings][6]": brutto,
                        "sedlak_calculator[monthlyEarnings][7]": brutto,
                        "sedlak_calculator[monthlyEarnings][8]": brutto,
                        "sedlak_calculator[monthlyEarnings][9]": brutto,
                        "sedlak_calculator[monthlyEarnings][10]": brutto,
                        "sedlak_calculator[monthlyEarnings][11]": brutto,
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
                        "sedlak_calculator[_token]": csrf
                        }

            response = c.post(url2, data=payload, headers=headers)
            if response.status_code == 200:
                with open("output1.html", "w") as file:
                   file.write(response.text)
                table = []
                soup = BeautifulSoup(response.content, 'html5lib')
                for table_data in soup.find_all('div', {'class': 'col-md-3 col-sm-6'}):
                    table.append(table_data)
                output = re.findall('(?<=<span>)(.*)(?=</span>)', str(table[0]))
                output = output[0]
                output = "".join(output.split())
                output = output.replace(',', '.')
                output = re.findall('\d+', output)

            else:
                raise requests.HTTPError

        else:
            raise requests.HTTPError

        return (output[0])




#testy
if __name__ == "__main__":
    netto1(2550)
