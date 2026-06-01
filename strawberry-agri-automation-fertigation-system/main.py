{\rtf1\ansi\ansicpg936\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11880\viewh11400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from strawberry_fertigation_calculator import StrawberryFertigationCalculator\
\
calc = StrawberryFertigationCalculator()\
\
# Calculate requirements for Stage 3 (Expansion) targeting a 500L field tank\
# \uc0\u35745 \u31639 \u31532  3 \u38454 \u27573 \u65288 \u33192 \u22823 \u26399 \u65289 \u37197 \u21046  500L \u33829 \u20859 \u28082 \u25152 \u38656 \u30340 \u21407 \u26009 \u29992 \u37327 \
result = calc.calculate(stage_id=3, target_volume_l=500.0)\
\
# Render formatted batch sheet to standard output\
# \uc0\u25171 \u21360 \u26631 \u20934 \u37197 \u26009 \u21333 \
calc.print_recipe(result)}