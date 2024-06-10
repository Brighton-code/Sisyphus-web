import os
import json
from datetime import datetime
from dataclasses import dataclass

import pandas as pd
import numpy as np
from specification import pab, icc


from flask import Flask
from flask import render_template, url_for, redirect, request, jsonify
from flask_bootstrap import Bootstrap5

from sqlalchemy import desc, insert
from models import db, Artlev, Artpr2, Conditierecord, Preset

@dataclass
class Conditie:
	type: str
	korting: float


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')  # Secret key for https
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sisyphus.db" # ?Make env variable
bootstrap = Bootstrap5(app)

db.init_app(app)

with app.app_context():
	db.create_all()


@app.route('/', methods=['GET'])
def home():
	page = int(request.args.get('page', 1))
	limit = int(request.args.get('limit', 20))
	artikelnummer = request.args.get('artikelnummer', '')
	omschrijving = request.args.get('omschrijving', '')
	
	result_artlev = Artlev.query.filter(
		db.and_(
			Artlev.productcode_fabricant.contains(artikelnummer),
			Artlev.artikelomschrijving.contains(omschrijving)
		)
	).paginate(page=page, per_page=limit, max_per_page=100)
	

	date = datetime.now().strftime('%Y%m%d')
	data = []
	for artlev in result_artlev.items:
		artpr2 = Artpr2.query.filter(db.and_(Artpr2.artikelcode_leverancier == artlev.artikelcode_leverancier, Artpr2.ingangsdatum_prijsinformatie <= date)).order_by(desc(Artpr2.ingangsdatum_prijsinformatie)).first()
		conditie_artikelnummer = Conditie('artikelnummer', Conditierecord.query.filter(Conditierecord.artikelnummer == artlev.artikelcode_leverancier).first())
		conditie_kortinggroep = Conditie('kortinggroep', Conditierecord.query.filter(Conditierecord.kortinggroep == artlev.kortingsgroep).first())
		tmp = {
				'artikelcode_leverancier': artlev.artikelcode_leverancier,
				'productcode_fabricant': artlev.productcode_fabricant,
				'gtin': artlev.gtin,
				'code_verpakkingsvorm': artlev.code_verpakkingsvorm,
				'aantal_gebruikseenheden': artlev.aantal_gebruikseenheden,
				'artikelomschrijving': artlev.artikelomschrijving,
				'bruto_prijs': artpr2.bruto_prijs,
				'korting': [conditie_artikelnummer, conditie_kortinggroep],
				'gebruikseenheid': artlev.gebruikseenheid
		}
		data.append(tmp)

	return render_template('index.html', data=data, pagination=result_artlev, params=[artikelnummer, omschrijving])

@app.route('/download-table', methods=['GET'])
def download_table():
	return render_template('download_table.html')


@app.get('/v1/get-save')
def get_presets():
	name_list = []
	for p in Preset.query.all():
		name_list.append(p.__dict__['name'])

	return jsonify(
		name_list = name_list
	)


@app.get('/v1/get-save/<name>')
def get_saved(name):
	data = Preset.query.filter(Preset.name == name).first()
	artikelnummer_list = json.loads(data.artikelnummer_list)

	result_artlev = Artlev.query.filter(Artlev.artikelcode_leverancier.in_(artikelnummer_list)).all()

	date = datetime.now().strftime('%Y%m%d')
	return_data = []
	for artlev in result_artlev:
		artpr2 = Artpr2.query.filter(db.and_(Artpr2.artikelcode_leverancier == artlev.artikelcode_leverancier, Artpr2.ingangsdatum_prijsinformatie <= date)).order_by(desc(Artpr2.ingangsdatum_prijsinformatie)).first()
		conditie_artikelnummer = Conditie('artikelnummer', Conditierecord.query.filter(Conditierecord.artikelnummer == artlev.artikelcode_leverancier).first())
		conditie_kortinggroep = Conditie('kortinggroep', Conditierecord.query.filter(Conditierecord.kortinggroep == artlev.kortingsgroep).first())
		conditie_list = [conditie_artikelnummer, conditie_kortinggroep]

		for c in conditie_list:
			if c.korting != None:
				c.korting = c.korting.__dict__
				c.korting['_sa_instance_state'] = None
		

		tmp = {
				'artikelcode_leverancier': artlev.artikelcode_leverancier,
				'productcode_fabricant': artlev.productcode_fabricant,
				'gtin': artlev.gtin,
				'code_verpakkingsvorm': artlev.code_verpakkingsvorm,
				'aantal_gebruikseenheden': artlev.aantal_gebruikseenheden,
				'artikelomschrijving': artlev.artikelomschrijving,
				'bruto_prijs': artpr2.bruto_prijs,
				'korting': conditie_list,
				'gebruikseenheid': artlev.gebruikseenheid
		}
		return_data.append(tmp)

	return jsonify(
		name=name,
		artikelnummer_list=data.artikelnummer_list,
		data=return_data
	)


@app.post('/v1/create-save')
def create_save():
	data = request.json
	name = data['name']
	artikelcodes = json.dumps(data['artikelcodes'], separators=(',', ':'))
	preset = Preset(
		name=name,
		artikelnummer_list=artikelcodes
	)
	db.session.add(preset)
	db.session.commit()
	print(preset)
	return jsonify(respone = 200)


@app.delete('/v1/delete-save/<name>')
def delete_save(name):
	respone = Preset.query.filter(Preset.name == name).delete()
	db.session.commit()
	return jsonify(respone=respone)


if __name__ ==  '__main__':
	app.run(host="0.0.0.0", port=3000, debug=True)
