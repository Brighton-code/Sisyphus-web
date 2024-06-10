import pandas as pd
import numpy as np
from specification import pab, icc


	Artlev.__table__.drop(db.engine)
	Artlev.__table__.create(db.engine)
	file = './data/artlev.txt'
	spec_dict = pab.get('artlev')

	widths, names, types = [], [], []
	for row in spec_dict:
		widths.append(int(row.get('width')))
		names.append(row.get('name'))
		types.append(row.get('type'))

	df = pd.read_fwf(file, widths=widths, names=names, encoding='latin-1', dtype=str)

	df.replace({np.nan: None}, inplace=True)

	for row in spec_dict:
		name = row.get('name')
		type = row.get('type')
		if type == 'int':
			df[name] = df[name].astype('Int64')
		elif type == 'str':
			df[name] = df[name].astype(str).replace('None', np.nan)
		elif type == 'float':
			df[name] = df[name].astype(float)


	insert_df: pd.DataFrame = df[['Artikelcode leverancier','Productcode fabrikant','GTIN','Code verpakkingsvorm','Aantal gebruikseenheden','Artikelomschrijving','Gebruikseenheid','Kortingsgroep']].copy()
	insert_df.to_sql(Artlev.__tablename__, db.engine, if_exists='append', index=True, index_label='id')



# 
	Artpr2.__table__.drop(db.engine)
	Artpr2.__table__.create(db.engine)

	file = './data/ArtPr2.txt'
	spec_dict = pab.get('artpr2')

	widths, names, types = [], [], []
	for row in spec_dict:
		widths.append(int(row.get('width')))
		names.append(row.get('name'))
		types.append(row.get('type'))

	df = pd.read_fwf(file, widths=widths, names=names, encoding='latin-1', dtype=str)

	df.replace({np.nan: None}, inplace=True)

	for row in spec_dict:
		name = row.get('name')
		type = row.get('type')
		if type == 'int':
			df[name] = df[name].astype('Int64')
		elif type == 'str':
			df[name] = df[name].astype(str).replace('None', np.nan)
		elif type == 'float':
			df[name] = df[name].astype(float)


	insert_df: pd.DataFrame = df[['Artikelcode leverancier', 'Ingangsdatum prijsinformatie', 'Bruto prijs']].copy()
	insert_df.to_sql(Artpr2.__tablename__, db.engine, if_exists='append', index=True, index_label='id')

#
	Conditierecord.__table__.drop(db.engine)
	Conditierecord.__table__.create(db.engine)

	file = './data/condities.txt'
	spec_dict = icc.get('conditierecord')

	widths, names, types = [], [], []
	for row in spec_dict:
		widths.append(int(row.get('width')))
		names.append(row.get('name'))
		types.append(row.get('type'))

	df = pd.read_fwf(file, widths=widths, names=names, encoding='latin-1', dtype=str, skiprows=1)

	df.replace({np.nan: None}, inplace=True)

	df['Korting 1'] = df['Korting'].astype('Int64')
	df['Korting 2'] = df['Korting 2'].astype('Int64')
	df['Korting 3'] = df['Korting 3'].astype('Int64')
	df['Netto prijs'] = df['Netto prijs'].astype('Int64')


	insert_df: pd.DataFrame = df[['Artikelnummer', 'Kortinggroep', 'Korting', 'Ingangsdatum', 'Einddatum']].copy()
	insert_df.to_sql(Conditierecord.__tablename__, db.engine, if_exists='append', index=True, index_label='id')