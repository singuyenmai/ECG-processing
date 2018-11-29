# Link of Database
https://physionet.org/pn3/incartdb/

# Download summary of samples
`wget https://physionet.org/pn3/incartdb/files-patients-diagnoses.txt`

# Download record descriptions
`wget https://physionet.org/pn3/incartdb/record-descriptions.txt`

# Download data
```SHELL
address="https://physionet.org/pn3/incartdb"
for i in {1..9}; do \
	wget "$address"/I0"$i".dat;
	wget "$address"/I0"$i".hea;
	wget "$address"/I0"$i".atr;
done

for i in {10..75}; do \
	wget "$address"/I0"$i".dat;
	wget "$address"/I0"$i".hea;
	wget "$address"/I0"$i".atr;
done

wget https://physionet.org/pn3/incartdb/ANNOTATORS
wget https://physionet.org/pn3/incartdb/RECORDS
```

# Besides, [package `wfdb` from Physionet](https://github.com/MIT-LCP/wfdb-python) can be used. After installing the package, run this python script:
```python
import wfdb
database="incartdb"
print(wfdb.get_record_list(database))

wfdb.dl_database(database, '/home/singuyen/Study/biosignal/project/rawData')
```
