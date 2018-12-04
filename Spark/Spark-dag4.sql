drop table v0; 
drop table v1;
drop table v2;
drop table v3;
drop table v4;
drop table v5;
drop table v6;
drop table v7;
drop table v8;
drop table v9;
drop table v10;
drop table v11;
drop table v12;
drop table v13;
drop table v14;
drop table v15;
drop table v16;
drop table v17;
drop table v18;
drop table v19;
drop table catalog_sales_text;
drop table catalog_returns_text;
drop table store_sales_text;
drop table date_dim_text;
drop table inventory_text;
drop table web_sales_text;
drop table store_returns_text;
drop table customer_text;
drop table customer_address_text;
drop table customer_demographics_text;
drop table web_returns_text;
drop table item_text;


0:
create table v0 as select * from catalog_sales_text;

1:
create table v1 as select * from catalog_returns_text;

2:
create table v2 as select * from store_sales_text;

3:
create table v3 as select * from date_dim_text;

4:
create table v4 as select * from inventory_text;

5:
create table v5 as select * from web_sales_text;

6:
create table v6 as select * from store_returns_text;

7:
create table v7 as select * from customer_text;

8:
create table v8 as select * from customer_address_text;

9:
create table v9 as select * from customer_demographics_text;

10:
create table v10 as select * from web_returns_text;

11:
create table v11 as select * from item_text;


12:
create table v12 as
select cs_sold_date_sk
      ,cs_sales_price
      ,cr_returned_date_sk
      ,cr_return_amount
      ,ss_item_sk
      ,ss_customer_sk
      ,d_date_sk
      ,d_date
from v0 cross join v1 cross join v2 cross join v3
limit 50000;


13:
create table v13 as
select cs_sold_date_sk
      ,cr_returned_date_sk
      ,ss_item_sk
      ,d_date_sk
from v12;


14:
create table v14 as
select v12.cs_sold_date_sk
      ,v12.cs_sales_price
      ,v12.cr_returned_date_sk
      ,v13.ss_item_sk
from v12 cross join v13
limit 50000;


15:
create table v15 as
select v12.cr_returned_date_sk
      ,v12.cr_return_amount
from v12
limit 50000;


16:
create table v16 as
select v12.ss_item_sk
      ,v12.ss_customer_sk
from v12
limit 500000;


17:
create table v17 as
select v12.d_date_sk
      ,v12.d_date
from v12
limit 500000;


18:
create table v18 as
select v12.cs_sales_price
      ,v12.cr_returned_date_sk
      ,v14.ss_item_sk
      ,v15.cr_return_amount
      ,v16.ss_customer_sk
      ,v17.d_date
      ,v19.i_item_id
from v12 cross join v14 cross join v15 cross join v16 cross join v17 cross join v19
limit 50000;


19:
create table v19 as
select inv_item_sk
      ,ws_item_sk
      ,sr_ticket_number
      ,c_customer_sk
      ,ca_address_id
      ,cd_education_status
      ,wr_returned_time_sk
      ,i_item_id
from v4 cross join v5 cross join v6 cross join v7 cross join v8 cross join v9 cross join v10 cross join v11
limit 60000;