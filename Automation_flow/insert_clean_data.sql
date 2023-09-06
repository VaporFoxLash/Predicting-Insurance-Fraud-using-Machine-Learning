#!/usr/bin/env python
# coding: utf-8

# In[ ]:

CREATE SCHEMA IF NOT EXISTS insurance;

DROP TABLE IF EXISTS insurance.insurance_claims; 

CREATE TABLE insurance.insurance_claims (
  policy_number BIGSERIAL PRIMARY KEY,
  policy_bind_date DATE NULL,
  months_as_customer INT NULL,
  age INT NULL,
  policy_annual_premium FLOAT NULL,
  total_claim_amount FLOAT NULL,
  incident_date DATE NULL,
  incident_severity VARCHAR(56) NULL,
  authorities_contacted VARCHAR(56) NULL,
  incident_state VARCHAR(56) NULL,
  incident_city VARCHAR(56) NULL,
  witnesses INT NULL,
  police_report_available VARCHAR(56) NULL,
  auto_make VARCHAR(56) NULL,
  auto_model VARCHAR(56) NULL,
  auto_year INT NULL,
  fraud_reported VARCHAR(3) NULL
);

SELECT aws_s3.table_import_from_s3(
  'insurance.insurance_claims',
  'policy_number, policy_bind_date, months_as_customer, age, 
  policy_annual_premium, total_claim_amount, incident_date, incident_severity, 
  authorities_contacted, incident_state, incident_city, witnesses, police_report_available, 
  auto_make, auto_model, auto_year, fraud_reported',
  '(format csv, DELIMITER '','' , HEADER false)',
  'de-mbd-predict-methuel-moukangwe-s3-source',
  'insurance_claims_data.csv',
  'eu-west-1'
);