first you need to have python preinstalled 

do to your cmd 

type following things in order

python --version REM if it return somthing like Python 3.10.11 or Python 3.11.0 or Python 3.12.00 you are good to go (recomended python version Python 3.10.11 or other 10th ed) 
/*
C:\Users\Lenovo>python --version
Python 3.10.11

C:\Users\Lenovo>
*/

mkdir my_flapy_bird REM or any other folder name like game_folder (adjust location accordingly)

/*
C:\Users\Lenovo>mkdir my_flapy_bird REM or any other folder name like game_folder (adjust location accordingly)

C:\Users\Lenovo>
*/


cd my_flapy_bird 

/*
C:\Users\Lenovo>cd my_flapy_bird

C:\Users\Lenovo\my_flapy_bird>
*/

python -m venv myvenv

/*
C:\Users\Lenovo\my_flapy_bird>python -m venv myvenv

C:\Users\Lenovo\my_flapy_bird>
*/


myvenv\Scripts\activate REM this will take some time so hold on

/*
C:\Users\Lenovo\my_flapy_bird>myvenv\Scripts\activate
'crumb' is not recognized as an internal or external command,
operable program or batch file.
'crumb' is not recognized as an internal or external command,
operable program or batch file.
*/

pip install pygame


/*
(myvenv) C:\Users\Lenovo\my_flapy_bird>pip install pygame
Collecting pygame
  Using cached pygame-2.6.1-cp310-cp310-win_amd64.whl (10.6 MB)
Installing collected packages: pygame
Successfully installed pygame-2.6.1

[notice] A new release of pip is available: 23.0.1 -> 26.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip
*/

########################## END ##################################

-----------------------------------------------------------
short recap:-



mkdir my_flapy_bird

cd my_flapy_bird

python -m venv myvenv

myvenv\Scripts\activate

pip install pygame

-----------------------------------------------------------


now open the my_flapy_bird folder in your pycham or VS

and then paste all the files in that folder then run main.py
