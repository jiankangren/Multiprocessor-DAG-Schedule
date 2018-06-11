copy call_center from '/hdd1/data/handled/call_center.dat' with delimiter as '|' NULL '';
    copy catalog_page from '/hdd1/data/handled/catalog_page.dat' with delimiter as '|' NULL '';
    copy catalog_returns from '/hdd1/data/handled/catalog_returns.dat' with delimiter as '|' NULL '';
    copy catalog_sales from '/hdd1/data/handled/catalog_sales.dat' with delimiter as '|' NULL '';
    copy customer from '/hdd1/data/handled/customer.dat' with delimiter as '|' NULL '';
    copy customer_address from '/hdd1/data/handled/customer_address.dat' with delimiter as '|' NULL '';
    copy customer_demographics from '/hdd1/data/handled/customer_demographics.dat' with delimiter as '|' NULL '';
    copy date_dim from '/hdd1/data/handled/date_dim.dat' with delimiter as '|' NULL '';
    copy dbgen_version from '/hdd1/data/handled/dbgen_version.dat' with delimiter as '|' NULL '';
    copy household_demographics from '/hdd1/data/handled/household_demographics.dat' with delimiter as '|' NULL '';
    copy income_band from '/hdd1/data/handled/income_band.dat' with delimiter as '|' NULL '';
    copy inventory from '/hdd1/data/handled/inventory.dat' with delimiter as '|' NULL '';
    copy item from '/hdd1/data/handled/item.dat' with delimiter as '|' NULL '';
    copy promotion from '/hdd1/data/handled/promotion.dat' with delimiter as '|' NULL '';
    copy reason from '/hdd1/data/handled/reason.dat' with delimiter as '|' NULL '';
    copy ship_mode from '/hdd1/data/handled/ship_mode.dat' with delimiter as '|' NULL '';
    copy store from '/hdd1/data/handled/store.dat' with delimiter as '|' NULL '';
    copy store_returns from '/hdd1/data/handled/store_returns.dat' with delimiter as '|' NULL '';
    copy store_sales from '/hdd1/data/handled/store_sales.dat' with delimiter as '|' NULL '';
    copy time_dim from '/hdd1/data/handled/time_dim.dat' with delimiter as '|' NULL '';
    copy warehouse from '/hdd1/data/handled/warehouse.dat' with delimiter as '|' NULL '';
    copy web_page from '/hdd1/data/handled/web_page.dat' with delimiter as '|' NULL '';
    copy web_returns from '/hdd1/data/handled/web_returns.dat' with delimiter as '|' NULL '';
    copy web_sales from '/hdd1/data/handled/web_sales.dat' with delimiter as '|' NULL '';
    copy web_site from '/hdd1/data/handled/web_site.dat' with delimiter as '|' NULL '';



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