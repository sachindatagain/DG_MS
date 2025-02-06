create table tiplati;
use tiplati;
 
show tables;

select * from employees;

SET SQL_SAFE_UPDATES = 0;

rename table admin_service to admin_1;
show tables;

select * from admin_service1;
rename table admin_service1 to admin_database;
desc admin_database;

alter table admin_database modify email_address varchar(255);
alter table admin_database modify ocr varchar(25);
alter table admin_database modify payer varchar(255);
alter table admin_database modify bill_ref_code varchar(200);
alter table admin_database modify matched_payee_id varchar(200);
alter table admin_database rename column `invoice_` to invoice;
alter table admin_database modify document_type varchar(100);
# alter table admin_database rename column `PO_` TO PO;
alter table admin_database modify track_id varchar(200);
alter table admin_database modify review varchar(10);
alter table admin_database modify Bill_lines int;
alter table admin_database modify payee_name text;
alter table admin_database modify invoice bigint;
alter table admin_database modify terms text;
alter table admin_database modify po text;
alter table admin_database modify tax_amt decimal(10,2);
alter table admin_database modify total_amt decimal(10,2);
alter table admin_database modify currency varchar(10);
alter table admin_database modify foreign_language varchar(15);
alter table admin_database modify Quality_analyst varchar(50);
alter table admin_database modify invoice_pages int;
alter table admin_database modify Multiple_payees varchar(15);
alter table admin_database modify pst_to_ist time;
alter table admin_database modify team text;
alter table admin_database modify Agent varchar(20);
alter table admin_database modify Unique_id text(200);
# alter table admin_database add constraint unique(Unique_id (255) );
alter table aadmin_database modify priority varchar(50);
alter table admin_database modify month varchar(25);
alter table admin_database modify hour int;
alter table admin_database modify EMEA varchar(25);
alter table admin_database modify timestamp date;
alter table admin_database modify us_date date;
alter table admin_database modify ind_date date;

desc admin_database;
UPDATE admin_database 
SET us_date = STR_TO_DATE(us_date, '%d-%m-%Y')
WHERE timestamp IS NOT NULL;

UPDATE admin_database 
SET ind_date = STR_TO_DATE(ind_date, '%d-%m-%Y')
WHERE timestamp IS NOT NULL;

SELECT Unique_id, COUNT(*) 
FROM admin_database 
GROUP BY Unique_id 
HAVING COUNT(*) > 1;  # duplicate records in the table 

# if necessary use the command to delete the duplicate records
DELETE t1 
FROM admin_service t1
JOIN admin_service t2 
ON t1.Unique_id = t2.Unique_id 
WHERE t1.id > t2.id;