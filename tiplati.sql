create database tiplati;
use tiplati;

create table if not exists employees (
employee_id int auto_increment primary key,
employee_name varchar(25),
email varchar(25),
role varchar(25),
password varchar(25));

SET SQL_SAFE_UPDATES = 0;

insert into employees values (1,"ashwin","ashwin@gmail.com","admin","ashwin@123") ,
(2,"dinesh","dinesh@gamil.com","admin","dinesh@123"),(3,"sachin","sachin@gmail","user","sachin@123"),
(4,"karthik","karthik@gmail","user","karthik@123");

update employees set email="ashwin@admin" where email="ashwin@gmail.com";
update employees set email="dinesh@admin" where email="dinesh@gamil.com";
select * from employees;

show tables;
drop table testdata;
drop table employees;

select * from testdata; # showcase the dataset 
select count(*) as total_count from testdata; # ensuring that dataset do not inserting duplicate values while re-uploading the dataset

desc testdata;

# converting the column  to there relatable data type
alter table testdata modify timestamp timestamp;
alter table testdata modify Bill_lines int(10);
ALTER TABLE testdata MODIFY COLUMN invoice_number DECIMAL(30,2);
alter table testdata modify hour int(10);
alter table testdata modify month varchar(10);
alter table testdata modify ind_date date;
alter table testdata modify us_date date;
alter table testdata modify pst_to_ist time;
alter table testdata modify total_amt decimal(20,2);
alter table testdata modify invoice_date date;
alter table testdata modify invoice_due_date date;
ALTER TABLE testdata MODIFY ind_time time;
UPDATE testdata
SET invoice_due_date = "2024-09-24" 
where invoice_due_date ="2024/09/24";

UPDATE testdata
SET invoice_due_date = "2024-10-15" 
where invoice_due_date ="2024/10/15";

UPDATE testdata
SET invoice_due_date = "2024-10-02" 
where invoice_due_date ="2024/10/02";

UPDATE testdata 
SET 
    invoice_due_date = '2024-10-30'
WHERE
    invoice_due_date = '2024/10/30';

UPDATE testdata
SET invoice_due_date = "2024-10-31" 
where invoice_due_date ="2024/10/31";

select invoice_due_date from testdata;

alter table testdata modify tax_amt int(10);
UPDATE testdata SET tax_amt = 0 WHERE tax_amt IS NULL;


UPDATE testdata
SET tax_amt = 0;

UPDATE testdata
SET po_number = 0;

select * from testdata;

update testdata set comments = null where comments ="null";
update testdata set emea = null where emea ="null";
update testdata set escalation_desk  = null where escalation_desk ="null";
update testdata set invoice_due_date="2024-10-31" where inVOICE_due_date = "null";
update testdata set foreign_language  = null where foreign_language ="null";
update testdata set track_id  = null where track_id ="null";
update testdata set invoice_number=0 where invoice_number = "null";
update testdata set quality_analyst=null where quality_analyst = "null";
update testdata set priority=null where priority = "null";


select * from testdata;
desc testdata;
/*
timestamp column - timestamp datatype
email- varchar 
tools -varchar 
bill_ref_code - varchar 
track_id- varchar 
payer -varchar 
review - varchar 
bill_lines - int 
capture_payee - varchar 
invoice_num - decimal 
invoice_date - date 
invoice_due_date - date 
po_number = int 
tax_amt = int 
total_amt -decimal 
currency - varchar 
pst_to_ist  - time 
us_date - date
inddate - date 
ind_time= time 
unique_id - unique key 

*/
desc testdata;
select * from testdata;
alter table testdata modify tax_amt decimal(10,2);
alter table testdata modify po_number int(10);
alter table testdata modify invoice_due_date date;
alter table testdata modify invoice_number decimal(20,2);
select count(*) as total_count from testdata;
update testdata set bill_ref_code=null where bill_ref_code="null";
SELECT * FROM `testdata original`; 
drop table `testdata original`;
select count(*) as total_count from `testdata original`;

show tables;
select processing_tool ,team from testdata;

create table if not exists sample_data(
index_no int primary key auto_increment,
email varchar(50),
process_tool varchar(50),
bill_ref_code varchar(100),
payer varchar (50),
Captured_Payee varchar(100));

drop table sample_data;
select * from sample_data;

select * from employees;

select * from testdata where processing_tool="aphub";

select * from test;
drop table test;

update testdata set processing_tool="Rossum" where bill_ref_code="75f54617ca4b4cd9";

select * from testdata;

insert into testdata (timestamp,email_address,processing_tool,payer)values("2024-11-01","sachin.p@santoshtech.com");

insert into testdata (timestamp,email_address,processing_tool,payer)values ("2024-11-04","kuldip.p@santosatech.com","aphub","BTS");

update testdata set processing_tool="Aphub" where processing_tool="kofex";

SELECT DISTINCT payer FROM testdata WHERE payer IS NOT NULL;

drop table `managed service`;
select * from managed;
desc managed;
select count(*) as total_count from managed;

SELECT 
    COUNT(terms) AS non_null_count,  -- This counts the non-null 'terms' values
    COUNT(*) - COUNT(terms) AS null_count  -- This counts the 'NULL' 'terms' values
FROM managed;

SELECT 
    COUNT(OCR) AS non_null_count,  -- This counts the non-null 'terms' values
    COUNT(*) - COUNT(OCR) AS null_count  -- This counts the 'NULL' 'terms' values
FROM managed;

show tables;

select count(*) from sample_service;
select count(*) from service;
select count(*) from dup_service;

select * from service;
select timestamp from service;
select email_address from service limit 1;
select distinct (ocr) from service;
select distinct(bill_ref_code) from service;
select distinct (track_id) from service;
select distinct (annotation_id) from service;
select distinct(document_type) from service;
select distinct(matched_payee_id) from service;
select distinct(payer) from service;
select distinct(review) from service;
select distinct(bill_lines) from service;
select distinct(payee_name) from service;
select distinct(invoice) from service;
select invoice_date from service;
select invoice_due_date from service;
select distinct(terms) from service;
select distinct po from service;
select tax_amt from service;
select total_amt from service;
select currency from service;
select foregin_language from service;
select quality_analyst from service;
select invoice_pages from service;
select multiple_payees from service;
select comments from service;




select distinct(OCR) from service;
select ocr,count(*) from service group by ocr;
select distinct(payer) from service;
select payer,count(*) from service group by payer order by payer;

desc service;

# changing the table data type
alter table service modify email_address varchar(255);
alter table service modify ocr varchar(25);
alter table service modify payer varchar(255);
alter table service rename column `invoice_#` to invoice;
alter table service modify document_type varchar(100);
alter table service rename column `PO_#` TO PO;
desc service;



# admin_service
select * from admin_service;
desc admin_service;

UPDATE admin_service 
SET timestamp = STR_TO_DATE(timestamp, '%d-%m-%Y')
WHERE timestamp IS NOT NULL;

UPDATE admin_service
SET foreign_language = 'english'
WHERE foreign_language IS NULL;

UPDATE admin_service
SET priority = 'normal'
WHERE priority IS NULL;

UPDATE admin_service
SET emea = 'Non-EMEA'  -- Replace 'Non-EMEA' with your desired value
WHERE emea IS NULL;

UPDATE admin_service SET timestamp = DATE(timestamp);

ALTER TABLE admin_service CHANGE timestamp timestamp DATE;

select distinct bill_ref_code from admin_service;

alter table admin_service modify Annotation_id int; 

alter table admin_service drop column date_column;

alter table admin_service modify email_address varchar(255);
alter table admin_service modify ocr varchar(25);
alter table admin_service modify payer varchar(255);
alter table admin_service modify bill_ref_code varchar(200);
alter table admin_service modify matched_payee_id varchar(200);
alter table admin_service rename column `invoice_#` to invoice;
alter table admin_service modify document_type varchar(100);
alter table admin_service rename column `PO_#` TO PO;
alter table admin_service modify track_id varchar(200);
alter table admin_service modify review varchar(10);
alter table admin_service modify Bill_lines int;
alter table admin_service modify payee_name text;
alter table admin_service modify invoice bigint;
alter table admin_service modify terms text;
alter table admin_service modify po text;
alter table admin_service modify tax_amt decimal(10,2);
alter table admin_service modify total_amt decimal(10,2);
alter table admin_service modify currency varchar(10);
alter table admin_service modify foreign_language varchar(15);
alter table admin_service modify Quality_analyst varchar(50);
alter table admin_service modify invoice_pages int;
alter table admin_service modify Multiple_payees varchar(15);
alter table admin_service modify pst_to_ist time;
alter table admin_service modify team text;
alter table admin_service modify Agent varchar(20);
alter table admin_service modify Unique_id text(200);
alter table admin_service add constraint unique(Unique_id (255) );
alter table admin_service modify priority varchar(50);
alter table admin_service modify month varchar(25);
alter table admin_service modify hour int;
alter table admin_service modify EMEA varchar(25);


select * from admin_service;
desc admin_service;
select pst_to_ist from admin_service;

SELECT Unique_id, COUNT(*) 
FROM admin_service 
GROUP BY Unique_id 
HAVING COUNT(*) > 1;  # duplicate records in the table 

# if necessary use the command to delete the duplicate records
DELETE t1 
FROM admin_service t1
JOIN admin_service t2 
ON t1.Unique_id = t2.Unique_id 
WHERE t1.id > t2.id;


show tables;
drop table  admin_1;
drop table testdata;
drop table sample_service;
drop table sample_s;
drop table dup_service;
drop table sample_data;
drop table data;
drop table service;