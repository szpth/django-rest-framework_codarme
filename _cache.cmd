FOR /d /r . %%d IN (__pycache__) DO @IF EXIST "%%d" rd /s /q "%%d"
rd /s /q "logs"
rd /s /q ".pytest_cache"
cls
exit
