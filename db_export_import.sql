
==================== PRODUCTZ ================
==================== PRODUCTZ - WINDOWS EXPORT/IMPORT ================
C:\mysql\bin\mysqldump.exe  -u root -p88footbDb#836 productinfo --result-file=D:\workspace\productz\productinfo\db\productinfo.sql

C:\mysql\bin\mysql.exe  -u root -p88footbDb#836 productinfo < D:\workspace\productz\productinfo\db\productinfo.sql

==================== PRODUCTZ - SERVER/MACOSX EXPORT/IMPORT ================
mysqldump  -u root -p88footbDb#836 productinfo  --result-file=~/git-projects/productz/productinfo/db/productinfo.sql

mysql -u root -p88footbDb#836 productinfo < ~/git-projects/productz/productinfo/db/productinfo.sql
