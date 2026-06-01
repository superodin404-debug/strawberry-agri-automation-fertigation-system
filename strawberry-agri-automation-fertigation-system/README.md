{\rtf1\ansi\ansicpg936\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Strawberry Agri-Automation Fertigation System (SAAFS)\
# \uc0\u33609 \u33683 \u20892 \u19994 \u33258 \u21160 \u21270 \u37197 \u32933 \u31995 \u32479 \
\
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)\
\
### \uc0\u55357 \u56541  Overview / \u39033 \u30446 \u27010 \u36848 \
**EN:** Core calculation engine for strawberry open-field fertigation based on the SAAFS solid powder nutrient architecture. This project integrates agricultural plant physiology with modern software engineering to provide dynamic precision fertigation formulas based on first principles.\
\
**ZH:** \uc0\u22522 \u20110  SAAFS \u22266 \u20307 \u31881 \u26411 \u33829 \u20859 \u20307 \u31995 \u30340 \u33609 \u33683 \u25143 \u22806 \u20892 \u30000 \u20840 \u29983 \u21629 \u21608 \u26399 \u27700 \u32933 \u19968 \u20307 \u21270 \u35745 \u31639 \u26680 \u24515 \u24341 \u25806 \u12290 \u26412 \u39033 \u30446 \u23558 \u20892 \u19994 \u26893 \u29289 \u29983 \u29702 \u23398 \u19982 \u29616 \u20195 \u36719 \u20214 \u24037 \u31243 \u30456 \u32467 \u21512 \u65292 \u25552 \u20379 \u22522 \u20110 \u31532 \u19968 \u24615 \u21407 \u29702 \u30340 \u21160 \u24577 \u31934 \u20934 \u37197 \u32933 \u26041 \u26696 \u12290 \
\
---\
\
### \uc0\u55357 \u56960  Core Features / \u26680 \u24515 \u29305 \u24615 \
\
- **Dynamic Ratio Logic / \uc0\u21160 \u24577 \u37197 \u27604 \u36923 \u36753 **\
  - **EN:** Rejects rigid static recipes, supporting algorithmic seamless transitions across three major growth stages (Vegetative, Flowering, and Fruit Expansion).\
  - **ZH:** \uc0\u35299 \u32806 \u20256 \u32479 \u22266 \u23450 \u37197 \u26041 \u65292 \u25903 \u25345 \u19977 \u22823 \u29983 \u32946 \u38454 \u27573 \u65288 \u33829 \u20859 \u29983 \u38271 \u12289 \u24320 \u33457 \u22352 \u26524 \u12289 \u26524 \u23454 \u33192 \u22823 \u65289 \u30340 \u31639 \u27861 \u21270 \u26080 \u32541 \u20999 \u25442 \u12290 \
- **Linear Scaling Engine / \uc0\u32447 \u24615 \u32553 \u25918 \u24341 \u25806 **\
  - **EN:** Computes exact solute mass weights dynamically for any target irrigation volume based on stoichiometry and mass conservation.\
  - **ZH:** \uc0\u22522 \u20110 \u21270 \u23398 \u35745 \u37327 \u19982 \u36136 \u37327 \u23432 \u24658 \u23450 \u24459 \u65292 \u36755 \u20837 \u20219 \u24847 \u30446 \u26631 \u28748 \u28297 \u27700 \u37327 \u65292 \u33258 \u21160 \u35745 \u31639 \u21508 \u21407 \u26009 \u30340 \u31934 \u30830 \u31216 \u37325 \u12290 \
- **Production Ready / \uc0\u24037 \u19994 \u32423 \u38598 \u25104 **\
  - **EN:** Built with strict type checking and defensive boundary validation. Zero external dependencies\'97highly optimized for AIoT edge or cloud integration.\
  - **ZH:** \uc0\u20869 \u32622 \u24378 \u31867 \u22411 \u26816 \u26597 \u19982 \u38450 \u24481 \u24615 \u36793 \u30028 \u39564 \u35777 \u12290 \u38646 \u22806 \u37096 \u20381 \u36182 \u65292 \u26497 \u26131 \u23884 \u20837  AIoT \u36793 \u32536 \u31471 \u25110 \u20113 \u31471 \u27700 \u32933 \u25511 \u21046 \u31995 \u32479 \u12290 \
\
---\
\
### \uc0\u9889  Quick Start / \u24555 \u36895 \u24320 \u22987 \
\
#### 1. Run the Demo / \uc0\u36816 \u34892 \u28436 \u31034 \
**EN:** This project relies strictly on the Python standard library. Run the core module directly to execute telemetry validation loops:\
**ZH:** \uc0\u26412 \u39033 \u30446 \u23436 \u20840 \u22522 \u20110  Python \u26631 \u20934 \u24211 \u24320 \u21457 \u12290 \u30452 \u25509 \u36816 \u34892 \u26680 \u24515 \u27169 \u22359 \u21363 \u21487 \u25191 \u34892 \u36793 \u30028 \u19982 \u25968 \u25454 \u39564 \u35777 \u28436 \u31034 \u65306 \
```bash\
python strawberry_fertigation_calculator.py}