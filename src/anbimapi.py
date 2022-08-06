import datetime
import pandas as pd
import requests

class InvalidAnbimaDate(Exception):
    pass


class InvalidAnbimaIndexType(Exception):
    pass


class InvalidRequest(Exception):
    pass

INDEXES = ["ida", "ima"]
IMA_SUBINDEXES = [
    'IRF-M P2',
    'IMA-GERAL-EX-C',
    'IMA-GERAL',
    'IRF-M 1',
    'IMA-S',
    'IMA-B 5',
    'IRF-M',
    'IRF-M 1+',
    'IMA-B',
    'IMA-C',
    'IMA-B 5+',
    'IMA-B 5 P2'
]
IDA_SUBINDEXES = [
    'IDA-DI',
    'IDA-GERAL',
    'IDA-IPCA',
    'IDA-IPCA_EX_INFRAESTRUTURA',
    'IDA-IPCA_INFRAESTRUTURA'
]
AVAILABLE_SUBINDEXES = IDA_SUBINDEXES + IMA_SUBINDEXES

def get_index_base(index_type, index, start_date=None, end_date=None):
    if index_type not in INDEXES:
        raise InvalidAnbimaIndexType(
            "Por enquanto, só é suportado os indices das classes: " + ", ".join(INDEXES)
        )

    if start_date is not None and start_date < datetime.datetime(2017, 6, 16):
        raise InvalidAnbimaDate("Anbima suporta apenas datas depois de 16/06/2017")
    
    if end_date is not None and end_date > datetime.datetime.today():
        raise InvalidAnbimaDate(
            "Ainda não temos uma máquina de prever o futuro, escolha uma data menor que {}".format(
                datetime.datetime.today()
            )
        )
    
    if start_date is None:
        start_date = datetime.datetime(2017, 6, 16)
    
    if end_date is None:
        end_date = datetime.datetime.now()
    
    if index not in AVAILABLE_SUBINDEXES:
        raise InvalidAnbimaIndexType(
            "O Indices {} não está disponível, apenas os índices: {}".format(
                index,
                ", ".join(AVAILABLE_SUBINDEXES)
            )
        )

    url = "https://www.anbima.com.br/pt_br/anbima/json{}/acionar?dataInicio={}&dataFim={}".format(
        index_type,
        start_date.strftime("%d/%m/%Y"),
        end_date.strftime("%d/%m/%Y")
    )

    req  = requests.get(url)
    if req.status_code not in [200, 201]:
        raise InvalidRequest("Request retornou status: {}".format(req.status_code))
    
    return req.json()

def index_dataframe(index_json, index):
    df = pd.DataFrame(
        {
            "date": index_json["datas"],
            "index": index_json[index]["numero_indice"],
        }
    )
    df["date"] = df["date"].apply(lambda x: datetime.datetime.strptime(x, '%d/%m/%Y'))
    return df

def get_ima_index(index, start_date=None, end_date=None):
    if index not in IMA_SUBINDEXES:
        raise InvalidAnbimaIndexType(
            "Indice não pertence a classe IMA, indices pertencentes são: {}".format(
                IMA_SUBINDEXES
            )
        )
    
    df = index_dataframe(get_index_base("ima", index, start_date, end_date), index)
    return df

def get_ida_index(index, start_date=None, end_date=None):
    if index not in IDA_SUBINDEXES:
        raise InvalidAnbimaIndexType(
            "Indice não pertence a classe IDA, indices pertencentes são: {}".format(
                IDA_SUBINDEXES
            )
        )
    
    df = index_dataframe(get_index_base("ida", index, start_date, end_date), index)
    return df