from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Date
from sqlalchemy.types import ARRAY
from datetime import datetime

class Base(DeclarativeBase):
	pass

db = SQLAlchemy(model_class=Base)

class Artlev(db.Model):
	__tablename__ = "artlev"
	id: 							Mapped[int] 				= mapped_column('id', primary_key=True)
	artikelcode_leverancier: 		Mapped[str] 				= mapped_column('Artikelcode leverancier', unique=True)
	productcode_fabricant: 			Mapped[Optional[str]]		= mapped_column('Productcode fabrikant')
	gtin:							Mapped[Optional[str]]		= mapped_column('GTIN')
	code_verpakkingsvorm:			Mapped[Optional[str]]		= mapped_column('Code verpakkingsvorm')
	aantal_gebruikseenheden:		Mapped[Optional[float]]		= mapped_column('Aantal gebruikseenheden')
	artikelomschrijving:			Mapped[Optional[str]]		= mapped_column('Artikelomschrijving')
	gebruikseenheid:				Mapped[Optional[str]]		= mapped_column('Gebruikseenheid')
	kortingsgroep:					Mapped[Optional[str]]		= mapped_column('Kortingsgroep')

class Artpr2(db.Model):
	__tablename__ = "artpr2"
	id:								Mapped[int] 				= mapped_column('id', primary_key=True)
	artikelcode_leverancier:		Mapped[str]					= mapped_column('Artikelcode leverancier')
	ingangsdatum_prijsinformatie: 	Mapped[Optional[str]]		= mapped_column('Ingangsdatum prijsinformatie')
	bruto_prijs:					Mapped[Optional[float]]		= mapped_column('Bruto prijs')


class Conditierecord(db.Model):
	__tablename__ = 'conditierecord'
	id:								Mapped[int] 				= mapped_column('id', primary_key=True)
	artikelnummer:					Mapped[Optional[str]]		= mapped_column('Artikelnummer')
	kortinggroep:					Mapped[Optional[str]]		= mapped_column('Kortinggroep')
	korting:						Mapped[Optional[int]]		= mapped_column('Korting')
	ingangsdatum:					Mapped[Optional[str]]		= mapped_column('Ingangsdatum')
	einddatum:						Mapped[Optional[str]]		= mapped_column('Einddatum')


class Preset(db.Model):
	__tablename__ = 'preset'
	id:								Mapped[int] 					= mapped_column('id', primary_key=True)
	name:							Mapped[str] 					= mapped_column('Name', unique=True)
	artikelnummer_list:				Mapped[Optional[str]] 			= mapped_column('Artikelnummer List')