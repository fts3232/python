@echo off
sc query mysql > nul
if %errorlevel% NEQ 0 (
    echo 等待安装mysql服务
    start /w E:\wamp64\bin\mysql\mysql5.7.14\bin\mysqld --install
    echo 安装mysql服务成功
)else (
    echo mysql已安装
)
for /f "skip=3 tokens=4" %%i in ('sc query MySQL') do set "zt=%%i" & goto :next
:next
if /i "%zt%"=="RUNNING" (
    echo myslq服务已启动
)else (
    echo 等待mysql服务启动
    start /w net start mysql
    echo mysql服务启动成功
)
sc query mongodb > nul
if %errorlevel% NEQ 0 (
    echo 等待安装mongodb服务
    start /w C:\"Program Files"\MongoDB\Server\3.4\bin\mongod.exe --logpath D:\MongoDB\logs\mongodb.log --logappend --dbpath D:\MongoDB\data --directoryperdb --serviceName MongoDB --auth --install
    echo 安装mongodb服务成功
)else (
    echo mongodb已安装
)
for /f "skip=3 tokens=4" %%i in ('sc query MongoDB') do set "zt=%%i" & goto :next
:next
if /i "%zt%"=="RUNNING" (
    echo mongodb服务已启动
)else (
    echo 等待mongodb服务启动
    start /w net start mongodb
    echo mongodb服务启动成功
)
echo 等待redis服务启动
start D:\Redis-x64-3.0.500\redis-server.exe
echo redis服务启动成功
start python Server.py
start npm start