0:
create materialized view v0 as select * from store_sales;


1:
create materialized view v1 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_cdemo_sk
      ,ss_hdemo_sk
      ,ss_addr_sk
      ,ss_store_sk
      ,ss_promo_sk
      ,ss_ticket_number
      ,ss_quantity
      ,ss_wholesale_cost
      ,ss_list_price
      ,ss_sales_price
      ,ss_ext_discount_amt
      ,ss_ext_sales_price
      ,ss_ext_wholesale_cost
      ,ss_ext_list_price
      ,ss_ext_tax
      ,ss_coupon_amt
      ,ss_net_paid
      ,ss_net_paid_inc_tax
      ,ss_net_profit
from v0;


2:
create materialized view v2 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_cdemo_sk
      ,ss_hdemo_sk
      ,ss_addr_sk
      ,ss_store_sk
      ,ss_promo_sk
      ,ss_ticket_number
      ,ss_quantity
      ,ss_wholesale_cost
      ,ss_list_price
      ,ss_sales_price
      ,ss_ext_discount_amt
      ,ss_ext_sales_price
      ,ss_ext_wholesale_cost
      ,ss_ext_list_price
      ,ss_ext_tax
      ,ss_coupon_amt
from v1;


3:
create materialized view v3 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_cdemo_sk
      ,ss_hdemo_sk
      ,ss_addr_sk
      ,ss_store_sk
      ,ss_promo_sk
      ,ss_ticket_number
      ,ss_quantity
      ,ss_wholesale_cost
      ,ss_list_price
      ,ss_sales_price
      ,ss_ext_discount_amt
      ,ss_ext_sales_price
from v2;


4:
create materialized view v4 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
      ,ss_cdemo_sk
      ,ss_hdemo_sk
      ,ss_addr_sk
      ,ss_store_sk
      ,ss_promo_sk
      ,ss_ticket_number
      ,ss_quantity
      ,ss_wholesale_cost
      ,ss_list_price
      ,ss_sales_price
from v3;


5:
create materialized view v5 as
select ss_customer_sk
      ,ss_addr_sk
      ,ss_store_sk
from v4;


6:
create materialized view v6 as
select ss_sold_date_sk
      ,ss_sold_time_sk
      ,ss_item_sk
      ,ss_customer_sk
from v4;


7:
create materialized view v7 as
select count(distinct ss_customer_sk)
from v6;


8:
create materialized view v8 as
select ss_cdemo_sk
      ,ss_hdemo_sk
      ,ss_addr_sk
      ,ss_store_sk
from v4;


9:
create materialized view v9 as
select count(distinct ss_store_sk)
from v8;


10:
create materialized view v10 as
select ss_item_sk
      ,ss_customer_sk
      ,ss_promo_sk
      ,ss_ticket_number
from v4;


11:
create materialized view v11 as
select count(ss_ticket_number)
from v10;


12:
create materialized view v12 as
select ss_quantity
      ,ss_wholesale_cost
      ,ss_list_price
      ,ss_sales_price
from v4;


13:
create materialized view v13 as
select sum(ss_sales_price)
from v12;

