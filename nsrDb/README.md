# Link of Database
https://physionet.org/pn3/nsrdb/

# To download the data, [package `wfdb` from Physionet](https://github.com/MIT-LCP/wfdb-python) can be used. After installing the package, run this python script:
```python
import wfdb
database="nsrdb"
print(wfdb.get_record_list(database))

wfdb.dl_database(database)
```
