# AnbimAPI

Pega informações dos índices IMA e IDA da Anbima através de uma API
mais concisa e clara.

## Como usar?

Para usar a biblioteca é simples, basta você instala-la com o pip através
do comando `pip install anbimapi` e depois usa-la conforme descrito abaixo


```python
# Estes são os indices disponiveis de cada uma das classes
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
```


```python
>>> from datetime import datetime
>>> from anbimapi import get_ima_index, get_ida_index
>>> df = get_ima_index("IMA-B"")
>>> print(df)
           date    index
0    2017-06-16     5147
1    2017-06-19  5162,88
2    2017-06-20   5143,1
3    2017-06-21  5148,09
4    2017-06-22  5137,19
...         ...      ...
1265 2022-08-01  8304,68
1266 2022-08-02  8283,99
1267 2022-08-03  8304,46
1268 2022-08-04  8407,35
1269 2022-08-05   8427,6

[1270 rows x 2 columns]
>>>
```