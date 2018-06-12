copy call_center from '/hdd1/data/40g-handled/call_center.dat' with delimiter as '|' NULL '';
    copy catalog_page from '/hdd1/data/40g-handled/catalog_page.dat' with delimiter as '|' NULL '';
    copy catalog_returns from '/hdd1/data/40g-handled/catalog_returns.dat' with delimiter as '|' NULL '';
    copy catalog_sales from '/hdd1/data/40g-handled/catalog_sales.dat' with delimiter as '|' NULL '';
    copy customer from '/hdd1/data/40g-handled/customer.dat' with delimiter as '|' NULL '';
    copy customer_address from '/hdd1/data/40g-handled/customer_address.dat' with delimiter as '|' NULL '';
    copy customer_demographics from '/hdd1/data/40g-handled/customer_demographics.dat' with delimiter as '|' NULL '';
    
    copy date_dim from '/hdd1/data/40g-handled/date_dim.dat' with delimiter as '|' NULL '';
    
    copy dbgen_version from '/hdd1/data/40g-handled/dbgen_version.dat' with delimiter as '|' NULL '';
    copy household_demographics from '/hdd1/data/40g-handled/household_demographics.dat' with delimiter as '|' NULL '';
    copy income_band from '/hdd1/data/40g-handled/income_band.dat' with delimiter as '|' NULL '';
    
    copy inventory from '/hdd1/data/40g-handled/inventory.dat' with delimiter as '|' NULL '';
    
    copy item from '/hdd1/data/40g-handled/item.dat' with delimiter as '|' NULL '';
    
    copy promotion from '/hdd1/data/40g-handled/promotion.dat' with delimiter as '|' NULL '';
    copy reason from '/hdd1/data/40g-handled/reason.dat' with delimiter as '|' NULL '';
    copy ship_mode from '/hdd1/data/40g-handled/ship_mode.dat' with delimiter as '|' NULL '';
    copy store from '/hdd1/data/40g-handled/store.dat' with delimiter as '|' NULL '';
    copy store_returns from '/hdd1/data/40g-handled/store_returns.dat' with delimiter as '|' NULL '';
    
    copy store_sales from '/hdd1/data/40g-handled/store_sales.dat' with delimiter as '|' NULL '';
    
    copy time_dim from '/hdd1/data/40g-handled/time_dim.dat' with delimiter as '|' NULL '';
    
    copy warehouse from '/hdd1/data/40g-handled/warehouse.dat' with delimiter as '|' NULL '';
    
    copy web_page from '/hdd1/data/40g-handled/web_page.dat' with delimiter as '|' NULL '';
    copy web_returns from '/hdd1/data/40g-handled/web_returns.dat' with delimiter as '|' NULL '';
    copy web_sales from '/hdd1/data/40g-handled/web_sales.dat' with delimiter as '|' NULL '';
    copy web_site from '/hdd1/data/40g-handled/web_site.dat' with delimiter as '|' NULL '';



    SELECT nspname || '.' || relname AS "relation",
    pg_size_pretty(pg_relation_size(C.oid)) AS "size"
  FROM pg_class C
  LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
  WHERE nspname NOT IN ('pg_catalog', 'information_schema')
  ORDER BY pg_relation_size(C.oid) DESC;



对生成的数据进行处理（不处理无法导入到表中）—每一行多了一个“|” 
在/part2/tpcds/v2.6.0/datas/目录下创建目录handled 
命令：mkdir handled 
在/part2/tpcds/v2.6.0/datas/目录下执行如下命令：

for i in `ls *.dat`
    do
     name="handled/$i"
     echo $name
     `touch $name`
     `chmod 777 $name`
     sed 's/|$//' $i >> $name;
    done


  http://blog.csdn.net/u011563666/article/details/78751584
  http://www.voidcn.com/article/p-fxpwszws-bhw.html
  https://stackoverflow.com/questions/19463074/postgres-error-could-not-open-file-for-reading-permission-denied