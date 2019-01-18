drop materialized view v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse;

drop materialized view v_catalog_sales, v_catalog_returns, v_inventory, v_date_dim, v_store_sales, v_item, v_warehouse, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28, v29, v30, v31, v32, v33, v34, v35, v36, v37, v38, v39, v40;


0:
create materialized view v_catalog_sales as select * from catalog_sales;

1:
create materialized view v_catalog_returns as select * from catalog_returns;

2:
create materialized view v_inventory as select * from inventory;

3:
create materialized view v_date_dim as select * from date_dim;

4:
create materialized view v_store_sales as select * from store_sales;

5:
create materialized view v_item as select * from item;

select  i_item_desc 
6:
create materialized view v_warehouse as select * from warehouse;

9:
create materialized view v9 as 
       ,i_category 
       ,i_class 
       ,i_current_price
       ,sum(cs_ext_sales_price) as itemrevenue 
       ,sum(cs_ext_sales_price)*100/sum(sum(cs_ext_sales_price)) over
           (partition by i_class) as revenueratio
 from v_catalog_sales
     ,v_item 
     ,v_date_dim
 where cs_item_sk = i_item_sk 
   and i_category in ('Jewelry', 'Sports', 'Books')
   and cs_sold_date_sk = d_date_sk
 and d_date between cast('2001-01-12' as date) 
        and (cast('2001-01-12' as date) + 30)
 group by i_item_id
         ,i_item_desc 
         ,i_category
         ,i_class
         ,i_current_price
 order by i_category
         ,i_class
         ,i_item_id
         ,i_item_desc
         ,revenueratio
limit 100;


10:
create materialized view v10 as 
select  *
 from(select w_warehouse_name
            ,i_item_id
            ,sum(case when (cast(d_date as date) < cast ('1998-04-08' as date))
                  then inv_quantity_on_hand 
                      else 0 end) as inv_before
            ,sum(case when (cast(d_date as date) >= cast ('1998-04-08' as date))
                      then inv_quantity_on_hand 
                      else 0 end) as inv_after
   from v_inventory
       ,v_warehouse
       ,v_item
       ,v_date_dim
   where i_current_price between 0.99 and 1.49
     and i_item_sk          = inv_item_sk
     and inv_warehouse_sk   = w_warehouse_sk
     and inv_date_sk    = d_date_sk
     and d_date between (cast ('1998-04-08' as date) - 30)
                    and (cast ('1998-04-08' as date) + 30)
   group by w_warehouse_name, i_item_id) x
 where (case when inv_before > 0 
             then inv_after / inv_before 
             else null
             end) between 2.0/3.0 and 3.0/2.0
 order by w_warehouse_name
         ,i_item_id
 limit 100;


 11:
 create materialized view v11 as
 select  i_product_name
             ,i_brand
             ,i_class
             ,i_category
             ,avg(inv_quantity_on_hand) qoh
       from v_inventory
           ,v_date_dim
           ,v_item
           ,v_warehouse
       where inv_date_sk=d_date_sk
              and inv_item_sk=i_item_sk
              and inv_warehouse_sk = w_warehouse_sk
              and d_month_seq between 1176 and 1176 + 11
       group by i_product_name
                       ,i_brand
                       ,i_class
                       ,i_category
order by qoh, i_product_name, i_brand, i_class, i_category
limit 100;


12:
create materialized view v12 as
select  dt.d_year 
       ,v_item.i_brand_id brand_id 
       ,v_item.i_brand brand
       ,sum(ss_ext_sales_price) sum_agg
from  v_date_dim dt 
      ,v_store_sales
      ,v_item
 where dt.d_date_sk = v_store_sales.ss_sold_date_sk
   and v_store_sales.ss_item_sk = v_item.i_item_sk
   and v_item.i_manufact_id = 436
   and dt.d_moy=12
 group by dt.d_year
      ,v_item.i_brand
      ,v_item.i_brand_id
 order by dt.d_year
         ,sum_agg desc
         ,brand_id
 limit 100;

13:
 create materialized view v13 as
 select  
   w_state
  ,i_item_id
  ,sum(case when (cast(d_date as date) < cast ('1998-04-08' as date)) 
    then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end) as sales_before
  ,sum(case when (cast(d_date as date) >= cast ('1998-04-08' as date)) 
    then cs_sales_price - coalesce(cr_refunded_cash,0) else 0 end) as sales_after
 from
   v_catalog_sales left outer join v_catalog_returns on
       (cs_order_number = cr_order_number 
        and cs_item_sk = cr_item_sk)
  ,v_warehouse 
  ,v_item
  ,v_date_dim
 where
     i_current_price between 0.99 and 1.49
 and i_item_sk          = cs_item_sk
 and cs_warehouse_sk    = w_warehouse_sk 
 and cs_sold_date_sk    = d_date_sk
 and d_date between (cast ('1998-04-08' as date) - 30)
                and (cast ('1998-04-08' as date) + 30) 
 group by
    w_state,i_item_id
 order by w_state,i_item_id
limit 100;


14:
create materialized view v14 as 
select  dt.d_year
  ,v_item.i_category_id
  ,v_item.i_category
  ,sum(ss_ext_sales_price)
 from   v_date_dim dt
  ,v_store_sales
  ,v_item
 where dt.d_date_sk = v_store_sales.ss_sold_date_sk
  and v_store_sales.ss_item_sk = v_item.i_item_sk
  and v_item.i_manager_id = 1   
  and dt.d_moy=12
  and dt.d_year=1998
 group by   dt.d_year
    ,v_item.i_category_id
    ,v_item.i_category
 order by       sum(ss_ext_sales_price) desc,dt.d_year
    ,v_item.i_category_id
    ,v_item.i_category
limit 100;


15:
create materialized view v15 as
select i_item_desc 
      ,i_category 
      ,i_class 
      ,i_current_price
      ,sum(ss_ext_sales_price) as itemrevenue 
      ,sum(ss_ext_sales_price)*100/sum(sum(ss_ext_sales_price)) over
          (partition by i_class) as revenueratio
from  
  v_store_sales
      ,v_item 
      ,v_date_dim
where 
  ss_item_sk = i_item_sk 
    and i_category in ('Jewelry', 'Sports', 'Books')
    and ss_sold_date_sk = d_date_sk
  and d_date between cast('2001-01-12' as date) 
        and (cast('2001-01-12' as date) + 30)
group by 
  i_item_id
        ,i_item_desc 
        ,i_category
        ,i_class
        ,i_current_price
order by 
  i_category
        ,i_class
        ,i_item_id
        ,i_item_desc
        ,revenueratio;


16:
create materialized view v16 as
select v7.itemrevenue 
       ,v8.inv_before 
       ,v8.inv_after
       ,v9.qoh
       ,v10.sum_agg
       ,v11.sales_before
       ,v12.d_year
       ,v13.revenueratio
from v7, v8, v9, v10, v11, v12, v13
limit 50000000;



17:
create materialized view v17 as
select v14.itemrevenue
       ,v14.inv_before 
       ,v14.inv_after
       ,v14.qoh
       ,v14.sum_agg
from v14
limit 50000000;



18(15*4):
create materialized view v18 as
select v15.inv_before 
       ,v15.inv_after
       ,v_store_sales.ss_ext_sales_price
from v15, v_store_sales
limit 50000000;


19(15*3):
create materialized view v19 as
select v15.qoh
       ,v15.sum_agg
       ,v_date_dim.d_date
from v15, v_date_dim
limit 50000000;


20(15*0):
create materialized view v20 as 
select v15.inv_before 
       ,v15.inv_after
       ,v_catalog_sales.cs_ext_sales_price
from v15, v_catalog_sales
limit 50000000;

21:
create materialized view v21 as 
select v16.inv_after
       ,v16.inv_before  
       ,v17.sum_agg
       ,v17.qoh
       ,v18.cs_ext_sales_price
from v16, v17, v18
limit 50000000;

22:
create materialized view v22 as 
select  v19.inv_after
        ,v19.sum_agg
from v19
limit 50000000;



7:
create materialized view v7 as
select ws_sold_date_sk,
    ws_sold_time_sk,
    ws_ship_date_sk,
    ws_item_sk,
    ws_bill_customer_sk,
    ws_bill_cdemo_sk,
    ws_bill_hdemo_sk,
    ws_bill_addr_sk,
    ws_ship_customer_sk,
    ws_ship_cdemo_sk,
    ws_ship_hdemo_sk,
    ws_ship_addr_sk,
    ws_web_page_sk,
    ws_web_site_sk,
    ws_ship_mode_sk,
    ws_warehouse_sk,
    ws_promo_sk,
    ws_order_number,
    ws_quantity,
    ws_wholesale_cost,
    ws_list_price,
    ws_sales_price,
    ws_ext_discount_amt,
    ws_ext_sales_price,
    ws_ext_wholesale_cost,
    ws_ext_list_price,
    ws_ext_tax,
    ws_coupon_amt,
    ws_ext_ship_cost,
    ws_net_paid,
    ws_net_paid_inc_tax,
    ws_net_paid_inc_ship,
    ws_net_paid_inc_ship_tax,
    ws_net_profit
from web_sales;



8:
create materialized view v8 as
select wr_returned_date_sk,
    wr_returned_time_sk,
    wr_item_sk,
    wr_refunded_customer_sk,
    wr_refunded_cdemo_sk,
    wr_refunded_hdemo_sk,
    wr_refunded_addr_sk,
    wr_returning_customer_sk,
    wr_returning_cdemo_sk,
    wr_returning_hdemo_sk,
    wr_returning_addr_sk,
    wr_web_page_sk,
    wr_reason_sk,
    wr_order_number,
    wr_return_quantity,
    wr_return_amt,
    wr_return_tax,
    wr_return_amt_inc_tax,
    wr_fee,
    wr_return_ship_cost,
    wr_refunded_cash,
    wr_reversed_charge,
    wr_account_credit,
    wr_net_loss
from web_returns;


23:
create materialized view v23 as
select ws_sold_date_sk,
    ws_sold_time_sk,
    ws_ship_date_sk,
    ws_item_sk,
    ws_bill_customer_sk,
    ws_bill_cdemo_sk,
    ws_bill_hdemo_sk,
    ws_bill_addr_sk,
    ws_ship_customer_sk,
    ws_ship_cdemo_sk,
    ws_ship_hdemo_sk,
    ws_ship_addr_sk,
    ws_web_page_sk,
    ws_web_site_sk,
    ws_ship_mode_sk,
    ws_warehouse_sk
from v7;


24:
create materialized view v24 as
select ws_sold_date_sk,
    ws_ship_cdemo_sk,
    ws_ship_hdemo_sk,
    ws_ship_addr_sk,
    ws_web_page_sk,
    ws_web_site_sk,
    ws_ship_mode_sk,
    ws_warehouse_sk,
    ws_promo_sk,
    ws_order_number,
    ws_quantity,
    ws_wholesale_cost,
    ws_list_price,
    ws_sales_price,
    ws_ext_discount_amt,
    ws_ext_sales_price,
    ws_ext_wholesale_cost
from v7;



25:
create materialized view v25 as
select ws_sold_date_sk,
    ws_promo_sk,
    ws_order_number,
    ws_quantity,
    ws_wholesale_cost,
    ws_list_price,
    ws_sales_price,
    ws_ext_discount_amt,
    ws_ext_sales_price,
    ws_ext_wholesale_cost,
    ws_ext_list_price,
    ws_ext_tax,
    ws_coupon_amt,
    ws_ext_ship_cost,
    ws_net_paid,
    ws_net_paid_inc_tax,
    ws_net_paid_inc_ship,
    ws_net_paid_inc_ship_tax,
    ws_net_profit
from v7;



26:
create materialized view v26 as
select ws_sold_date_sk,
    ws_sold_time_sk,
    ws_ship_date_sk,
    ws_item_sk,
    ws_bill_customer_sk,
    ws_bill_cdemo_sk,
    ws_bill_hdemo_sk,
    ws_bill_addr_sk,
    ws_ext_wholesale_cost,
    ws_ext_list_price,
    ws_ext_tax,
    ws_coupon_amt,
    ws_ext_ship_cost,
    ws_net_paid,
    ws_net_paid_inc_tax,
    ws_net_paid_inc_ship,
    ws_net_paid_inc_ship_tax,
    ws_net_profit
from v7;


27:
create materialized view v27 as
select wr_returned_date_sk,
    wr_returned_time_sk,
    wr_item_sk,
    wr_refunded_customer_sk,
    wr_refunded_cdemo_sk,
    wr_refunded_hdemo_sk
from v8;


28:
create materialized view v28 as
select wr_refunded_hdemo_sk,
    wr_refunded_addr_sk,
    wr_returning_customer_sk,
    wr_returning_cdemo_sk,
    wr_returning_hdemo_sk,
    wr_returning_addr_sk
from v8;



29:
create materialized view v29 as
select wr_returned_date_sk,
    wr_order_number,
    wr_return_quantity,
    wr_return_amt,
    wr_return_tax,
    wr_return_amt_inc_tax,
    wr_fee
from v8;


30:
create materialized view v30 as
select wr_returned_date_sk,
    wr_returned_time_sk,
    wr_item_sk,
    wr_return_ship_cost,
    wr_refunded_cash,
    wr_reversed_charge,
    wr_account_credit,
    wr_net_loss
from v8;


31:
create materialized view v31 as
select v23.ws_sold_date_sk,
    v23.ws_sold_time_sk,
    v24.ws_sold_date_sk,
    v24.ws_ship_cdemo_sk,
    v25.ws_order_number,
    v25.ws_quantity,
    v26.ws_item_sk,
    v26.ws_bill_customer_sk,
    v27.wr_returned_time_sk,
    v27.wr_item_sk,
    v28.wr_refunded_hdemo_sk,
    v28.wr_refunded_addr_sk,
    v28.wr_returning_customer_sk,
    v29.wr_returned_date_sk,
    v29.wr_order_number,
    v29.wr_return_quantity,
    v30.wr_returned_date_sk,
    v30.wr_returned_time_sk,
    v30.wr_item_sk
from v23, v24, v25, v26, v27, v28, v29, v30;


32:
create materialized view v32 as
select ws_sold_date_sk,
    ws_sold_time_sk,
    ws_ship_date_sk,
    ws_item_sk,
    ws_bill_customer_sk,
    ws_bill_cdemo_sk,
    ws_bill_hdemo_sk,
    ws_bill_addr_sk
from v23;


33:
create materialized view v33 as
select ws_sold_date_sk,
    ws_ship_cdemo_sk,
    ws_ship_hdemo_sk,
    ws_ship_addr_sk,
    ws_web_page_sk,
    ws_web_site_sk,
    ws_ship_mode_sk,
    ws_warehouse_sk,
    ws_promo_sk
from v24;



34:
create materialized view v34 as
select ws_sold_date_sk,
    ws_promo_sk,
    ws_order_number,
    ws_quantity,
    ws_wholesale_cost,
    ws_list_price,
    ws_sales_price,
    ws_ext_discount_amt,
    ws_ext_sales_price,
    ws_ext_wholesale_cost
from v25;



35:
create materialized view v35 as
select ws_sold_date_sk,
    ws_sold_time_sk,
    ws_ship_date_sk,
    ws_item_sk,
    ws_bill_customer_sk,
    ws_bill_cdemo_sk,
    ws_bill_hdemo_sk,
    ws_bill_addr_sk,
    ws_ext_wholesale_cost,
    ws_ext_list_price
from v26;


36:
create materialized view v36 as
select wr_returned_date_sk,
    wr_returned_time_sk,
    wr_item_sk,
    wr_refunded_customer_sk
from v27;


37:
create materialized view v37 as
select wr_refunded_hdemo_sk,
    wr_refunded_addr_sk,
    wr_returning_customer_sk,
    wr_returning_cdemo_sk
from v28;



38:
create materialized view v38 as
select wr_returned_date_sk,
    wr_order_number,
    wr_return_quantity,
    wr_return_amt
from v29;


39:
create materialized view v39 as
select wr_returned_date_sk,
    wr_returned_time_sk,
    wr_item_sk,
    wr_return_ship_cost,
    wr_refunded_cash
from v30;


40:
create materialized view v40 as
select v32.ws_sold_date_sk,
    v32.ws_sold_time_sk,
    v33.ws_sold_date_sk,
    v33.ws_ship_cdemo_sk,
    v33.ws_ship_hdemo_sk,
    v34.ws_sold_date_sk,
    v34.ws_promo_sk,
    v34.ws_order_number,
    v35.ws_sold_date_sk,
    v35.ws_sold_time_sk,
    v35.ws_ship_date_sk,
    v35.ws_item_sk,
    v36.wr_returned_date_sk,
    v36.wr_returned_time_sk,
    v36.wr_item_sk,
    v37.wr_refunded_hdemo_sk,
    v37.wr_refunded_addr_sk,
    v38.wr_returned_date_sk,
    v38.wr_order_number,
    v39.wr_returned_date_sk,
    v39.wr_returned_time_sk
from v39, v32, v33, v34, v35, v36, v37, v38;
