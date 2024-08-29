cd %1
rmdir /S /Q recipes
mkdir recipes
call micromamba run -n devenv vinca -m

