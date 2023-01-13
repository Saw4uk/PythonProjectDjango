import requests
import pandas as pd
import json
from multiprocessing import Pool



class API_loader:
    @staticmethod
    def parse_response(hour):
        def get(dict, key):
            try:
                return dict.get(key)
            except:
                return None

        result_array = []
        for x in range(20):
            for i in range(5):
                res = requests.get(f'https://api.hh.ru/vacancies'
                                   f'?specialization=1'
                                   f'&per_page=100'
                                   f'&page={x}'
                                   f'&date_from=2022-12-26T{hour:02}:00:00'
                                   f'&date_to=2022-12-26T{hour + 1:02}:00:00')
                if res.status_code == 200:
                    print(x)
                    parsedJson = json.loads(res.text)["items"]
                    result_array.append(pd.DataFrame([{'name': get(item, 'name'),
                                                       'employer': get(get(item,'employer'),'name'),
                                                       'salary_from': get(get(item, 'salary'), 'from'),
                                                       'salary_to': get(get(item, 'salary'), 'to'),
                                                       'url': get(item, 'url'),
                                                       'salary_currency': get(get(item, 'salary'), 'currency'),
                                                       'area_name': get(get(item, 'area'), 'name'),
                                                       'description': '',
                                                       'skills': '',
                                                       'published_at': get(item, 'published_at')} for item in
                                                      parsedJson]))
                    break
        return pd.concat(result_array, ignore_index=True)

    @staticmethod
    def Load_API():
        final_dataframe_array = []
        data_to_async = range(23)
        with Pool(23) as p:
            x = p.map(API_loader.parse_response,data_to_async)
        for i in x:
            final_dataframe_array.append(i)
        newDf = pd.concat(final_dataframe_array, ignore_index=True).sort_values(by='published_at')
        newDf = newDf[newDf['name'].str.lower().str.contains('c#')]
        resultDf = pd.DataFrame(columns=newDf.keys())
        for _, vacancy in newDf.iterrows():
            url = requests.get(vacancy['url']).json()
            vacancy['description'] = url['description']
            vacancy['skills'] = ', '.join(skill['name'] for skill in url['key_skills'])
            vacancy['published_at'] = vacancy['published_at'][11:19]
            vacancy['salary_from'] = f"{vacancy['salary_from'] if 0/vacancy['salary_from'] == 0 else vacancy['salary_to'] if 0/vacancy['salary_to'] == 0 else 'Не указан' if (0 / (vacancy['salary_from']+vacancy['salary_to']/2)) != 0 else str(vacancy['salary_from']+vacancy['salary_to']/2)} {vacancy['salary_currency'] if vacancy['salary_currency'] is not None else ''}"
            resultDf.loc[len(resultDf.index)] = vacancy
        return API_loader.get_array_ov_vacs(resultDf)

    @staticmethod
    def get_array_ov_vacs(df):
        resutArray = []
        counter = 0
        for _,row in df.iterrows():
            counter += 1
            resutArray.append(row.to_dict())
            if counter == 10:
                return resutArray
        return resutArray
